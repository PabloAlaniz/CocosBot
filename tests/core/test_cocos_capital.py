"""Tests for CocosBot.core.cocos_capital"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from CocosBot.config.enums import Currency, OrderOperation, MarketType


@patch('CocosBot.core.browser.sync_playwright')
class TestCocosCapitalInit:
    """Tests for CocosCapital.__init__"""

    def test_init_creates_services(self, mock_sync_pw):
        mock_pw = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=Mock()))
        mock_sync_pw.return_value.start.return_value = mock_pw

        from CocosBot.core.cocos_capital import CocosCapital
        cc = CocosCapital("user@test.com", "pass123", "gmail@test.com", "app_pass")

        assert cc.auth is not None
        assert cc.market is not None
        assert cc.user is not None
        assert cc.username == "user@test.com"
        assert cc.password == "pass123"

    def test_init_validates_credentials(self, mock_sync_pw):
        mock_pw = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=Mock()))
        mock_sync_pw.return_value.start.return_value = mock_pw

        from CocosBot.core.cocos_capital import CocosCapital
        with pytest.raises(ValueError):
            CocosCapital("", "pass", "gmail@test.com", "app_pass")

    def test_init_passes_headless(self, mock_sync_pw):
        mock_pw = Mock()
        mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=Mock()))
        mock_sync_pw.return_value.start.return_value = mock_pw

        from CocosBot.core.cocos_capital import CocosCapital
        CocosCapital("user@test.com", "pass123", "gmail@test.com", "app_pass", headless=True)

        mock_pw.chromium.launch.assert_called_once_with(headless=True)


class TestCocosCapitalDelegation:
    """Tests for CocosCapital method delegation to services"""

    @pytest.fixture
    def cocos(self):
        with patch('CocosBot.core.browser.sync_playwright') as mock_sync_pw:
            mock_pw = Mock()
            mock_pw.chromium.launch.return_value = Mock(new_page=Mock(return_value=Mock()))
            mock_sync_pw.return_value.start.return_value = mock_pw

            from CocosBot.core.cocos_capital import CocosCapital
            cc = CocosCapital("user@test.com", "pass123", "gmail@test.com", "app_pass")
            # Replace services with mocks
            cc.auth = Mock()
            cc.market = Mock()
            cc.user = Mock()
            yield cc

    def test_login_delegates(self, cocos):
        cocos.auth.login.return_value = True
        result = cocos.login()

        assert result is True
        cocos.auth.login.assert_called_once_with(
            "user@test.com", "pass123", "gmail@test.com", "app_pass"
        )

    def test_logout_delegates(self, cocos):
        cocos.auth.logout.return_value = True
        result = cocos.logout()

        assert result is True
        cocos.auth.logout.assert_called_once()

    def test_get_user_data_delegates(self, cocos):
        cocos.user.get_user_data.return_value = {"name": "Test"}
        result = cocos.get_user_data()

        assert result == {"name": "Test"}
        cocos.user.get_user_data.assert_called_once()

    def test_get_account_tier_delegates(self, cocos):
        cocos.user.get_account_tier.return_value = {"tier": "premium"}
        result = cocos.get_account_tier()

        assert result == {"tier": "premium"}
        cocos.user.get_account_tier.assert_called_once()

    def test_get_portfolio_data_delegates(self, cocos):
        cocos.user.get_portfolio_data.return_value = {"total": 1000}
        result = cocos.get_portfolio_data()

        assert result == {"total": 1000}
        cocos.user.get_portfolio_data.assert_called_once()

    def test_fetch_portfolio_balance_delegates(self, cocos):
        cocos.user.get_portfolio_balance.return_value = 25000.50
        result = cocos.fetch_portfolio_balance()

        assert result == 25000.50
        cocos.user.get_portfolio_balance.assert_called_once()

    def test_get_linked_accounts_delegates(self, cocos):
        cocos.user.get_linked_accounts.return_value = [{"bank": "Test"}]
        result = cocos.get_linked_accounts(amount=1000, currency=Currency.USD)

        assert result == [{"bank": "Test"}]
        cocos.user.get_linked_accounts.assert_called_once_with(1000, Currency.USD)

    def test_get_linked_accounts_defaults(self, cocos):
        cocos.user.get_linked_accounts.return_value = [{"bank": "Test"}]
        cocos.get_linked_accounts()

        cocos.user.get_linked_accounts.assert_called_once_with(5000, Currency.ARS)

    def test_get_academy_data_delegates(self, cocos):
        cocos.user.get_academy_data.return_value = {"courses": []}
        result = cocos.get_academy_data()

        assert result == {"courses": []}
        cocos.user.get_academy_data.assert_called_once()

    def test_create_order_delegates(self, cocos):
        cocos.market.create_order.return_value = True
        result = cocos.create_order("AAPL", OrderOperation.BUY, 1000, limit=150.0)

        assert result is True
        cocos.market.create_order.assert_called_once_with("AAPL", OrderOperation.BUY, 1000, 150.0)

    def test_get_ticker_info_delegates(self, cocos):
        cocos.market.get_ticker_info.return_value = {"ticker": "AAPL"}
        result = cocos.get_ticker_info("AAPL", MarketType.STOCKS, segment="C")

        assert result == {"ticker": "AAPL"}
        cocos.market.get_ticker_info.assert_called_once_with("AAPL", MarketType.STOCKS, "C")

    def test_get_market_schedule_delegates(self, cocos):
        cocos.market.get_market_schedule.return_value = {"open": "10:00"}
        result = cocos.get_market_schedule()

        assert result == {"open": "10:00"}
        cocos.market.get_market_schedule.assert_called_once()

    def test_get_orders_delegates(self, cocos):
        cocos.market.get_orders.return_value = {"orders": []}
        result = cocos.get_orders()

        assert result == {"orders": []}
        cocos.market.get_orders.assert_called_once()

    def test_cancel_order_delegates(self, cocos):
        cocos.market.cancel_order.return_value = True
        result = cocos.cancel_order(amount=1000, quantity=10)

        assert result is True
        cocos.market.cancel_order.assert_called_once_with(1000, 10)

    def test_get_mep_value_delegates(self, cocos):
        cocos.market.get_mep_value.return_value = {"buy": 350}
        result = cocos.get_mep_value()

        assert result == {"buy": 350}
        cocos.market.get_mep_value.assert_called_once()
