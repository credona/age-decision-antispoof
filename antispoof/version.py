"""Application version metadata.

This module keeps backward-compatible constants while project metadata is now
loaded from project.json.
"""

from antispoof.project import project_metadata

APP_NAME = project_metadata.app_name
APP_VERSION = project_metadata.version
SERVICE_NAME = project_metadata.service_name
CONTRACT_VERSION = project_metadata.contract_version
