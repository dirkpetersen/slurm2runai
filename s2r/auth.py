"""Authentication utilities for signed requests."""

import hashlib
import hmac
import time
from typing import Dict


# Shared secret - this will be hardcoded in both library and Lambda
# In production, you'd rotate this periodically
SHARED_SECRET = "s2r-shared-secret-change-this-in-production"


def generate_signature(payload: str, timestamp: str, secret: str = SHARED_SECRET) -> str:
    """Generate HMAC signature for request authentication.

    Args:
        payload: The request body (SLURM script content)
        timestamp: ISO format timestamp string
        secret: Shared secret key

    Returns:
        Hex-encoded HMAC-SHA256 signature
    """
    message = f"{timestamp}:{payload}"
    signature = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature


def verify_signature(
    payload: str,
    timestamp: str,
    signature: str,
    secret: str = SHARED_SECRET,
    max_age_seconds: int = 300
) -> bool:
    """Verify request signature and timestamp.

    Args:
        payload: The request body
        timestamp: ISO format timestamp string
        signature: Signature to verify
        secret: Shared secret key
        max_age_seconds: Maximum age of request in seconds (prevents replay attacks)

    Returns:
        True if signature is valid and timestamp is recent
    """
    # Verify timestamp is recent (prevent replay attacks)
    try:
        request_time = float(timestamp)
        current_time = time.time()
        if abs(current_time - request_time) > max_age_seconds:
            return False
    except (ValueError, TypeError):
        return False

    # Verify signature
    expected_signature = generate_signature(payload, timestamp, secret)
    return hmac.compare_digest(signature, expected_signature)


def create_signed_headers(payload: str) -> Dict[str, str]:
    """Create headers with signature for API request.

    Args:
        payload: The request body

    Returns:
        Dictionary of headers including timestamp and signature
    """
    timestamp = str(time.time())
    signature = generate_signature(payload, timestamp)

    return {
        "X-S2R-Timestamp": timestamp,
        "X-S2R-Signature": signature,
        "Content-Type": "text/plain",
    }
