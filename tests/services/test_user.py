"""Tests for CocosBot.services.user"""
import pytest
from unittest.mock import Mock, MagicMock
from CocosBot.services.user import UserService
from CocosBot.config.enums import Currency


class TestUserService:
    """Tests for UserService class"""

    @pytest.fixture
    def mock_browser(self):
        """Create a mock browser instance"""
        browser = Mock()
        browser.page = Mock()
        browser.page.locator = Mock(return_value=Mock())
        return browser

    @pytest.fixture
    def user_service(self, mock_browser):
        """Create a UserService instance with mock browser"""
        return UserService(mock_browser)

    def test_init(self, mock_browser):
        """Test UserService initialization"""
        service = UserService(mock_browser)
        assert service.browser == mock_browser

    def test_get_user_data(self, user_service, mock_browser):
        """Test getting user data"""
        # Setup
        expected_data = {"name": "Test User", "email": "test@example.com"}
        mock_browser.fetch_data.return_value = expected_data

        # Execute
        result = user_service.get_user_data()

        # Assert
        assert result == expected_data
        mock_browser.fetch_data.assert_called_once()

    def test_get_user_data_none(self, user_service, mock_browser):
        """Test getting user data when it returns None"""
        # Setup
        mock_browser.fetch_data.return_value = None

        # Execute
        result = user_service.get_user_data()

        # Assert
        assert result is None

    def test_get_account_tier(self, user_service, mock_browser):
        """Test getting account tier"""
        # Setup
        expected_tier = {"tier": "premium", "level": 3}
        mock_browser.fetch_data.return_value = expected_tier

        # Execute
        result = user_service.get_account_tier()

        # Assert
        assert result == expected_tier
        mock_browser.fetch_data.assert_called_once()

    def test_navigate_withdraw_form_ars(self, user_service, mock_browser):
        """Test navigating withdraw form with ARS"""
        # Execute
        result = user_service.navigate_withdraw_form(amount=1000.0, currency=Currency.ARS)

        # Assert
        assert result is True
        mock_browser.click_element.assert_called()
        mock_browser.fill_input.assert_called_once()
        mock_browser.wait_for_element.assert_called_once()

    def test_navigate_withdraw_form_usd(self, user_service, mock_browser):
        """Test navigating withdraw form with USD"""
        # Execute
        result = user_service.navigate_withdraw_form(amount=500.0, currency=Currency.USD)

        # Assert
        assert result is True
        mock_browser.click_element.assert_called()
        mock_browser.fill_input.assert_called_once()

    def test_navigate_withdraw_form_invalid_currency(self, user_service, mock_browser):
        """Test navigate withdraw form with invalid currency returns False"""
        # Using a mock object that's not ARS or USD - will be caught in exception handler
        invalid_currency = Mock()
        invalid_currency.__eq__ = Mock(return_value=False)
        
        # Execute - ValueError is caught and method returns False
        result = user_service.navigate_withdraw_form(amount=1000, currency=invalid_currency)
        
        # Assert
        assert result is False

    def test_navigate_withdraw_form_error(self, user_service, mock_browser):
        """Test navigate withdraw form error handling"""
        # Setup
        mock_browser.click_element.side_effect = Exception("Click failed")

        # Execute
        result = user_service.navigate_withdraw_form(amount=1000, currency=Currency.ARS)

        # Assert
        assert result is False

    def test_get_linked_accounts_ars(self, user_service, mock_browser):
        """Test getting linked accounts with ARS"""
        # Setup
        expected_accounts = [{"bank": "Bank A", "number": "1234"}]
        mock_browser.process_response.return_value = expected_accounts
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        # Execute
        result = user_service.get_linked_accounts(amount=5000, currency=Currency.ARS)

        # Assert
        assert result == expected_accounts

    def test_get_linked_accounts_usd(self, user_service, mock_browser):
        """Test getting linked accounts with USD"""
        # Setup
        expected_accounts = [{"bank": "Bank B", "number": "5678"}]
        mock_browser.process_response.return_value = expected_accounts
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        # Execute
        result = user_service.get_linked_accounts(amount=1000, currency=Currency.USD)

        # Assert
        assert result == expected_accounts

    def test_get_linked_accounts_navigate_fails(self, user_service, mock_browser):
        """Test get_linked_accounts when navigation fails"""
        # Setup
        mock_browser.click_element.side_effect = Exception("Navigation failed")

        # Execute
        result = user_service.get_linked_accounts()

        # Assert
        assert result is None

    def test_get_linked_accounts_error(self, user_service, mock_browser):
        """Test get_linked_accounts error handling"""
        # Setup
        mock_browser.page.expect_response.side_effect = Exception("Response error")

        # Execute
        result = user_service.get_linked_accounts()

        # Assert
        assert result is None

    def test_get_portfolio_data(self, user_service, mock_browser):
        """Test getting portfolio data"""
        # Setup
        expected_portfolio = {
            "stocks": [{"ticker": "AAPL", "shares": 10}],
            "total_value": 15000
        }
        mock_browser.fetch_data.return_value = expected_portfolio

        # Execute
        result = user_service.get_portfolio_data()

        # Assert
        assert result == expected_portfolio
        mock_browser.fetch_data.assert_called_once()

    def test_get_portfolio_balance(self, user_service, mock_browser):
        """Test getting portfolio balance"""
        # Setup
        mock_browser.fetch_data.return_value = 25000.50

        # Execute
        result = user_service.get_portfolio_balance()

        # Assert
        assert result == 25000.50
        # Verify fetch_data was called with a custom processor
        assert mock_browser.fetch_data.called
        call_args = mock_browser.fetch_data.call_args
        assert len(call_args[0]) == 3  # request_url, navigation_url, process_response

    def test_get_portfolio_balance_none(self, user_service, mock_browser):
        """Test getting portfolio balance when None"""
        # Setup
        mock_browser.fetch_data.return_value = None

        # Execute
        result = user_service.get_portfolio_balance()

        # Assert
        assert result is None

    def test_get_academy_data(self, user_service, mock_browser):
        """Test getting academy data"""
        # Setup
        expected_academy = {"courses": [{"name": "Investing 101"}]}
        mock_browser.fetch_data.return_value = expected_academy

        # Execute
        result = user_service.get_academy_data()

        # Assert
        assert result == expected_academy
        mock_browser.fetch_data.assert_called_once()

    def test_get_academy_data_none(self, user_service, mock_browser):
        """Test getting academy data when None"""
        # Setup
        mock_browser.fetch_data.return_value = None

        # Execute
        result = user_service.get_academy_data()

        # Assert
        assert result is None


class TestUserServiceIntegration:
    """Integration-style tests for UserService"""

    @pytest.fixture
    def mock_browser(self):
        """Create a mock browser with more realistic behavior"""
        browser = Mock()
        browser.page = Mock()
        browser.page.locator = Mock(return_value=Mock())
        return browser

    @pytest.fixture
    def user_service(self, mock_browser):
        """Create a UserService instance"""
        return UserService(mock_browser)

    def test_withdraw_flow_complete(self, user_service, mock_browser):
        """Test complete withdraw flow"""
        # Setup
        mock_browser.process_response.return_value = [{"bank": "Test Bank"}]
        mock_response = Mock()
        mock_browser.page.expect_response.return_value.__enter__ = Mock(return_value=Mock(value=mock_response))
        mock_browser.page.expect_response.return_value.__exit__ = Mock(return_value=False)

        # Execute
        accounts = user_service.get_linked_accounts(amount=10000, currency=Currency.ARS)

        # Assert
        assert accounts is not None
        assert len(accounts) > 0
        # Verify the full flow was called
        assert mock_browser.click_element.called
        assert mock_browser.fill_input.called
        assert mock_browser.wait_for_element.called
