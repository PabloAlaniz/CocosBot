"""Tests for CocosBot.services.market"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from CocosBot.services.market import MarketService, OrderCreationError
from CocosBot.config.enums import OrderOperation, MarketType
from CocosBot.config.urls import WEB_APP_URLS, API_URLS
from CocosBot.config.selectors import (
    OPERATION_SELECTORS,
    COMMON_SELECTORS,
    LIST_SELECTORS,
    ORDER_SELECTORS,
)


class TestMarketService:
    """Tests for MarketService class"""

    @pytest.fixture
    def market_service(self, mock_browser):
        """Create a MarketService instance with mock browser"""
        return MarketService(mock_browser)

    def test_init(self, mock_browser):
        """Test MarketService initialization"""
        service = MarketService(mock_browser)
        assert service.browser == mock_browser

    def test_create_order_buy_success(self, market_service, mock_browser):
        """Test successful buy order creation with correct URL and selectors"""
        result = market_service.create_order(
            ticker="AAPL",
            operation=OrderOperation.BUY,
            amount=1000.50
        )

        assert result is True
        mock_browser.go_to.assert_called_once_with(WEB_APP_URLS["market_stocks"])
        mock_browser.search_and_select.assert_called_once_with(
            search_input_selector=COMMON_SELECTORS["search_input"],
            search_term="AAPL",
            list_item_selector=LIST_SELECTORS["list_item"]("AAPL"),
            log_message="Seleccionando el ticker 'AAPL' de la lista."
        )
        mock_browser.click_element.assert_any_call(
            OPERATION_SELECTORS["general"]["expand_windows"],
            "Expandiendo pantalla."
        )

    def test_create_order_sell_with_limit(self, market_service, mock_browser):
        """Test sell order with limit price"""
        result = market_service.create_order(
            ticker="TSLA",
            operation="SELL",
            amount=10,
            limit=250.75
        )

        assert result is True

    def test_create_order_string_operation(self, market_service, mock_browser):
        """Test order creation with string operation"""
        result = market_service.create_order(
            ticker="GOOGL",
            operation="BUY",
            amount=500
        )

        assert result is True

    def test_create_order_handles_error(self, market_service, mock_browser):
        """Test order creation error handling"""
        mock_browser.go_to.side_effect = Exception("Navigation failed")

        with pytest.raises(OrderCreationError, match="Error al crear la orden"):
            market_service.create_order(
                ticker="FAIL",
                operation=OrderOperation.BUY,
                amount=100
            )

    def test_get_ticker_info_stocks(self, market_service, mock_browser):
        """Test getting ticker info for stocks"""
        mock_browser.process_response.return_value = {"ticker": "AAPL", "price": 150}
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = market_service.get_ticker_info("AAPL", MarketType.STOCKS)

        assert result == {"ticker": "AAPL", "price": 150}
        mock_browser.go_to.assert_called_once_with(WEB_APP_URLS["market_stocks"])
        mock_browser.search_and_select.assert_called_once_with(
            COMMON_SELECTORS["search_input"],
            "AAPL",
            LIST_SELECTORS["list_item"]("AAPL"),
            "Seleccionando el ticker 'AAPL' de la lista."
        )

    def test_get_ticker_info_cedears(self, market_service, mock_browser):
        """Test getting ticker info for cedears"""
        mock_browser.process_response.return_value = {"ticker": "TSLA", "price": 200}
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = market_service.get_ticker_info("TSLA", "CEDEARS", segment="C")

        assert result == {"ticker": "TSLA", "price": 200}
        mock_browser.go_to.assert_called_once_with(WEB_APP_URLS["market_cedears"])

    def test_get_ticker_info_no_navigation_url(self, market_service, mock_browser):
        """Test get_ticker_info returns None when navigation URL is None"""
        with patch.object(market_service, '_get_navigation_ticker_url', return_value=None):
            result = market_service.get_ticker_info("AAPL", MarketType.STOCKS)

        assert result is None
        mock_browser.go_to.assert_not_called()

    def test_get_ticker_info_error(self, market_service, mock_browser):
        """Test ticker info error handling"""
        mock_browser.go_to.side_effect = Exception("Error")

        result = market_service.get_ticker_info("FAIL", MarketType.STOCKS)

        assert result is None

    def test_get_market_schedule(self, market_service, mock_browser):
        """Test getting market schedule with correct URLs"""
        expected_schedule = {"open": "10:00", "close": "17:00"}
        mock_browser.fetch_data.return_value = expected_schedule

        result = market_service.get_market_schedule()

        assert result == expected_schedule
        mock_browser.fetch_data.assert_called_once_with(
            request_url=API_URLS["markets_schedule"],
            navigation_url=WEB_APP_URLS["dashboard"]
        )

    def test_get_orders_with_orders(self, market_service, mock_browser):
        """Test getting orders when orders exist"""
        expected_orders = {"orders": [{"id": 1}, {"id": 2}]}
        mock_browser.fetch_data.return_value = expected_orders

        result = market_service.get_orders()

        assert result == expected_orders
        mock_browser.fetch_data.assert_called_once_with(
            request_url=API_URLS["orders"],
            navigation_url=WEB_APP_URLS["orders"]
        )

    def test_get_orders_no_orders(self, market_service, mock_browser):
        """Test getting orders when no orders exist"""
        mock_browser.fetch_data.return_value = None

        result = market_service.get_orders()

        assert result is None

    def test_cancel_order_success(self, market_service, mock_browser):
        """Test successful order cancellation with correct selectors"""
        result = market_service.cancel_order(amount=1000.50, quantity=10)

        assert result is True
        mock_browser.go_to.assert_called_once_with(WEB_APP_URLS["orders"])

        expected_order_selector = (
            "div._rowContainer_1m8d2_23:has(span:text-is('AR$1000,5')) "
            ":has(span:text-is('10'))"
        )
        mock_browser.wait_for_element.assert_called_once_with(expected_order_selector)
        mock_browser.click_element.assert_any_call(
            expected_order_selector,
            "Seleccionando la orden en la tabla."
        )
        mock_browser.click_element.assert_any_call(
            ORDER_SELECTORS["cancel_button"],
            "Clic en el botón 'Cancelar orden'."
        )

    def test_cancel_order_failure(self, market_service, mock_browser):
        """Test order cancellation failure"""
        mock_browser.go_to.side_effect = Exception("Error")

        result = market_service.cancel_order(amount=1000, quantity=5)

        assert result is False

    def test_get_mep_value(self, market_service, mock_browser):
        """Test getting MEP value with correct URLs"""
        expected_mep = {"buy": 350.5, "sell": 355.2}
        mock_browser.fetch_data.return_value = expected_mep

        result = market_service.get_mep_value()

        assert result == expected_mep
        mock_browser.fetch_data.assert_called_once_with(
            API_URLS["mep_prices"],
            WEB_APP_URLS["portfolio"]
        )

    def test_get_navigation_ticker_url_stocks(self, market_service):
        """Test getting navigation URL for stocks"""
        result = market_service._get_navigation_ticker_url(MarketType.STOCKS)

        assert result == WEB_APP_URLS["market_stocks"]

    def test_get_navigation_ticker_url_bonds(self, market_service):
        """Test getting navigation URL for bonds"""
        result = market_service._get_navigation_ticker_url(MarketType.BONDS_CORP)

        assert result == WEB_APP_URLS["market_bonds_corp"]

    def test_get_navigation_ticker_url_all_types(self, market_service):
        """Test all market types map to their correct URLs"""
        expected_mappings = {
            MarketType.STOCKS: WEB_APP_URLS["market_stocks"],
            MarketType.CEDEARS: WEB_APP_URLS["market_cedears"],
            MarketType.BONDS_CORP: WEB_APP_URLS["market_bonds_corp"],
            MarketType.BONDS_PUBLIC: WEB_APP_URLS["market_bonds_public"],
            MarketType.LETTERS: WEB_APP_URLS["market_letters"],
            MarketType.CAUCION: WEB_APP_URLS["market_caucion"],
            MarketType.FCI: WEB_APP_URLS["market_fci"],
        }
        for market_type, expected_url in expected_mappings.items():
            result = market_service._get_navigation_ticker_url(market_type)
            assert result == expected_url, f"Wrong URL for {market_type}: got {result}, expected {expected_url}"

    def test_get_navigation_ticker_url_unknown_type(self, market_service):
        """Test unknown ticker type returns None"""
        mock_type = Mock()
        mock_type.value = "UNKNOWN_TYPE"

        result = market_service._get_navigation_ticker_url(mock_type)

        assert result is None

    @pytest.mark.parametrize("operation", [OrderOperation.BUY, OrderOperation.SELL])
    def test_configure_operation(self, operation, market_service, mock_browser):
        """Test configuring buy/sell operation uses correct selector and message"""
        market_service._configure_operation(operation.value)

        op_config = OPERATION_SELECTORS[operation.value]
        mock_browser.click_element.assert_called_once_with(
            op_config["button"],
            f"Seleccionando la operación: {op_config['message']}."
        )

    @patch('time.sleep')
    def test_configure_limit_order(self, mock_sleep, market_service, mock_browser):
        """Test configuring limit order with correct selectors and value"""
        market_service._configure_limit_order("100,50")

        mock_sleep.assert_called_once_with(3)
        mock_browser.click_element.assert_any_call(
            OPERATION_SELECTORS["general"]["more_options"],
            "Expandiendo opciones adicionales."
        )
        mock_browser.click_element.assert_any_call(
            OPERATION_SELECTORS["general"]["limit_button"],
            "Seleccionando orden límite."
        )
        mock_browser.fill_input_with_delay.assert_called_once_with(
            OPERATION_SELECTORS["general"]["limit_input"],
            "100,50",
            "Ingresando precio límite: 100,50"
        )

    @pytest.mark.parametrize("operation,amount", [
        (OrderOperation.BUY, "1000,50"),
        (OrderOperation.SELL, "10"),
    ])
    def test_enter_amount(self, operation, amount, market_service, mock_browser):
        """Test entering amount uses correct selector for operation type"""
        market_service._enter_amount(operation.value, amount)

        op_config = OPERATION_SELECTORS[operation.value]
        mock_browser.click_element.assert_called_once_with(
            op_config["amount_input"],
            "Seleccionando el campo de entrada para el monto o cantidad."
        )
        expected_label = 'monto' if operation == OrderOperation.BUY else 'cantidad'
        mock_browser.fill_input.assert_called_once_with(
            op_config["amount_input"],
            amount,
            f"Ingresando {expected_label}: {amount}"
        )

    @patch('time.sleep')
    def test_confirm_operation_success(self, mock_sleep, market_service, mock_browser):
        """Test successful operation confirmation clicks review and confirm"""
        market_service.confirm_operation()

        mock_browser.click_element.assert_any_call(
            OPERATION_SELECTORS["confirm_buttons"]["review_buy"],
            "Haciendo clic en 'Revisar'."
        )
        mock_browser.click_element.assert_any_call(
            OPERATION_SELECTORS["confirm_buttons"]["confirm"],
            "Haciendo clic en 'Confirmar'."
        )
        mock_sleep.assert_called_once_with(4)

    @patch('time.sleep')
    def test_confirm_operation_error(self, mock_sleep, market_service, mock_browser):
        """Test operation confirmation error"""
        mock_browser.click_element.side_effect = Exception("Click failed")

        with pytest.raises(OrderCreationError, match="Error al confirmar la operación"):
            market_service.confirm_operation()


class TestOrderCreationError:
    """Tests for OrderCreationError exception"""

    def test_order_creation_error_is_exception(self):
        """Test OrderCreationError is an Exception"""
        error = OrderCreationError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
