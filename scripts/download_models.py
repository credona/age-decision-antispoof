from pathlib import Path

import requests

MODELS_DIR = Path("antispoof/models")

MODELS = {
    "MiniFASNetV2.onnx": "https://github.com/yakhyo/face-anti-spoofing/releases/download/weights/MiniFASNetV2.onnx"
}


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        print(f"Already exists: {destination}")
        return

    print(f"Downloading: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    destination.write_bytes(response.content)
    print(f"Downloaded: {destination}")


def main() -> None:
    for filename, url in MODELS.items():
        download_file(url, MODELS_DIR / filename)


if __name__ == "__main__":
    main()
