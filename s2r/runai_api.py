"""Run:ai REST API helpers for datasource provisioning.

Used by the s2r setup wizard to register S3 buckets as Run:ai datasources.

Token source: ~/.runai/authentication.json — the accessToken field is wrapped
in an extra layer of base64 (the decoded payload is the JWT itself), so we
base64-decode once before sending it as a Bearer token.
"""

import base64
import configparser
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Tuple

AUTH_FILE = Path.home() / ".runai" / "authentication.json"
CONFIG_FILE = Path.home() / ".runai" / "config.json"


class RunaiAPIError(RuntimeError):
    """Raised for any failure talking to the Run:ai REST API."""


def _token() -> str:
    """Return the Bearer token from ~/.runai/authentication.json.

    The accessToken in this file is base64-encoded (the decoded payload IS the
    JWT). Decode one layer; the result is a `header.payload.signature` JWT.
    """
    if not AUTH_FILE.is_file():
        raise RunaiAPIError(f"Not logged in: {AUTH_FILE} does not exist. Run 'runai login'.")
    with AUTH_FILE.open() as f:
        d = json.load(f)
    raw = d.get("accessToken", "")
    if not raw:
        raise RunaiAPIError(f"No accessToken in {AUTH_FILE}.")
    pad = len(raw) % 4
    if pad:
        raw += "=" * (4 - pad)
    try:
        return base64.b64decode(raw).decode()
    except Exception as e:
        raise RunaiAPIError(f"Failed to decode accessToken: {e}")


def _runai_url() -> str:
    """Read the control-plane URL from ~/.runai/config.json. Raises on failure."""
    if not CONFIG_FILE.is_file():
        raise RunaiAPIError(f"{CONFIG_FILE} does not exist. Run 'runai login'.")
    with CONFIG_FILE.open() as f:
        d = json.load(f)
    url = d.get("control_plane", {}).get("url", "").rstrip("/")
    if not url:
        raise RunaiAPIError(f"No control_plane.url in {CONFIG_FILE}.")
    return url


def _cluster_id() -> str:
    """Read the active cluster UUID from ~/.runai/config.json. Raises on failure."""
    if not CONFIG_FILE.is_file():
        raise RunaiAPIError(f"{CONFIG_FILE} does not exist. Run 'runai login'.")
    with CONFIG_FILE.open() as f:
        d = json.load(f)
    uid = d.get("cluster", {}).get("uuid", "")
    if not uid:
        raise RunaiAPIError(f"No cluster.uuid in {CONFIG_FILE}.")
    return uid


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _request(method: str, url: str, token: str, payload: dict = None) -> dict:
    """Send an HTTPS request and return the parsed JSON response."""
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=_headers(token), method=method)
    try:
        with urllib.request.urlopen(req) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RunaiAPIError(f"{method} {url} → HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise RunaiAPIError(f"{method} {url} → {e.reason}")
    if not body:
        return {}
    try:
        return json.loads(body)
    except ValueError as e:
        raise RunaiAPIError(f"{method} {url} → invalid JSON: {e}")


def _get(url: str, token: str) -> dict:
    return _request("GET", url, token)


def _post(url: str, token: str, payload: dict) -> dict:
    return _request("POST", url, token, payload)


def _list_projects(base_url: str, token: str) -> List[dict]:
    """Return all projects visible to the current user."""
    data = _get(f"{base_url}/api/v1/org-unit/projects", token)
    return data.get("projects", [])


def _project_meta(base_url: str, token: str, project_name: str) -> Tuple[int, str]:
    """Return (projectId, clusterId) for the given project name.

    Uses the org-unit/projects endpoint, which always works for greenfield
    projects (no existing assets needed).
    """
    for p in _list_projects(base_url, token):
        if p.get("name") == project_name:
            pid = p.get("id")
            cid = p.get("clusterId")
            if pid is None or cid is None:
                raise RunaiAPIError(f"Project '{project_name}' missing id/clusterId: {p}")
            return int(pid), cid
    raise RunaiAPIError(f"Project '{project_name}' not found via /api/v1/org-unit/projects")


def get_aws_region(profile: str = "") -> str:
    """Return the AWS region from the standard chain.

    Order: AWS_REGION → AWS_DEFAULT_REGION env vars → explicit profile arg
    → AWS_PROFILE env var → 'default' profile in ~/.aws/config.
    Returns empty string if nothing is configured (caller should fall back).
    """
    region = os.environ.get("AWS_REGION", "") or os.environ.get("AWS_DEFAULT_REGION", "")
    if region:
        return region

    config_file = Path.home() / ".aws" / "config"
    if not config_file.is_file():
        return ""

    c = configparser.ConfigParser()
    c.read(config_file)
    chosen = profile or os.environ.get("AWS_PROFILE", "") or "default"
    # In ~/.aws/config, non-default profiles are named "profile <name>"
    section = chosen if chosen == "default" else f"profile {chosen}"
    if section in c:
        return c[section].get("region", "")
    return ""


def s3_endpoint_url(profile: str = "") -> str:
    """Return the S3 endpoint URL for the configured AWS region."""
    region = get_aws_region(profile)
    if region:
        return f"https://s3.{region}.amazonaws.com"
    return "https://s3.amazonaws.com"


def get_aws_credentials(profile: str = "") -> Tuple[str, str]:
    """Return (access_key_id, secret_access_key) from the standard AWS credential chain.

    Order: AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY env vars → explicit profile arg
    → AWS_PROFILE env var → 'default' profile in ~/.aws/credentials.

    Does NOT silently fall through to "first available profile" — that risks
    using the wrong AWS account.
    """
    ak = os.environ.get("AWS_ACCESS_KEY_ID", "")
    sk = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    if ak and sk:
        return ak, sk

    creds_file = Path.home() / ".aws" / "credentials"
    if not creds_file.exists():
        raise RunaiAPIError(
            "No AWS credentials found. Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY "
            "or configure ~/.aws/credentials."
        )

    c = configparser.ConfigParser()
    c.read(creds_file)
    chosen = profile or os.environ.get("AWS_PROFILE", "") or "default"
    if chosen not in c:
        available = ", ".join(c.sections()) or "(none)"
        raise RunaiAPIError(
            f"AWS profile '{chosen}' not found in {creds_file}. Available: {available}"
        )
    ak = c[chosen].get("aws_access_key_id", "")
    sk = c[chosen].get("aws_secret_access_key", "")
    if not (ak and sk):
        raise RunaiAPIError(
            f"AWS profile '{chosen}' is missing aws_access_key_id or aws_secret_access_key."
        )
    return ak, sk


def list_s3_datasources(project_name: str) -> List[str]:
    """Return list of S3 datasource names for the given project. [] on any failure."""
    try:
        token = _token()
        base_url = _runai_url()
        data = _get(f"{base_url}/api/v1/asset/datasource/s3", token)
    except RunaiAPIError:
        return []
    return [
        e["meta"]["name"]
        for e in data.get("entries", [])
        if e.get("meta", {}).get("projectName") == project_name
    ]


def datasource_exists(bucket_name: str, project_name: str) -> bool:
    """Return True if an S3 datasource with this name already exists."""
    return bucket_name in list_s3_datasources(project_name)


def create_s3_datasource(
    bucket_name: str,
    project_name: str,
    s3_url: str = "",
    bucket_path: str = "",
    aws_profile: str = "",
) -> str:
    """Create an S3 credential + datasource in Run:ai. Returns the datasource name.

    AWS credentials are read from the standard chain (env vars → aws_profile → default).
    If s3_url is empty, defaults to https://s3.<region>.amazonaws.com using the
    profile's configured region (avoids cross-region 301 redirects in goofys).
    If bucket_path is empty, defaults to /mnt/<bucket-name> (the container mount).
    Raises RunaiAPIError on failure.
    """
    if "/" in bucket_name or not bucket_name:
        raise RunaiAPIError(
            f"Invalid bucket name {bucket_name!r}: must not contain '/'. "
            "Pass the bare bucket name (not s3://uri or path)."
        )

    if not s3_url:
        s3_url = s3_endpoint_url(aws_profile)
    if not bucket_path:
        bucket_path = f"/mnt/{bucket_name}"

    access_key_id, secret_access_key = get_aws_credentials(aws_profile)
    token = _token()
    base_url = _runai_url()
    project_id, cluster_id = _project_meta(base_url, token, project_name)

    meta_base = {
        "name": bucket_name,
        "scope": "project",
        "projectId": project_id,
        "clusterId": cluster_id,
    }

    cred_resp = _post(
        f"{base_url}/api/v1/asset/credentials/access-key",
        token,
        {
            "meta": meta_base,
            "spec": {"accessKeyId": access_key_id, "secretAccessKey": secret_access_key},
        },
    )
    cred_id = cred_resp.get("meta", {}).get("id") or cred_resp.get("id")
    if not cred_id:
        raise RunaiAPIError(f"Credential creation returned no id: {cred_resp}")

    ds_resp = _post(
        f"{base_url}/api/v1/asset/datasource/s3",
        token,
        {
            "meta": meta_base,
            "spec": {
                "bucket": bucket_name,
                "url": s3_url,
                "path": bucket_path,
                "accessKeyAssetId": cred_id,
            },
        },
    )
    return ds_resp.get("meta", {}).get("name") or bucket_name
