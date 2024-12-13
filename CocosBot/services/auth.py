from CocosBot.utils.gmail_2fa import obtener_codigo_2FA
from CocosBot.config.urls import WEB_APP_URLS
from CocosBot.config.selectors import LOGIN_SELECTORS
from CocosBot.config.general import DEFAULT_TIMEOUT

import logging
logger = logging.getLogger(__name__)


class AuthService:
    """Servicio para manejar la autenticación en Cocos Capital."""

    def __init__(self, browser):
        """
        Inicializa el servicio de autenticación.

        Args:
            browser: Instancia de PlaywrightBrowser
        """
        self.browser = browser

    def login(self, username: str, password: str, gmail_user: str, gmail_app_pass: str) -> bool:
        """
        Realiza el login en Cocos Capital.

        Args:
            username: Email del usuario
            password: Contraseña del usuario
            gmail_user: Usuario de Gmail para 2FA
            gmail_app_pass: Contraseña de aplicación de Gmail para 2FA

        Returns:
            bool: True si el login fue exitoso

        Raises:
            AuthenticationError: Si hay un error durante el proceso de login
        """
        try:
            self.browser.go_to(WEB_APP_URLS["login"])
            self.browser.fill_input(
                LOGIN_SELECTORS["email_input"],
                username,
                "Llenando el email..."
            )
            self.browser.fill_input(
                LOGIN_SELECTORS["password_input"],
                password,
                "Llenando la contraseña..."
            )
            self.browser.click_element(
                LOGIN_SELECTORS["submit_button"],
                "Enviando formulario de login..."
            )

            self._handle_two_factor_authentication(gmail_user, gmail_app_pass)
            self._handle_save_device_prompt()

            logger.info("Login exitoso.")
            return True

        except Exception as e:
            logger.error("Error durante el proceso de login: %s", e)
            self.browser.close_browser()
            raise AuthenticationError(f"Error en el proceso de login: {str(e)}")

    def _handle_two_factor_authentication(self, gmail_user: str, gmail_app_pass: str) -> None:
        """
        Maneja la autenticación de dos factores.

        Args:
            gmail_user: Usuario de Gmail
            gmail_app_pass: Contraseña de aplicación de Gmail

        Raises:
            TwoFactorError: Si hay un error con el código 2FA
        """
        self.browser.wait_for_element(
            LOGIN_SELECTORS["two_factor_container"],
            log_message="Esperando pantalla de autenticación de dos factores.",
            timeout=DEFAULT_TIMEOUT
        )

        code = obtener_codigo_2FA(gmail_user, gmail_app_pass, 'no-reply@cocos.capital')
        if not code or len(code) != 6:
            logger.error("No se pudo obtener un código 2FA válido.")
            raise TwoFactorError("No se pudo obtener un código 2FA válido.")

        logger.info("Código 2FA obtenido: %s", code)

        for i, digit in enumerate(code):
            self.browser.fill_input(
                f'input#input{i}',
                digit,
                f"Ingresando dígito {i + 1} del código 2FA..."
            )

        logger.info("Código 2FA ingresado automáticamente.")

    def _handle_save_device_prompt(self) -> None:
        """Maneja la pantalla de guardar el dispositivo como seguro."""
        try:
            self.browser.click_element(
                LOGIN_SELECTORS["save_device_button"],
                log_message="Guardando dispositivo como seguro...",
                timeout=5000
            )
        except Exception:
            logger.warning("No apareció la pantalla de guardar dispositivo.")

    def logout(self) -> bool:
        """
        Realiza el logout de Cocos Capital.

        Returns:
            bool: True si el logout fue exitoso
        """
        try:
            self.browser.go_to(WEB_APP_URLS["dashboard"])
            self.browser.click_element(
                LOGIN_SELECTORS["logout_button"],
                "Haciendo clic en el botón de logout..."
            )
            self.browser.wait_for_element(
                LOGIN_SELECTORS["email_input"],
                log_message="Confirmando logout exitoso..."
            )

            logger.info("Logout realizado con éxito.")
            return True

        except Exception as e:
            logger.error(f"Error durante el proceso de logout: {e}")
            return False


class AuthenticationError(Exception):
    """Error en el proceso de autenticación."""
    pass


class TwoFactorError(AuthenticationError):
    """Error específico para problemas con 2FA."""
    pass