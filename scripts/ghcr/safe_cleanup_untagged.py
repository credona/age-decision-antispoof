import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

RELEASE_TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")
API_VERSION = "2022-11-28"


def env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def gh_request(method: str, url: str, token: str, data: bytes | None = None) -> tuple[int, dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = resp.read().decode("utf-8")
        return resp.status, json.loads(payload) if payload else {}


def list_all_versions(owner: str, package_name: str, token: str) -> list[dict]:
    encoded_package = urllib.parse.quote(package_name, safe="")
    url = (
        f"https://api.github.com/orgs/{owner}/packages/container/"
        f"{encoded_package}/versions?per_page=100"
    )
    versions: list[dict] = []

    while url:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": API_VERSION,
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            versions.extend(json.loads(body))
            link = resp.headers.get("Link", "")

        next_url = None
        for part in link.split(","):
            part = part.strip()
            if 'rel="next"' in part and "<" in part and ">" in part:
                next_url = part[part.find("<") + 1 : part.find(">")]
                break
        url = next_url

    return versions


def extract_tags(version: dict) -> list[str]:
    return version.get("metadata", {}).get("container", {}).get("tags", []) or []


def extract_digest(version: dict) -> str | None:
    return version.get("name")


def main() -> None:
    token = os.environ["GITHUB_TOKEN"]
    owner = os.environ.get("OWNER", "credona")
    package_name = os.environ["PACKAGE_NAME"]
    dry_run = env_bool("DRY_RUN", default=True)

    versions = list_all_versions(owner, package_name, token)
    print(f"Scanned {len(versions)} GHCR versions for {owner}/{package_name}")
    print(f"Dry run: {dry_run}")

    release_tagged_digests: set[str] = set()
    for version in versions:
        tags = extract_tags(version)
        digest = extract_digest(version)
        if digest and any(RELEASE_TAG_RE.match(tag) for tag in tags):
            release_tagged_digests.add(digest)

    for version in versions:
        version_id = version.get("id")
        tags = extract_tags(version)
        digest = extract_digest(version)

        if tags:
            continue

        if not version_id:
            print("Skip untagged version with missing id (cannot prove safety)")
            continue
        if not digest:
            print(f"Skip version {version_id}: missing digest/name (cannot prove safety)")
            continue
        if digest in release_tagged_digests:
            print(
                f"Skip version {version_id}: digest {digest} is also associated with a release tag"
            )
            continue

        encoded_package = urllib.parse.quote(package_name, safe="")
        delete_url = (
            f"https://api.github.com/orgs/{owner}/packages/container/"
            f"{encoded_package}/versions/{version_id}"
        )
        if dry_run:
            print(f"[DRY-RUN] Would delete untagged version id={version_id}, digest={digest}")
            continue

        try:
            status, _ = gh_request("DELETE", delete_url, token)
            if status in {200, 202, 204}:
                print(f"Deleted untagged version id={version_id}, digest={digest}")
            else:
                print(f"Skip version {version_id}: unexpected delete status {status}")
        except urllib.error.HTTPError as exc:
            print(f"Skip version {version_id}: delete failed with HTTP {exc.code}")


if __name__ == "__main__":
    main()
