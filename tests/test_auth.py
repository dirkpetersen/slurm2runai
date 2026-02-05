"""Tests for authentication module."""

import time

from s2r.auth import generate_signature, verify_signature, create_signed_headers


def test_generate_signature() -> None:
    """Test signature generation."""
    payload = "test payload"
    timestamp = "1234567890.0"
    secret = "test-secret"

    sig1 = generate_signature(payload, timestamp, secret)
    sig2 = generate_signature(payload, timestamp, secret)

    # Same inputs should produce same signature
    assert sig1 == sig2
    assert len(sig1) == 64  # SHA256 hex is 64 chars


def test_verify_signature_valid() -> None:
    """Test signature verification with valid signature."""
    payload = "test payload"
    timestamp = str(time.time())
    secret = "test-secret"

    signature = generate_signature(payload, timestamp, secret)
    assert verify_signature(payload, timestamp, signature, secret)


def test_verify_signature_invalid() -> None:
    """Test signature verification with invalid signature."""
    payload = "test payload"
    timestamp = str(time.time())
    secret = "test-secret"

    signature = "invalid_signature"
    assert not verify_signature(payload, timestamp, signature, secret)


def test_verify_signature_expired() -> None:
    """Test signature verification with expired timestamp."""
    payload = "test payload"
    old_timestamp = str(time.time() - 400)  # 400 seconds ago (> 300s limit)
    secret = "test-secret"

    signature = generate_signature(payload, old_timestamp, secret)
    assert not verify_signature(payload, old_timestamp, signature, secret)


def test_verify_signature_future() -> None:
    """Test signature verification with future timestamp."""
    payload = "test payload"
    future_timestamp = str(time.time() + 400)  # 400 seconds in future
    secret = "test-secret"

    signature = generate_signature(payload, future_timestamp, secret)
    assert not verify_signature(payload, future_timestamp, signature, secret)


def test_verify_signature_wrong_secret() -> None:
    """Test signature verification with wrong secret."""
    payload = "test payload"
    timestamp = str(time.time())

    signature = generate_signature(payload, timestamp, "secret1")
    assert not verify_signature(payload, timestamp, signature, "secret2")


def test_create_signed_headers() -> None:
    """Test creating signed headers."""
    payload = "test payload"
    headers = create_signed_headers(payload)

    assert "X-S2R-Timestamp" in headers
    assert "X-S2R-Signature" in headers
    assert "Content-Type" in headers
    assert headers["Content-Type"] == "text/plain"

    # Verify the signature is valid
    assert verify_signature(
        payload,
        headers["X-S2R-Timestamp"],
        headers["X-S2R-Signature"]
    )
