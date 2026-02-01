"""
Tests for CocosBot general config module.
"""
from CocosBot.config import general


class TestGeneralConfig:
    """Tests for general configuration constants."""

    def test_default_timeout_exists(self):
        """Test that DEFAULT_TIMEOUT is defined."""
        assert hasattr(general, 'DEFAULT_TIMEOUT')
        assert isinstance(general.DEFAULT_TIMEOUT, int)
        assert general.DEFAULT_TIMEOUT > 0

    def test_max_retries_exists(self):
        """Test that MAX_RETRIES is defined."""
        assert hasattr(general, 'MAX_RETRIES')
        assert isinstance(general.MAX_RETRIES, int)
        assert general.MAX_RETRIES > 0

    def test_retry_delay_exists(self):
        """Test that RETRY_DELAY is defined."""
        assert hasattr(general, 'RETRY_DELAY')
        assert isinstance(general.RETRY_DELAY, int)
        assert general.RETRY_DELAY > 0

    def test_default_timeout_value(self):
        """Test DEFAULT_TIMEOUT has expected value."""
        assert general.DEFAULT_TIMEOUT == 10000

    def test_max_retries_value(self):
        """Test MAX_RETRIES has expected value."""
        assert general.MAX_RETRIES == 3

    def test_retry_delay_value(self):
        """Test RETRY_DELAY has expected value."""
        assert general.RETRY_DELAY == 1000
