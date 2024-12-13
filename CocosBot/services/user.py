from typing import Optional, Dict, Any
from CocosBot.config.urls import WEB_APP_URLS, API_URLS
from CocosBot.config.enums import Currency
from CocosBot.config.selectors import TRANSFER_SELECTORS

import logging
logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, browser):
        self.browser = browser

    def get_user_data(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos del usuario."""
        return self.browser.fetch_data(
            API_URLS["user_data"],
            WEB_APP_URLS["dashboard"]
        )

    def get_account_tier(self) -> Optional[Dict[str, Any]]:
        """Obtiene el nivel de cuenta del usuario."""
        return self.browser.fetch_data(
            request_url=API_URLS["account_tier"],
            navigation_url=WEB_APP_URLS["dashboard"]
        )

    def navigate_withdraw_form(self, amount: float, currency: Currency = Currency.ARS) -> bool:
        """
        Navega al formulario de extracción y lo completa sin clickear el botón final.
        Este método es común para ver cuentas y realizar extracciones.

        Args:
            amount: Monto a extraer
            currency: Moneda seleccionada ("ARS" o "USD")

        Returns:
            bool: True si la navegación fue exitosa
        """
        try:
            # Click en el botón de extraer
            self.browser.click_element(
                TRANSFER_SELECTORS["withdraw_button"],
                "Navegando al apartado de extraer desde el dashboard."
            )

            # Resto del código usando currency_enum
            if currency == Currency.ARS:
                self.browser.click_element(
                    TRANSFER_SELECTORS["currency_ars"],
                    "Seleccionando moneda ARS."
                )
            elif currency == Currency.USD:
                self.browser.click_element(
                    TRANSFER_SELECTORS["currency_usd"],
                    "Seleccionando moneda USD."
                )
            else:
                raise ValueError("Moneda no soportada. Use 'ARS' o 'USD'.")

            # Ingresar monto
            self.browser.fill_input(
                TRANSFER_SELECTORS["amount_input"],
                str(amount),
                f"Ingresando monto {amount}"
            )

            # Simular blur para validaciones
            self.browser.page.locator(TRANSFER_SELECTORS["amount_input"]).evaluate("el => el.blur()")

            # Esperar que el botón "Continuar" esté habilitado
            self.browser.wait_for_element(
                TRANSFER_SELECTORS["continue_button"],
                "Esperando que el botón 'Continuar' habilitado sea visible dentro del contenedor 'Extraé dinero'."
            )

            return True

        except Exception as e:
            logger.error(f"Error navegando al formulario de extracción: {e}")
            return False

    def get_linked_accounts(self, amount: float = 5000, currency: Currency = Currency.ARS) -> Optional[Dict[str, Any]]:
        """Obtiene las cuentas vinculadas disponibles."""
        try:
            # Llamar a navigate_withdraw_form
            if not self.navigate_withdraw_form(amount, currency):
                return None

            # Configurar la intercepción y procesar la respuesta usando process_response
            with self.browser.page.expect_response(f'{API_URLS["user_accounts"]}{currency.value}') as response_info:
                self.browser.click_element(
                    'button:has-text("Continuar")',
                    "Click en el botón 'Continuar'."
                )
                logger.info("Esperando respuesta para obtener cuentas disponibles...")
                response = response_info.value
                return self.browser.process_response(response, "Cuentas disponibles obtenidas con éxito.")

        except Exception as e:
            logger.error(f"Error obteniendo cuentas vinculadas: {e}")
            return None

    def get_portfolio_data(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos del portafolio del usuario."""
        return self.browser.fetch_data(
            request_url=API_URLS["portfolio_data"],
            navigation_url=WEB_APP_URLS["portfolio"]
        )

    def get_portfolio_balance(self) -> Optional[float]:
        """Obtiene el balance total del portafolio del usuario."""

        def process_response(response):
            total_balance = response.get('totalBalance')
            if total_balance is not None:
                logger.info("Total Balance obtenido con éxito: %s", total_balance)
            else:
                logger.warning("El campo 'totalBalance' no está presente en la respuesta.")
            return total_balance

        return self.browser.fetch_data(
            API_URLS["portfolio_balance"],
            WEB_APP_URLS["portfolio"],
            process_response
        )

    def get_academy_data(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos de la sección de Academia."""
        return self.browser.fetch_data(
            request_url=API_URLS["academy"],
            navigation_url=WEB_APP_URLS["dashboard"]
        )