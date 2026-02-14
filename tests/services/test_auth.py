"""Tests for CocosBot.services.auth"""
import pytest
from unittest.mock import Mock, patch, call
from CocosBot.services.auth import AuthService, AuthenticationError, TwoFactorError
from CocosBot.config.urls import WEB_APP_URLS
from CocosBot.config.selectors import LOGIN_SELECTORS


class TestAuthService:
    """Tests for AuthService class"""

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
        mock_get_2fa.return_value = "123456"

        result = auth_service.login(
            username="test@example.com",
            password="password123",
            gmail_user="gmail@example.com",
            gmail_app_pass="app_pass"
        )

        assert result is True
        mock_browser.go_to.assert_called_once_with(WEB_APP_URLS["login"])
        mock_browser.fill_input.assert_any_call(
            LOGIN_SELECTORS["email_input"],
            "test@example.com",
            "Llenando el email..."
        )
        mock_browser.fill_input.assert_any_call(
            LOGIN_SELECTORS["password_input"],
            "password123",
            "Llenando la contraseña..."
        )
        mock_browser.click_element.assert_any_call(
            LOGIN_SELECTORS["submit_button"],
            "Enviando formulario de login..."
        )
        assert mock_browser.fill_input.call_count == 8  # 2 login + 6 digits

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_login_invalid_2fa_code(self, mock_get_2fa, auth_service, mock_browser):
        """Test login fails with invalid 2FA code"""
        mock_get_2fa.return_value = "12345"  # Invalid length

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
        mock_get_2fa.return_value = None

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
        mock_get_2fa.return_value = "123456"
        mock_browser.go_to.side_effect = Exception("Browser error")

        with pytest.raises(AuthenticationError, match="Error en el proceso de login"):
            auth_service.login(
                username="test@example.com",
                password="password123",
                gmail_user="gmail@example.com",
                gmail_app_pass="app_pass"
            )

        mock_browser.close_browser.assert_not_called()

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_handle_two_factor_authentication(self, mock_get_2fa, auth_service, mock_browser):
        """Test 2FA handling fills each digit in the correct input"""
        mock_get_2fa.return_value = "654321"

        auth_service._handle_two_factor_authentication("gmail@test.com", "app_pass")

        mock_get_2fa.assert_called_once_with("gmail@test.com", "app_pass", "no-reply@cocos.capital")
        mock_browser.wait_for_element.assert_called_once_with(
            LOGIN_SELECTORS["two_factor_container"],
            log_message="Esperando pantalla de autenticación de dos factores.",
            timeout=10000
        )
        assert mock_browser.fill_input.call_count == 6
        for i, digit in enumerate("654321"):
            mock_browser.fill_input.assert_any_call(
                f'input#input{i}',
                digit,
                f"Ingresando dígito {i + 1} del código 2FA..."
            )

    def test_handle_save_device_prompt_success(self, auth_service, mock_browser):
        """Test save device prompt clicks the correct button"""
        auth_service._handle_save_device_prompt()

        mock_browser.click_element.assert_called_once_with(
            LOGIN_SELECTORS["save_device_button"],
            log_message="Guardando dispositivo como seguro...",
            timeout=5000
        )

    def test_handle_save_device_prompt_not_shown(self, auth_service, mock_browser):
        """Test save device prompt when not shown (no error)"""
        mock_browser.click_element.side_effect = Exception("Element not found")

        auth_service._handle_save_device_prompt()

        mock_browser.click_element.assert_called_once()

    def test_logout_success(self, auth_service, mock_browser):
        """Test successful logout uses correct URL and selectors"""
        result = auth_service.logout()

        assert result is True
        mock_browser.go_to.assert_called_once_with(WEB_APP_URLS["dashboard"])
        mock_browser.click_element.assert_called_once_with(
            LOGIN_SELECTORS["logout_button"],
            "Haciendo clic en el botón de logout..."
        )
        mock_browser.wait_for_element.assert_called_once_with(
            LOGIN_SELECTORS["email_input"],
            log_message="Confirmando logout exitoso..."
        )

    def test_logout_failure(self, auth_service, mock_browser):
        """Test logout handles errors"""
        mock_browser.go_to.side_effect = Exception("Navigation error")

        result = auth_service.logout()

        assert result is False

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_login_2fa_code_too_short(self, mock_get_2fa, auth_service, mock_browser):
        """Test login fails with 2FA code that is too short (5 digits)"""
        mock_get_2fa.return_value = "12345"

        with pytest.raises(AuthenticationError):
            auth_service.login("user@test.com", "pass", "gmail@test.com", "app_pass")

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_login_2fa_code_too_long(self, mock_get_2fa, auth_service, mock_browser):
        """Test login fails with 2FA code that is too long (7 digits)"""
        mock_get_2fa.return_value = "1234567"

        with pytest.raises(AuthenticationError):
            auth_service.login("user@test.com", "pass", "gmail@test.com", "app_pass")

    @patch('CocosBot.services.auth.obtener_codigo_2FA')
    def test_handle_2fa_when_obtener_raises(self, mock_get_2fa, auth_service, mock_browser):
        """Test _handle_two_factor_authentication when obtener_codigo_2FA raises"""
        mock_get_2fa.side_effect = Exception("IMAP connection failed")

        with pytest.raises(Exception, match="IMAP connection failed"):
            auth_service._handle_two_factor_authentication("gmail@test.com", "app_pass")


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
