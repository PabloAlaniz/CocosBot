"""Tests for CocosBot.core.browser"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from CocosBot.core.browser import PlaywrightBrowser


@patch('CocosBot.core.browser.sync_playwright')
class TestInit:
    """Tests for PlaywrightBrowser.__init__"""

    def test_init_headless_false(self, mock_sync_pw):
        mock_pw = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        mock_sync_pw.return_value.start.return_value = mock_pw

        browser = PlaywrightBrowser(headless=False)

        mock_pw.chromium.launch.assert_called_once_with(headless=False)
        mock_browser.new_page.assert_called_once()
        assert browser.page == mock_page

    def test_init_headless_true(self, mock_sync_pw):
        mock_pw = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        mock_sync_pw.return_value.start.return_value = mock_pw

        browser = PlaywrightBrowser(headless=True)

        mock_pw.chromium.launch.assert_called_once_with(headless=True)


@patch('CocosBot.core.browser.sync_playwright')
class TestContextManager:
    """Tests for __enter__ and __exit__"""

    def test_enter_returns_self(self, mock_sync_pw):
        mock_pw = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=Mock()))
        mock_sync_pw.return_value.start.return_value = mock_pw

        browser = PlaywrightBrowser()
        result = browser.__enter__()

        assert result is browser

    def test_exit_calls_close_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=Mock()))
        mock_sync_pw.return_value.start.return_value = mock_pw

        browser = PlaywrightBrowser()
        browser.__exit__(None, None, None)

        browser.browser.close.assert_called_once()
        mock_pw.stop.assert_called_once()


@patch('CocosBot.core.browser.sync_playwright')
class TestCloseBrowser:
    """Tests for close_browser"""

    def test_close_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_browser_inst = Mock()
        mock_pw.chromium.launch.return_value = mock_browser_inst
        mock_browser_inst.new_page.return_value = Mock()
        mock_sync_pw.return_value.start.return_value = mock_pw

        browser = PlaywrightBrowser()
        browser.close_browser()

        mock_browser_inst.close.assert_called_once()
        mock_pw.stop.assert_called_once()

    def test_close_browser_idempotent(self, mock_sync_pw):
        mock_pw = Mock()
        mock_browser_inst = Mock()
        mock_pw.chromium.launch.return_value = mock_browser_inst
        mock_browser_inst.new_page.return_value = Mock()
        mock_sync_pw.return_value.start.return_value = mock_pw

        browser = PlaywrightBrowser()
        browser.close_browser()
        browser.close_browser()

        # Should only be called once due to _closed flag
        mock_browser_inst.close.assert_called_once()
        mock_pw.stop.assert_called_once()


@patch('CocosBot.core.browser.sync_playwright')
class TestGoTo:
    """Tests for go_to"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_go_to(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.go_to("https://example.com")

        mock_page.goto.assert_called_once_with("https://example.com")

    def test_go_to_with_log_message(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.go_to("https://example.com", log_message="Navigating")

        mock_page.goto.assert_called_once_with("https://example.com")


@patch('CocosBot.core.browser.sync_playwright')
class TestWaitForElement:
    """Tests for wait_for_element"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_wait_for_element_default_timeout(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.wait_for_element("div.test")

        from CocosBot.config.general import DEFAULT_TIMEOUT
        mock_page.wait_for_selector.assert_called_once_with(
            "div.test", timeout=DEFAULT_TIMEOUT, state="visible"
        )

    def test_wait_for_element_custom_timeout(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.wait_for_element("div.test", timeout=5000)

        mock_page.wait_for_selector.assert_called_once_with(
            "div.test", timeout=5000, state="visible"
        )


@patch('CocosBot.core.browser.sync_playwright')
class TestClickElement:
    """Tests for click_element"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_click_element(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.click_element("button.submit")

        mock_page.wait_for_selector.assert_called_once()
        mock_page.click.assert_called_once_with("button.submit")

    def test_click_element_with_timeout(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.click_element("button.submit", timeout=3000)

        mock_page.wait_for_selector.assert_called_once()
        mock_page.click.assert_called_once_with("button.submit")


@patch('CocosBot.core.browser.sync_playwright')
class TestFillInput:
    """Tests for fill_input"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_fill_input(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.fill_input("input#email", "test@example.com")

        mock_page.wait_for_selector.assert_called_once()
        mock_page.fill.assert_called_once_with("input#email", "test@example.com")

    def test_fill_input_with_timeout(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.fill_input("input#email", "test@example.com", timeout=2000)

        mock_page.wait_for_selector.assert_called_once()
        mock_page.fill.assert_called_once_with("input#email", "test@example.com")


@patch('CocosBot.core.browser.sync_playwright')
class TestFillInputWithEvents:
    """Tests for fill_input_with_events"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_fill_input_with_events(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.fill_input_with_events("input#amount", "1000")

        mock_page.fill.assert_called_once_with("input#amount", "1000")
        mock_page.keyboard.press.assert_called_once_with("Enter")
        mock_page.locator.assert_called_once_with("input#amount")
        mock_page.locator.return_value.evaluate.assert_called_once_with("el => el.blur()")

    def test_fill_input_with_events_and_log(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.fill_input_with_events("input#amount", "500", log_message="Filling amount")

        mock_page.fill.assert_called_once_with("input#amount", "500")
        mock_page.keyboard.press.assert_called_once_with("Enter")


@patch('CocosBot.core.browser.sync_playwright')
class TestFillInputWithDelay:
    """Tests for fill_input_with_delay"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_locator = Mock()
        mock_page.locator.return_value = mock_locator
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page, mock_locator

    @patch('CocosBot.core.browser.time.sleep')
    def test_fill_input_with_delay(self, mock_sleep, mock_sync_pw):
        browser, mock_page, mock_locator = self._make_browser(mock_sync_pw)
        browser.fill_input_with_delay("input#price", "123", delay=0.1)

        # Should clear the input first
        mock_locator.fill.assert_called_once_with("")
        # Should type each character
        assert mock_locator.type.call_count == 3
        mock_locator.type.assert_any_call("1")
        mock_locator.type.assert_any_call("2")
        mock_locator.type.assert_any_call("3")
        assert mock_sleep.call_count == 3

    @patch('CocosBot.core.browser.time.sleep')
    def test_fill_input_with_delay_clears_first(self, mock_sleep, mock_sync_pw):
        browser, mock_page, mock_locator = self._make_browser(mock_sync_pw)
        browser.fill_input_with_delay("input#price", "ab")

        mock_locator.fill.assert_called_once_with("")
        assert mock_locator.type.call_count == 2

    @patch('CocosBot.core.browser.time.sleep')
    def test_fill_input_with_delay_with_log_message(self, mock_sleep, mock_sync_pw):
        browser, mock_page, mock_locator = self._make_browser(mock_sync_pw)
        browser.fill_input_with_delay("input#price", "5", log_message="Filling price")

        mock_locator.fill.assert_called_once_with("")
        mock_locator.type.assert_called_once_with("5")


@patch('CocosBot.core.browser.sync_playwright')
class TestGetTextContent:
    """Tests for get_text_content"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_get_text_content(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_page.text_content.return_value = "Hello World"

        result = browser.get_text_content("span.title")

        assert result == "Hello World"
        mock_page.text_content.assert_called_once_with("span.title")

    def test_get_text_content_waits(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_page.text_content.return_value = "Content"

        browser.get_text_content("span.title", timeout=5000)

        mock_page.wait_for_selector.assert_called_once()


@patch('CocosBot.core.browser.sync_playwright')
class TestTakeScreenshot:
    """Tests for take_screenshot"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_take_screenshot_default_filename(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.take_screenshot()

        mock_page.screenshot.assert_called_once_with(path="screenshot.png")

    def test_take_screenshot_custom_filename(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        browser.take_screenshot("custom.png")

        mock_page.screenshot.assert_called_once_with(path="custom.png")


@patch('CocosBot.core.browser.sync_playwright')
class TestProcessResponse:
    """Tests for process_response"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser

    def test_process_response_success(self, mock_sync_pw):
        browser = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json.return_value = {"data": "value"}

        result = browser.process_response(mock_response, "Success!")

        assert result == {"data": "value"}

    def test_process_response_error_status(self, mock_sync_pw):
        browser = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 500

        result = browser.process_response(mock_response)

        assert result is None

    def test_process_response_json_exception(self, mock_sync_pw):
        browser = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json.side_effect = Exception("Invalid JSON")

        result = browser.process_response(mock_response)

        assert result is None


@patch('CocosBot.core.browser.sync_playwright')
class TestSearchAndSelect:
    """Tests for search_and_select"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_search_and_select(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)

        browser.search_and_select("input#search", "AAPL", "li.item-{}", "Selecting AAPL")

        # fill_input should be called for the search
        mock_page.fill.assert_called_once_with("input#search", "AAPL")
        # click should be called for the item (formatted selector)
        mock_page.click.assert_called_once_with("li.item-AAPL")

    def test_search_and_select_format(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)

        browser.search_and_select("input#search", "TSLA", "ul li[data-ticker='{}']", "Select")

        mock_page.click.assert_called_once_with("ul li[data-ticker='TSLA']")


@patch('CocosBot.core.browser.sync_playwright')
class TestFetchData:
    """Tests for fetch_data"""

    def _make_browser(self, mock_sync_pw):
        mock_pw = Mock()
        mock_page = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=mock_page))
        mock_sync_pw.return_value.start.return_value = mock_pw
        browser = PlaywrightBrowser()
        return browser, mock_page

    def test_fetch_data_happy_path(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 200
        mock_response.url = "https://api.example.com/data"
        mock_response.json.return_value = {"key": "value"}

        mock_response_info = Mock()
        mock_response_info.value = mock_response
        mock_page.expect_response.return_value.__enter__ = Mock(return_value=mock_response_info)
        mock_page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page"
        )

        assert result == {"key": "value"}
        mock_page.goto.assert_called_once()

    def test_fetch_data_with_callback(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 200
        mock_response.url = "https://api.example.com/data"
        mock_response.json.return_value = {"total": 100, "items": [1, 2]}

        mock_response_info = Mock()
        mock_response_info.value = mock_response
        mock_page.expect_response.return_value.__enter__ = Mock(return_value=mock_response_info)
        mock_page.expect_response.return_value.__exit__ = Mock(return_value=False)

        callback = lambda data: data["total"]
        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page",
            process_response=callback
        )

        assert result == 100

    def test_fetch_data_timeout(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_page.expect_response.return_value.__enter__ = Mock(side_effect=TimeoutError("Timeout"))
        mock_page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page"
        )

        assert result is None

    def test_fetch_data_handle_response_callback(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 200
        mock_response.url = "https://api.example.com/data"
        mock_response.json.return_value = {"key": "value"}

        mock_response_info = Mock()
        mock_response_info.value = mock_response
        mock_page.expect_response.return_value.__enter__ = Mock(return_value=mock_response_info)
        mock_page.expect_response.return_value.__exit__ = Mock(return_value=False)

        captured_callback = None
        def capture_on(event, callback):
            nonlocal captured_callback
            if event == "response":
                captured_callback = callback
        mock_page.on.side_effect = capture_on

        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page"
        )

        assert result == {"key": "value"}
        # Invoke the captured callback to cover handle_response lines
        assert captured_callback is not None
        cb_response = Mock()
        cb_response.url = "https://api.example.com/data?page=1"
        cb_response.status = 200
        cb_result = captured_callback(cb_response)
        assert cb_result == cb_response

    def test_fetch_data_empty_response(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json.return_value = {}

        mock_response_info = Mock()
        mock_response_info.value = mock_response
        mock_page.expect_response.return_value.__enter__ = Mock(return_value=mock_response_info)
        mock_page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page"
        )

        assert result is None

    def test_fetch_data_json_decode_error(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json.side_effect = Exception("Invalid JSON")

        mock_response_info = Mock()
        mock_response_info.value = mock_response
        mock_page.expect_response.return_value.__enter__ = Mock(return_value=mock_response_info)
        mock_page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page"
        )

        assert result is None

    def test_fetch_data_non_200_status(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_response = Mock()
        mock_response.status = 500

        mock_response_info = Mock()
        mock_response_info.value = mock_response
        mock_page.expect_response.return_value.__enter__ = Mock(return_value=mock_response_info)
        mock_page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page"
        )

        assert result is None

    def test_fetch_data_exception(self, mock_sync_pw):
        browser, mock_page = self._make_browser(mock_sync_pw)
        mock_page.goto.side_effect = Exception("Network error")

        result = browser.fetch_data(
            "https://api.example.com/data",
            "https://example.com/page"
        )

        assert result is None
