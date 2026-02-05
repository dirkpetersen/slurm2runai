"""Core conversion functionality."""

import os
from typing import Optional

import requests

from s2r.auth import create_signed_headers


# Default API endpoint - you'll replace this with your Lambda URL
DEFAULT_API_ENDPOINT = os.environ.get(
    "S2R_API_ENDPOINT",
    "https://btohftfievc7zn5ffic7e5jrve0gzafw.lambda-url.us-west-2.on.aws/"
)

# AWS region for Function URL (used for IAM auth)
DEFAULT_AWS_REGION = os.environ.get("S2R_AWS_REGION", "us-west-2")

# Whether to use IAM authentication (requires boto3 and AWS credentials)
USE_IAM_AUTH = os.environ.get("S2R_USE_IAM_AUTH", "true").lower() in ("true", "1", "yes")


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
            "boto3 is required for IAM authentication. Install with: pip install boto3"
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

    endpoint = api_endpoint or DEFAULT_API_ENDPOINT
    iam_auth = use_iam_auth if use_iam_auth is not None else USE_IAM_AUTH
    region = aws_region or DEFAULT_AWS_REGION

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
