"""Tests for CocosBot.services.user"""
import pytest
from unittest.mock import Mock, MagicMock
from CocosBot.services.user import UserService
from CocosBot.config.enums import Currency
from CocosBot.config.urls import WEB_APP_URLS, API_URLS
from CocosBot.config.selectors import TRANSFER_SELECTORS


class TestUserService:
    """Tests for UserService class"""

    @pytest.fixture
    def user_service(self, mock_browser):
        """Create a UserService instance with mock browser"""
        return UserService(mock_browser)

    def test_init(self, mock_browser):
        """Test UserService initialization"""
        service = UserService(mock_browser)
        assert service.browser == mock_browser

    def test_get_user_data(self, user_service, mock_browser):
        """Test getting user data with correct URLs"""
        expected_data = {"name": "Test User", "email": "test@example.com"}
        mock_browser.fetch_data.return_value = expected_data

        result = user_service.get_user_data()

        assert result == expected_data
        mock_browser.fetch_data.assert_called_once_with(
            API_URLS["user_data"],
            WEB_APP_URLS["dashboard"]
        )

    def test_get_user_data_none(self, user_service, mock_browser):
        """Test getting user data when it returns None"""
        mock_browser.fetch_data.return_value = None

        result = user_service.get_user_data()

        assert result is None

    def test_get_account_tier(self, user_service, mock_browser):
        """Test getting account tier with correct URLs"""
        expected_tier = {"tier": "premium", "level": 3}
        mock_browser.fetch_data.return_value = expected_tier

        result = user_service.get_account_tier()

        assert result == expected_tier
        mock_browser.fetch_data.assert_called_once_with(
            request_url=API_URLS["account_tier"],
            navigation_url=WEB_APP_URLS["dashboard"]
        )

    def test_navigate_withdraw_form_ars(self, user_service, mock_browser):
        """Test navigating withdraw form with ARS uses correct selectors"""
        result = user_service.navigate_withdraw_form(amount=1000.0, currency=Currency.ARS)

        assert result is True
        mock_browser.click_element.assert_any_call(
            TRANSFER_SELECTORS["withdraw_button"],
            "Navegando al apartado de extraer desde el dashboard."
        )
        mock_browser.click_element.assert_any_call(
            TRANSFER_SELECTORS["currency_ars"],
            "Seleccionando moneda ARS."
        )
        mock_browser.fill_input.assert_called_once_with(
            TRANSFER_SELECTORS["amount_input"],
            "1000.0",
            "Ingresando monto 1000.0"
        )
        mock_browser.page.locator.assert_called_once_with(TRANSFER_SELECTORS["amount_input"])
        mock_browser.page.locator.return_value.evaluate.assert_called_once_with("el => el.blur()")
        mock_browser.wait_for_element.assert_called_once_with(
            TRANSFER_SELECTORS["continue_button"],
            "Esperando que el botón 'Continuar' habilitado sea visible dentro del contenedor 'Extraé dinero'."
        )

    def test_navigate_withdraw_form_usd(self, user_service, mock_browser):
        """Test navigating withdraw form with USD selects correct currency"""
        result = user_service.navigate_withdraw_form(amount=500.0, currency=Currency.USD)

        assert result is True
        mock_browser.click_element.assert_any_call(
            TRANSFER_SELECTORS["currency_usd"],
            "Seleccionando moneda USD."
        )
        mock_browser.fill_input.assert_called_once_with(
            TRANSFER_SELECTORS["amount_input"],
            "500.0",
            "Ingresando monto 500.0"
        )

    def test_navigate_withdraw_form_invalid_currency(self, user_service, mock_browser):
        """Test navigate withdraw form with invalid currency returns False"""
        invalid_currency = "EUR"

        result = user_service.navigate_withdraw_form(amount=1000, currency=invalid_currency)

        assert result is False

    def test_navigate_withdraw_form_error(self, user_service, mock_browser):
        """Test navigate withdraw form error handling"""
        mock_browser.click_element.side_effect = Exception("Click failed")

        result = user_service.navigate_withdraw_form(amount=1000, currency=Currency.ARS)

        assert result is False

    def test_get_linked_accounts_ars(self, user_service, mock_browser):
        """Test getting linked accounts with ARS"""
        expected_accounts = [{"bank": "Bank A", "number": "1234"}]
        mock_browser.process_response.return_value = expected_accounts
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = user_service.get_linked_accounts(amount=5000, currency=Currency.ARS)

        assert result == expected_accounts

    def test_get_linked_accounts_usd(self, user_service, mock_browser):
        """Test getting linked accounts with USD"""
        expected_accounts = [{"bank": "Bank B", "number": "5678"}]
        mock_browser.process_response.return_value = expected_accounts
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        result = user_service.get_linked_accounts(amount=1000, currency=Currency.USD)

        assert result == expected_accounts

    def test_get_linked_accounts_navigate_fails(self, user_service, mock_browser):
        """Test get_linked_accounts when navigation fails"""
        mock_browser.click_element.side_effect = Exception("Navigation failed")

        result = user_service.get_linked_accounts()

        assert result is None

    def test_get_linked_accounts_error(self, user_service, mock_browser):
        """Test get_linked_accounts error handling"""
        mock_browser.page.expect_response.side_effect = Exception("Response error")

        result = user_service.get_linked_accounts()

        assert result is None

    def test_get_portfolio_data(self, user_service, mock_browser):
        """Test getting portfolio data with correct URLs"""
        expected_portfolio = {
            "stocks": [{"ticker": "AAPL", "shares": 10}],
            "total_value": 15000
        }
        mock_browser.fetch_data.return_value = expected_portfolio

        result = user_service.get_portfolio_data()

        assert result == expected_portfolio
        mock_browser.fetch_data.assert_called_once_with(
            request_url=API_URLS["portfolio_data"],
            navigation_url=WEB_APP_URLS["portfolio"]
        )

    def test_get_portfolio_balance(self, user_service, mock_browser):
        """Test getting portfolio balance verifies custom processor"""
        mock_browser.fetch_data.return_value = 25000.50

        result = user_service.get_portfolio_balance()

        assert result == 25000.50
        call_args = mock_browser.fetch_data.call_args
        assert call_args[0][0] == API_URLS["portfolio_balance"]
        assert call_args[0][1] == WEB_APP_URLS["portfolio"]
        # Verify the process_response function works correctly
        process_fn = call_args[0][2]
        assert process_fn({"totalBalance": 42000.0}) == 42000.0
        assert process_fn({"other": "data"}) is None

    def test_get_portfolio_balance_none(self, user_service, mock_browser):
        """Test getting portfolio balance when None"""
        mock_browser.fetch_data.return_value = None

        result = user_service.get_portfolio_balance()

        assert result is None

    def test_get_academy_data(self, user_service, mock_browser):
        """Test getting academy data with correct URLs"""
        expected_academy = {"courses": [{"name": "Investing 101"}]}
        mock_browser.fetch_data.return_value = expected_academy

        result = user_service.get_academy_data()

        assert result == expected_academy
        mock_browser.fetch_data.assert_called_once_with(
            request_url=API_URLS["academy"],
            navigation_url=WEB_APP_URLS["dashboard"]
        )

    def test_get_academy_data_none(self, user_service, mock_browser):
        """Test getting academy data when None"""
        mock_browser.fetch_data.return_value = None

        result = user_service.get_academy_data()

        assert result is None


class TestUserServiceIntegration:
    """Integration-style tests for UserService"""

    @pytest.fixture
    def user_service(self, mock_browser):
        """Create a UserService instance"""
        return UserService(mock_browser)

    def test_withdraw_flow_complete(self, user_service, mock_browser):
        """Test complete withdraw flow verifies navigation and response"""
        mock_browser.process_response.return_value = [{"bank": "Test Bank"}]
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        accounts = user_service.get_linked_accounts(amount=10000, currency=Currency.ARS)

        assert accounts is not None
        assert len(accounts) > 0
        mock_browser.click_element.assert_any_call(
            TRANSFER_SELECTORS["withdraw_button"],
            "Navegando al apartado de extraer desde el dashboard."
        )
        mock_browser.fill_input.assert_called_once_with(
            TRANSFER_SELECTORS["amount_input"],
            "10000",
            "Ingresando monto 10000"
        )
        mock_browser.wait_for_element.assert_called_once_with(
            TRANSFER_SELECTORS["continue_button"],
            "Esperando que el botón 'Continuar' habilitado sea visible dentro del contenedor 'Extraé dinero'."
        )
