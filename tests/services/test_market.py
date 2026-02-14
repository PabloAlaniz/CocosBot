"""Tests for CocosBot.services.market"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from CocosBot.services.market import MarketService, OrderCreationError
from CocosBot.config.enums import OrderOperation, MarketType


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
        """Test successful buy order creation"""
        # Execute
        result = market_service.create_order(
            ticker="AAPL",
            operation=OrderOperation.BUY,
            amount=1000.50
        )

        # Assert
        assert result is True
        mock_browser.go_to.assert_called_once()
        mock_browser.search_and_select.assert_called_once()

    def test_create_order_sell_with_limit(self, market_service, mock_browser):
        """Test sell order with limit price"""
        # Execute
        result = market_service.create_order(
            ticker="TSLA",
            operation="SELL",
            amount=10,
            limit=250.75
        )

        # Assert
        assert result is True

    def test_create_order_string_operation(self, market_service, mock_browser):
        """Test order creation with string operation"""
        # Execute
        result = market_service.create_order(
            ticker="GOOGL",
            operation="BUY",
            amount=500
        )

        # Assert
        assert result is True

    def test_create_order_handles_error(self, market_service, mock_browser):
        """Test order creation error handling"""
        # Setup
        mock_browser.go_to.side_effect = Exception("Navigation failed")

        # Execute & Assert
        with pytest.raises(OrderCreationError, match="Error al crear la orden"):
            market_service.create_order(
                ticker="FAIL",
                operation=OrderOperation.BUY,
                amount=100
            )

    def test_get_ticker_info_stocks(self, market_service, mock_browser):
        """Test getting ticker info for stocks"""
        # Setup
        mock_browser.process_response.return_value = {"ticker": "AAPL", "price": 150}
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        # Execute
        result = market_service.get_ticker_info("AAPL", MarketType.STOCKS)

        # Assert
        assert result == {"ticker": "AAPL", "price": 150}
        mock_browser.go_to.assert_called_once()

    def test_get_ticker_info_cedears(self, market_service, mock_browser):
        """Test getting ticker info for cedears"""
        # Setup
        mock_browser.process_response.return_value = {"ticker": "TSLA", "price": 200}
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        # Execute
        result = market_service.get_ticker_info("TSLA", "CEDEARS", segment="C")

        # Assert
        assert result == {"ticker": "TSLA", "price": 200}

    def test_get_ticker_info_error(self, market_service, mock_browser):
        """Test ticker info error handling"""
        # Setup
        mock_browser.go_to.side_effect = Exception("Error")

        # Execute
        result = market_service.get_ticker_info("FAIL", MarketType.STOCKS)

        # Assert
        assert result is None

    def test_get_market_schedule(self, market_service, mock_browser):
        """Test getting market schedule"""
        # Setup
        expected_schedule = {"open": "10:00", "close": "17:00"}
        mock_browser.fetch_data.return_value = expected_schedule

        # Execute
        result = market_service.get_market_schedule()

        # Assert
        assert result == expected_schedule
        mock_browser.fetch_data.assert_called_once()

    def test_get_orders_with_orders(self, market_service, mock_browser):
        """Test getting orders when orders exist"""
        # Setup
        expected_orders = {"orders": [{"id": 1}, {"id": 2}]}
        mock_browser.fetch_data.return_value = expected_orders

        # Execute
        result = market_service.get_orders()

        # Assert
        assert result == expected_orders

    def test_get_orders_no_orders(self, market_service, mock_browser):
        """Test getting orders when no orders exist"""
        # Setup
        mock_browser.fetch_data.return_value = None

        # Execute
        result = market_service.get_orders()

        # Assert
        assert result is None

    @patch('CocosBot.services.market.COMMON_SELECTORS', {
        'cancel_button': 'button.cancel'
    })
    def test_cancel_order_success(self, market_service, mock_browser):
        """Test successful order cancellation"""
        # Execute
        result = market_service.cancel_order(amount=1000.50, quantity=10)

        # Assert
        assert result is True
        mock_browser.go_to.assert_called_once()
        mock_browser.wait_for_element.assert_called_once()
        assert mock_browser.click_element.call_count == 2

    def test_cancel_order_failure(self, market_service, mock_browser):
        """Test order cancellation failure"""
        # Setup
        mock_browser.go_to.side_effect = Exception("Error")

        # Execute
        result = market_service.cancel_order(amount=1000, quantity=5)

        # Assert
        assert result is False

    def test_get_mep_value(self, market_service, mock_browser):
        """Test getting MEP value"""
        # Setup
        expected_mep = {"buy": 350.5, "sell": 355.2}
        mock_browser.fetch_data.return_value = expected_mep

        # Execute
        result = market_service.get_mep_value()

        # Assert
        assert result == expected_mep
        mock_browser.fetch_data.assert_called_once()

    def test_get_navigation_ticker_url_stocks(self, market_service):
        """Test getting navigation URL for stocks"""
        # Execute
        result = market_service._get_navigation_ticker_url(MarketType.STOCKS)

        # Assert
        assert result is not None
        assert "acciones" in result.lower()

    def test_get_navigation_ticker_url_bonds(self, market_service):
        """Test getting navigation URL for bonds"""
        # Execute
        result = market_service._get_navigation_ticker_url(MarketType.BONDS_CORP)

        # Assert
        assert result is not None

    def test_get_navigation_ticker_url_all_types(self, market_service):
        """Test all market types have navigation URLs"""
        # Test all market types
        for market_type in MarketType:
            result = market_service._get_navigation_ticker_url(market_type)
            assert result is not None, f"No URL for {market_type}"

    @pytest.mark.parametrize("operation", [OrderOperation.BUY, OrderOperation.SELL])
    def test_configure_operation(self, operation, market_service, mock_browser):
        """Test configuring buy/sell operation"""
        market_service._configure_operation(operation.value)

        mock_browser.click_element.assert_called_once()

    @patch('time.sleep')
    def test_configure_limit_order(self, mock_sleep, market_service, mock_browser):
        """Test configuring limit order"""
        # Execute
        market_service._configure_limit_order("100,50")

        # Assert
        mock_sleep.assert_called_once_with(3)
        assert mock_browser.click_element.call_count == 2
        mock_browser.fill_input_with_delay.assert_called_once()

    @pytest.mark.parametrize("operation,amount", [
        (OrderOperation.BUY, "1000,50"),
        (OrderOperation.SELL, "10"),
    ])
    def test_enter_amount(self, operation, amount, market_service, mock_browser):
        """Test entering amount for buy/sell operation"""
        market_service._enter_amount(operation.value, amount)

        assert mock_browser.click_element.call_count == 1
        mock_browser.fill_input.assert_called_once()

    @patch('time.sleep')
    def test_confirm_operation_success(self, mock_sleep, market_service, mock_browser):
        """Test successful operation confirmation"""
        # Execute
        market_service.confirm_operation()

        # Assert
        assert mock_browser.click_element.call_count == 2
        mock_sleep.assert_called_once_with(4)

    @patch('time.sleep')
    def test_confirm_operation_error(self, mock_sleep, market_service, mock_browser):
        """Test operation confirmation error"""
        # Setup
        mock_browser.click_element.side_effect = Exception("Click failed")

        # Execute & Assert
        with pytest.raises(OrderCreationError, match="Error al confirmar la operación"):
            market_service.confirm_operation()


class TestOrderCreationError:
    """Tests for OrderCreationError exception"""

    def test_order_creation_error_is_exception(self):
        """Test OrderCreationError is an Exception"""
        error = OrderCreationError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
