"""Tests for CocosBot.services.auth"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from CocosBot.services.auth import AuthService, AuthenticationError, TwoFactorError


class TestAuthService:
    """Tests for AuthService class"""

    @pytest.fixture
    def mock_browser(self):
        """Create a mock browser instance"""
        browser = Mock()
        return browser

    @pytest.fixture
    def auth_service(self, mock_browser):
        """Create an AuthService instance with mock browser"""
        return AuthService(mock_browser)

    def test_init(self, mock_browser):
        """Test AuthService initialization"""
        service = AuthService(mock_browser)
        assert service.browser == mock_browser

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_login_success(self, mock_get_2fa, auth_service, mock_browser):
        """Test successful login flow"""
        # Setup
        mock_get_2fa.return_value = "123456"
        
        # Execute
        result = auth_service.login(
            username="test@example.com",
            password="password123",
            gmail_user="gmail@example.com",
            gmail_app_pass="app_pass"
        )

        # Assert
        assert result is True
        mock_browser.go_to.assert_called_once()
        assert mock_browser.fill_input.call_count == 8  # 2 for login + 6 for 2FA digits
        mock_browser.click_element.assert_called()
        mock_browser.wait_for_element.assert_called()

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_login_invalid_2fa_code(self, mock_get_2fa, auth_service, mock_browser):
        """Test login fails with invalid 2FA code"""
        # Setup
        mock_get_2fa.return_value = "12345"  # Invalid length

        # Execute & Assert (wrapped in AuthenticationError)
        with pytest.raises(AuthenticationError, match="Error en el proceso de login"):
            auth_service.login(
                username="test@example.com",
                password="password123",
                gmail_user="gmail@example.com",
                gmail_app_pass="app_pass"
            )

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_login_no_2fa_code(self, mock_get_2fa, auth_service, mock_browser):
        """Test login fails when no 2FA code is obtained"""
        # Setup
        mock_get_2fa.return_value = None

        # Execute & Assert (wrapped in AuthenticationError)
        with pytest.raises(AuthenticationError):
            auth_service.login(
                username="test@example.com",
                password="password123",
                gmail_user="gmail@example.com",
                gmail_app_pass="app_pass"
            )

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_login_browser_error(self, mock_get_2fa, auth_service, mock_browser):
        """Test login handles browser errors"""
        # Setup
        mock_get_2fa.return_value = "123456"
        mock_browser.go_to.side_effect = Exception("Browser error")

        # Execute & Assert
        with pytest.raises(AuthenticationError, match="Error en el proceso de login"):
            auth_service.login(
                username="test@example.com",
                password="password123",
                gmail_user="gmail@example.com",
                gmail_app_pass="app_pass"
            )
        
        mock_browser.close_browser.assert_called_once()

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_handle_two_factor_authentication(self, mock_get_2fa, auth_service, mock_browser):
        """Test 2FA handling"""
        # Setup
        mock_get_2fa.return_value = "654321"

        # Execute
        auth_service._handle_two_factor_authentication("gmail@test.com", "app_pass")

        # Assert
        mock_get_2fa.assert_called_once_with("gmail@test.com", "app_pass", "no-reply@cocos.capital")
        assert mock_browser.fill_input.call_count == 6

    def test_handle_save_device_prompt_success(self, auth_service, mock_browser):
        """Test save device prompt is handled"""
        # Execute
        auth_service._handle_save_device_prompt()

        # Assert
        mock_browser.click_element.assert_called_once()

    def test_handle_save_device_prompt_not_shown(self, auth_service, mock_browser):
        """Test save device prompt when not shown (no error)"""
        # Setup
        mock_browser.click_element.side_effect = Exception("Element not found")

        # Execute (should not raise)
        auth_service._handle_save_device_prompt()

        # Assert
        mock_browser.click_element.assert_called_once()

    @patch('CocosBot.services.auth.LOGIN_SELECTORS', {
        'logout_button': 'button.logout',
        'email_input': 'input#email'
    })
    def test_logout_success(self, auth_service, mock_browser):
        """Test successful logout"""
        # Execute
        result = auth_service.logout()

        # Assert
        assert result is True
        mock_browser.go_to.assert_called_once()
        mock_browser.click_element.assert_called_once()
        mock_browser.wait_for_element.assert_called_once()

    def test_logout_failure(self, auth_service, mock_browser):
        """Test logout handles errors"""
        # Setup
        mock_browser.go_to.side_effect = Exception("Navigation error")

        # Execute
        result = auth_service.logout()

        # Assert
        assert result is False


class TestAuthExceptions:
    """Tests for authentication exception classes"""

    def test_authentication_error_is_exception(self):
        """Test AuthenticationError is an Exception"""
        error = AuthenticationError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_two_factor_error_is_authentication_error(self):
        """Test TwoFactorError is subclass of AuthenticationError"""
        error = TwoFactorError("2FA error")
        assert isinstance(error, AuthenticationError)
        assert isinstance(error, Exception)
        assert str(error) == "2FA error"
