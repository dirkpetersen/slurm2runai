"""Core conversion functionality."""

import os
from typing import Optional

import requests

from s2r.auth import create_signed_headers


# Default API endpoint - you'll replace this with your Lambda URL
DEFAULT_API_ENDPOINT = os.environ.get(
    "S2R_API_ENDPOINT",
    "https://your-lambda-url.lambda-url.us-east-1.on.aws/"
)


class ConversionError(Exception):
    """Raised when conversion fails."""
    pass


def convert_slurm_to_runai(
    slurm_script: str,
    api_endpoint: Optional[str] = None,
    timeout: int = 60
) -> str:
    """Convert a SLURM script to Run.ai configuration.

    Args:
        slurm_script: SLURM batch script content
        api_endpoint: Optional custom API endpoint (defaults to S2R_API_ENDPOINT env var)
        timeout: Request timeout in seconds

    Returns:
        Run.ai configuration (YAML or CLI commands)

    Raises:
        ConversionError: If conversion fails
    """
    if not slurm_script.strip():
        raise ConversionError("SLURM script cannot be empty")

    endpoint = api_endpoint or DEFAULT_API_ENDPOINT

    # Create signed request
    headers = create_signed_headers(slurm_script)

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
