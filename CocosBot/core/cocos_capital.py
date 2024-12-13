from CocosBot.core.browser import PlaywrightBrowser
from typing import Optional, Dict, Any, Union
from CocosBot.config.enums import Currency
from CocosBot.config.enums import OrderOperation, MarketType
from CocosBot.services.auth import AuthService
from CocosBot.services.market import MarketService
from CocosBot.services.user import UserService
from CocosBot.utils.validators import validate_credentials

import logging
logger = logging.getLogger(__name__)


class CocosCapital(PlaywrightBrowser):
    """
    Cliente principal para interactuar con Cocos Capital.

    Esta clase proporciona una interfaz unificada para todas las operaciones
    disponibles en Cocos Capital, delegando las funcionalidades específicas
    a servicios especializados.

    Example:
        cocos = CocosCapital("user@example.com", "password", "gmail_user", "gmail_pass")
        if cocos.login():
            user_data = cocos.get_user_data()
            print(user_data)
            cocos.logout()
    """
    def __init__(self, username, password, gmail_user, gmail_app_pass, headless=False):
        super().__init__(headless)
        validate_credentials([username, password, gmail_user, gmail_app_pass])
        self.auth = AuthService(self)
        self.market = MarketService(self)
        self.user = UserService(self)
        self.username = username
        self.password = password
        self.gmail_user = gmail_user
        self.gmail_app_pass = gmail_app_pass

    # Métodos de Autenticación
    def login(self) -> bool:
        """Realiza el login usando el servicio de autenticación."""
        return self.auth.login(self.username, self.password, self.gmail_user, self.gmail_app_pass)

    def logout(self) -> bool:
        """Realiza el logout usando el servicio de autenticación."""
        return self.auth.logout()

    # Métodos de Usuario y Cuenta
    def get_user_data(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos del usuario."""
        return self.user.get_user_data()

    def get_account_tier(self) -> Optional[Dict[str, Any]]:
        """Obtiene el nivel de cuenta del usuario."""
        return self.user.get_account_tier()

    def get_portfolio_data(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos del portafolio del usuario."""
        return self.user.get_portfolio_data()

    def fetch_portfolio_balance(self) -> Optional[float]:
        """Obtiene el balance total del portafolio."""
        return self.user.get_portfolio_balance()

    def get_linked_accounts(self, amount: float = 5000, currency: Currency = Currency.ARS) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de las cuentas vinculadas del usuario.

        Args:
            amount: Monto a ingresar para la extracción
            currency: Moneda seleccionada ("ARS" o "USD")

        Returns:
            Optional[Dict[str, Any]]: Información de las cuentas vinculadas o None si hay error
        """
        return self.user.get_linked_accounts(amount, currency)

    def get_academy_data(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos de la sección de Academia desde la API."""
        return self.user.get_academy_data()

    # Métodos de Mercado y Operaciones
    def create_order(self, ticker: str, operation: Union[str, OrderOperation], amount: float,
                    limit: Optional[float] = None) -> bool:
        """Crea una orden usando el servicio de mercado."""
        return self.market.create_order(ticker, operation, amount, limit)

    def get_ticker_info(self, ticker: str, ticker_type: Union[str, MarketType], segment: str = "C") -> Optional[Dict[str, Any]]:
        """Obtiene la información de un ticker."""
        return self.market.get_ticker_info(ticker, ticker_type, segment)

    def get_market_schedule(self) -> Optional[Dict[str, Any]]:
        """Obtiene los horarios del mercado."""
        return self.market.get_market_schedule()

    def get_orders(self) -> Optional[Dict[str, Any]]:
        """Obtiene las órdenes del usuario desde la API."""
        return self.market.get_orders()

    def cancel_order(self, amount: float, quantity: int) -> bool:
        """Cancela una orden usando el servicio de mercado."""
        return self.market.cancel_order(amount, quantity)

    def get_mep_value(self) -> Optional[Dict[str, Any]]:
        """Obtiene el valor DOLAR MEP."""
        return self.market.get_mep_value()