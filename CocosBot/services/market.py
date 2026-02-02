import time
from typing import Optional, Dict, Any, Union
from CocosBot.config.urls import WEB_APP_URLS, API_URLS
from CocosBot.config.enums import OrderOperation, MarketType
from CocosBot.config.selectors import (
    OPERATION_SELECTORS,
    COMMON_SELECTORS,
    LIST_SELECTORS,
    ORDER_SELECTORS
)
from CocosBot.utils.validators import validate_order_params, validate_market_type

import logging
logger = logging.getLogger(__name__)


class MarketService:
    """Servicio para manejar operaciones de mercado en Cocos Capital."""

    def __init__(self, browser):
        self.browser = browser

    def create_order(self, ticker: str, operation: Union[str, OrderOperation], amount: float,
                     limit: Optional[float] = None) -> bool:
        """
        Crea una orden de compra o venta para un ticker específico.

        Args:
            ticker: Símbolo del ticker.
            operation: Tipo de operación (BUY o SELL).
            amount: Monto a invertir o cantidad de acciones.
            limit: Precio límite para la orden (opcional).

        Returns:
            bool: True si la orden se creó exitosamente.

        Raises:
            OrderCreationError: Si hay un error al crear la orden.
        """
        try:
            # Validar parámetros
            operation_str = operation.value if isinstance(operation, OrderOperation) else operation
            operation_str, ticker = validate_order_params(ticker, operation_str, amount, limit)

            # Convertir valores al formato local
            formatted_amount = str(amount).replace('.', ',')
            formatted_limit = str(limit).replace('.', ',') if limit is not None else None

            # Navegar a la página
            self.browser.go_to(WEB_APP_URLS["market_stocks"])

            # Buscar y seleccionar el ticker
            self.browser.search_and_select(
                search_input_selector=COMMON_SELECTORS["search_input"],
                search_term=ticker,
                list_item_selector=LIST_SELECTORS["list_item"](ticker),
                log_message=f"Seleccionando el ticker '{ticker}' de la lista."
            )

            # Expandir pantalla
            self.browser.click_element(OPERATION_SELECTORS["general"]["expand_windows"], "Expandiendo pantalla.")

            # Configurar la operación
            self._configure_operation(operation_str)

            # Configurar límite si existe
            if formatted_limit:
                self._configure_limit_order(formatted_limit)

            # Ingresar monto o cantidad
            self._enter_amount(operation_str, formatted_amount)

            # Confirmar la operación
            self.confirm_operation()

            logger.info(f"Orden de {operation_str} creada exitosamente para {ticker}")
            return True

        except Exception as e:
            logger.error(f"Error creando la orden: {str(e)}")
            raise OrderCreationError(f"Error al crear la orden: {str(e)}")

    def get_ticker_info(self, ticker: str, ticker_type: Union[str, MarketType], segment: str = "C") -> Optional[
        Dict[str, Any]]:
        """
        Obtiene la información de un ticker.

        Args:
            ticker: Símbolo del ticker.
            ticker_type: Tipo de mercado como cadena o instancia de MarketType.
            segment: Segmento del mercado. Por defecto, "C".

        Returns:
            Optional[Dict[str, Any]]: Información del ticker, o None si falla.
        """
        # Validar y convertir ticker_type
        ticker_type_enum = validate_market_type(ticker_type)

        navigation_url = self._get_navigation_ticker_url(ticker_type_enum)
        if not navigation_url:
            return None

        request_url = f"{API_URLS['markets_tickers']}/{ticker}?segment={segment}"

        try:
            self.browser.go_to(navigation_url)
            self.browser.search_and_select(
                COMMON_SELECTORS["search_input"],
                ticker,
                LIST_SELECTORS["list_item"](ticker),
                f"Seleccionando el ticker '{ticker}' de la lista."
            )

            with self.browser.page.expect_response(request_url) as response_info:
                logger.info(f"Esperando la respuesta de {request_url}...")
                response = response_info.value

            return self.browser.process_response(response, f"Información del ticker {ticker} obtenida con éxito.")
        except Exception as e:
            logger.error(f"Error al obtener información del ticker {ticker}: {e}")
            return None

    def get_market_schedule(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene los horarios de apertura y cierre del mercado.
        
        Returns:
            Optional[Dict[str, Any]]: Información de horarios del mercado o None si falla.
        """
        return self.browser.fetch_data(
            request_url=API_URLS["markets_schedule"],
            navigation_url=WEB_APP_URLS["dashboard"]
        )

    def get_orders(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene todas las órdenes del usuario (pendientes y ejecutadas).
        
        Returns:
            Optional[Dict[str, Any]]: Información de órdenes o None si no hay órdenes/error.
        """
        orders = self.browser.fetch_data(
            request_url=API_URLS["orders"],
            navigation_url=WEB_APP_URLS["orders"]
        )
        if orders is None:
            logger.info("No hay órdenes pendientes.")
        return orders

    def cancel_order(self, amount: float, quantity: int) -> bool:
        """
        Cancela una orden en el mercado basada en el monto y la cantidad.

        Args:
            amount (float): Monto de la orden a cancelar.
            quantity (int): Cantidad de acciones de la orden a cancelar.

        Returns:
            bool: True si la orden fue cancelada exitosamente.

        Raises:
            Exception: Si ocurre algún error durante el proceso.
        """
        try:
            # Navegar a la página de órdenes
            self.browser.go_to(WEB_APP_URLS["orders"])

            # Convertir valores al formato local
            formatted_amount = f"AR${str(amount).replace('.', ',')}"
            formatted_quantity = str(quantity)

            # Buscar la orden en la tabla
            order_selector = (
                f"div._rowContainer_1m8d2_23:has(span:text-is('{formatted_amount}')) "
                f":has(span:text-is('{formatted_quantity}'))"
            )
            self.browser.wait_for_element(order_selector)
            self.browser.click_element(order_selector, "Seleccionando la orden en la tabla.")

            # Confirmar cancelación
            cancel_button_selector = COMMON_SELECTORS["cancel_button"]
            self.browser.click_element(cancel_button_selector, "Clic en el botón 'Cancelar orden'.")

            logger.info(f"Orden con monto {amount} y cantidad {quantity} cancelada exitosamente.")
            return True

        except Exception as e:
            logger.error(f"Error al cancelar la orden: {e}")
            return False

    def get_mep_value(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene el valor actual del dólar MEP (Mercado Electrónico de Pagos).
        
        Returns:
            Optional[Dict[str, Any]]: Información del valor MEP o None si falla.
        """
        return self.browser.fetch_data(
            API_URLS["mep_prices"],
            WEB_APP_URLS["portfolio"]
        )

    def _get_navigation_ticker_url(self, ticker_type: MarketType) -> Optional[str]:
        """
        Obtiene la URL de navegación para un tipo de ticker específico.
        
        Args:
            ticker_type: Tipo de mercado (STOCKS, CEDEARS, BONDS, etc.).
            
        Returns:
            Optional[str]: URL de navegación o None si el tipo es desconocido.
        """
        # Convertir siempre el tipo de ticker a minúsculas para la comparación
        ticker_type_str = ticker_type.value.lower()

        # Diccionario con claves en minúsculas
        market_navigation_urls = {
            MarketType.BONDS_CORP.value.lower(): WEB_APP_URLS["market_bonds_corp"],
            MarketType.BONDS_PUBLIC.value.lower(): WEB_APP_URLS["market_bonds_public"],
            MarketType.STOCKS.value.lower(): WEB_APP_URLS["market_stocks"],
            MarketType.CEDEARS.value.lower(): WEB_APP_URLS["market_cedears"],
            MarketType.LETTERS.value.lower(): WEB_APP_URLS["market_letters"],
            MarketType.CAUCION.value.lower(): WEB_APP_URLS["market_caucion"],
            MarketType.FCI.value.lower(): WEB_APP_URLS["market_fci"]
        }

        # Buscar la URL correspondiente
        navigation_url = market_navigation_urls.get(ticker_type_str)
        if not navigation_url:
            logger.error(f"Tipo de ticker desconocido: {ticker_type_str}")
            return None
        return navigation_url

    def _configure_operation(self, operation: str) -> None:
        """
        Configura el tipo de operación (compra/venta) en la interfaz.
        
        Args:
            operation: Tipo de operación ('BUY' o 'SELL').
        """
        op_config = OPERATION_SELECTORS[operation]
        self.browser.click_element(
            op_config["button"],
            f"Seleccionando la operación: {op_config['message']}."
        )

    def _configure_limit_order(self, limit: str) -> None:
        """
        Configura una orden límite con el precio especificado.
        
        Args:
            limit: Precio límite formateado (con coma decimal).
        """
        time.sleep(3) #No me gusta el tiempo explicito, pero no aparece clickeable rápido.
        self.browser.click_element(
            OPERATION_SELECTORS["general"]["more_options"],
            "Expandiendo opciones adicionales."
        )

        self.browser.click_element(
            OPERATION_SELECTORS["general"]["limit_button"],
            "Seleccionando orden límite."
        )

        self.browser.fill_input_with_delay(
            OPERATION_SELECTORS["general"]["limit_input"],
            limit,
            f"Ingresando precio límite: {limit}"
        )

    def _enter_amount(self, operation: str, amount: str) -> None:
        """
        Ingresa el monto (compra) o cantidad (venta) de la operación.
        
        Args:
            operation: Tipo de operación ('BUY' o 'SELL').
            amount: Monto o cantidad formateado.
        """
        op_config = OPERATION_SELECTORS[operation]
        amount_input = op_config["amount_input"]

        self.browser.click_element(
            amount_input,
            "Seleccionando el campo de entrada para el monto o cantidad."
        )

        self.browser.fill_input(
            amount_input,
            str(amount),
            f"Ingresando {'monto' if operation == OrderOperation.BUY.value else 'cantidad'}: {amount}"
        )

    def confirm_operation(self) -> None:
        """
        Confirma la operación haciendo clic en los botones de 'Revisar' y 'Confirmar'.
        """
        try:
            # Hacer clic en el botón "Revisar Compra"
            self.browser.click_element(
                OPERATION_SELECTORS["confirm_buttons"]["review_buy"],
                "Haciendo clic en 'Revisar'."
            )

            # Hacer clic en el botón "Confirmar"
            self.browser.click_element(
                OPERATION_SELECTORS["confirm_buttons"]["confirm"],
                "Haciendo clic en 'Confirmar'."
            )

            time.sleep(4)
            logger.info("Operación confirmada exitosamente.")
        except Exception as e:
            logger.error(f"Error al confirmar la operación: {e}")
            raise OrderCreationError(f"Error al confirmar la operación: {e}")


class OrderCreationError(Exception):
    """Error en la creación de una orden."""
    pass