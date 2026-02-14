"""Shared fixtures for CocosBot tests."""
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_browser():
    """Create a mock browser instance with page and locator support.

    This is the most complete version of the mock browser,
    compatible with all service tests (auth, market, user).
    """
    browser = Mock()
    browser.page = Mock()
    browser.page.locator = Mock(return_value=Mock())
    return browser


@pytest.fixture
def mock_playwright():
    """Create a mock for the sync_playwright().start() chain.

    Returns a tuple of (mock_playwright_cm, mock_browser_instance, mock_page)
    for use in browser.py tests.
    """
    mock_page = Mock()
    mock_browser_instance = Mock()
    mock_browser_instance.new_page.return_value = mock_page

    mock_chromium = Mock()
    mock_chromium.launch.return_value = mock_browser_instance

    mock_pw = Mock()
    mock_pw.chromium = mock_chromium

    mock_sync_pw = Mock()
    mock_sync_pw.return_value.start.return_value = mock_pw

    return mock_sync_pw, mock_pw, mock_browser_instance, mock_page
