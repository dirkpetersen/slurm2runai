"""Core conversion functionality."""

import os
from typing import Optional

import requests

from s2r.auth import create_signed_headers
from s2r.env import load_env_file

# Default API endpoint - you'll replace this with your Lambda URL
DEFAULT_API_ENDPOINT_FALLBACK = "https://zzk4zf48pi.execute-api.us-west-2.amazonaws.com/"


def _bucket_name(bucket: str) -> str:
    """Extract bare bucket name from s3://bucket/path or plain bucket."""
    name = bucket
    for prefix in ("s3://", "s3a://", "s3n://"):
        if name.lower().startswith(prefix):
            name = name[len(prefix):]
            break
    return name.split("/")[0]


def _inject_context(slurm_script: str) -> str:
    """Prepend a context block with Run:ai hints if any are set in the environment."""
    project = os.environ.get("RUNAI_PROJECT", "")
    bucket  = os.environ.get("RUNAI_BUCKET", "")
    cache   = os.environ.get("RUNAI_CACHE", "")

    lines = []
    if project:
        lines.append(f"# RUNAI_PROJECT: {project}")
    if bucket:
        bname = _bucket_name(bucket)
        lines.append(f"# RUNAI_BUCKET: {bucket}")
        lines.append(f"# RUNAI_BUCKET_NAME: {bname}")
        lines.append(f"# RUNAI_BUCKET_MOUNT: /mnt/{bname}")
    if cache:
        lines.append(f"# RUNAI_CACHE: {cache}")
    if not lines:
        return slurm_script
    header = "# --- s2r context (use these values in the output) ---\n"
    header += "\n".join(lines) + "\n"
    header += "# -----------------------------------------------------\n"
    return header + slurm_script


class ConversionError(Exception):
    """Raised when conversion fails."""
    pass


def _get_aws_signed_headers(
    endpoint: str,
    payload: str,
    headers: dict,
    region: str
) -> dict:
    """Add AWS SigV4 signature to headers for IAM-authenticated Lambda Function URL."""
    try:
        import boto3
        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest
    except ImportError:
        raise ConversionError(
            "boto3 is required for IAM authentication. Install with: pip install 's2r[iam-auth]'"
        )

    # Get credentials from default credential chain (env vars, ~/.aws/credentials, IAM role, etc.)
    session = boto3.Session()
    credentials = session.get_credentials()

    if credentials is None:
        raise ConversionError(
            "No AWS credentials found. Configure credentials via environment variables, "
            "~/.aws/credentials, or IAM role."
        )

    # Create and sign the request
    request = AWSRequest(
        method='POST',
        url=endpoint,
        data=payload.encode('utf-8'),
        headers=headers
    )
    SigV4Auth(credentials, 'lambda', region).add_auth(request)

    return dict(request.headers)


def convert_slurm_to_runai(
    slurm_script: str,
    api_endpoint: Optional[str] = None,
    timeout: int = 90,
    use_iam_auth: Optional[bool] = None,
    aws_region: Optional[str] = None
) -> str:
    """Convert a SLURM script to Run.ai configuration.

    Args:
        slurm_script: SLURM batch script content
        api_endpoint: Optional custom API endpoint (defaults to S2R_API_ENDPOINT env var)
        timeout: Request timeout in seconds
        use_iam_auth: Whether to use AWS IAM authentication (defaults to S2R_USE_IAM_AUTH env var)
        aws_region: AWS region for SigV4 signing (defaults to S2R_AWS_REGION env var)

    Returns:
        Run.ai configuration (YAML or CLI commands)

    Raises:
        ConversionError: If conversion fails
    """
    if not slurm_script.strip():
        raise ConversionError("SLURM script cannot be empty")

    # Load runai.env into os.environ on first use (shell env still wins).
    load_env_file()

    slurm_script = _inject_context(slurm_script)
    endpoint = api_endpoint or os.environ.get("S2R_API_ENDPOINT", DEFAULT_API_ENDPOINT_FALLBACK)
    if use_iam_auth is None:
        use_iam_auth = os.environ.get("S2R_USE_IAM_AUTH", "false").lower() in ("true", "1", "yes")
    iam_auth = use_iam_auth
    region = aws_region or os.environ.get("S2R_AWS_REGION", "us-west-2")

    # Create signed request headers (HMAC signature for Lambda validation)
    headers = create_signed_headers(slurm_script)

    # Add AWS SigV4 signature if using IAM authentication
    if iam_auth:
        headers = _get_aws_signed_headers(endpoint, slurm_script, headers, region)

    try:
        response = requests.post(
            endpoint,
            data=slurm_script.encode("utf-8"),
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()

        result = response.json()

        if "error" in result:
            raise ConversionError(f"API error: {result['error']}")

        return result.get("runai_config", "")

    except requests.exceptions.Timeout:
        raise ConversionError("Request timed out")
    except requests.exceptions.RequestException as e:
        raise ConversionError(f"Request failed: {e}")
    except ValueError as e:
        raise ConversionError(f"Invalid JSON response: {e}")
