"""Tests for converter module."""

import pytest

from s2r.converter import convert_slurm_to_runai, ConversionError


def test_convert_empty_script() -> None:
    """Test conversion fails with empty script."""
    with pytest.raises(ConversionError, match="cannot be empty"):
        convert_slurm_to_runai("")


def test_convert_whitespace_only() -> None:
    """Test conversion fails with whitespace-only script."""
    with pytest.raises(ConversionError, match="cannot be empty"):
        convert_slurm_to_runai("   \n  \t  ")


def test_conversion_error_message() -> None:
    """Test ConversionError can be raised with custom message."""
    try:
        raise ConversionError("Custom error message")
    except ConversionError as e:
        assert str(e) == "Custom error message"


# Note: Full integration tests would require a running Lambda endpoint
# These tests cover the basic validation logic
