"""
Tests for CocosBot selectors config module.
"""
from CocosBot.config import selectors


class TestLoginSelectors:
    """Tests for LOGIN_SELECTORS dictionary."""

    def test_login_selectors_exists(self):
        """Test that LOGIN_SELECTORS dict exists."""
        assert hasattr(selectors, 'LOGIN_SELECTORS')
        assert isinstance(selectors.LOGIN_SELECTORS, dict)

    def test_email_input_selector(self):
        """Test email input selector."""
        assert "email_input" in selectors.LOGIN_SELECTORS
        assert 'input[type="email"]' in selectors.LOGIN_SELECTORS["email_input"]

    def test_password_input_selector(self):
        """Test password input selector."""
        assert "password_input" in selectors.LOGIN_SELECTORS
        assert 'input[type="password"]' in selectors.LOGIN_SELECTORS["password_input"]

    def test_submit_button_selector(self):
        """Test submit button selector."""
        assert "submit_button" in selectors.LOGIN_SELECTORS
        assert 'button[type="submit"]' in selectors.LOGIN_SELECTORS["submit_button"]

    def test_two_factor_container_selector(self):
        """Test 2FA container selector."""
        assert "two_factor_container" in selectors.LOGIN_SELECTORS

    def test_save_device_button_selector(self):
        """Test save device button selector."""
        assert "save_device_button" in selectors.LOGIN_SELECTORS


class TestNavigationSelectors:
    """Tests for NAVIGATION_SELECTORS dictionary."""

    def test_navigation_selectors_exists(self):
        """Test that NAVIGATION_SELECTORS dict exists."""
        assert hasattr(selectors, 'NAVIGATION_SELECTORS')
        assert isinstance(selectors.NAVIGATION_SELECTORS, dict)

    def test_logout_icon_selector(self):
        """Test logout icon selector."""
        assert "logout_icon" in selectors.NAVIGATION_SELECTORS
        assert "svg" in selectors.NAVIGATION_SELECTORS["logout_icon"]

    def test_deposit_arrow_selector(self):
        """Test deposit arrow selector."""
        assert "deposit_arrow" in selectors.NAVIGATION_SELECTORS

    def test_menu_toggle_selector(self):
        """Test menu toggle selector."""
        assert "menu_toggle" in selectors.NAVIGATION_SELECTORS


class TestOperationSelectors:
    """Tests for OPERATION_SELECTORS dictionary."""

    def test_operation_selectors_exists(self):
        """Test that OPERATION_SELECTORS dict exists."""
        assert hasattr(selectors, 'OPERATION_SELECTORS')
        assert isinstance(selectors.OPERATION_SELECTORS, dict)

    def test_general_selectors(self):
        """Test general operation selectors."""
        assert "general" in selectors.OPERATION_SELECTORS
        assert isinstance(selectors.OPERATION_SELECTORS["general"], dict)
        assert "expand_windows" in selectors.OPERATION_SELECTORS["general"]
        assert "more_options" in selectors.OPERATION_SELECTORS["general"]
        assert "limit_input" in selectors.OPERATION_SELECTORS["general"]
        assert "limit_button" in selectors.OPERATION_SELECTORS["general"]

    def test_buy_selectors(self):
        """Test BUY operation selectors."""
        assert "BUY" in selectors.OPERATION_SELECTORS
        buy_selectors = selectors.OPERATION_SELECTORS["BUY"]
        assert "button" in buy_selectors
        assert "amount_input" in buy_selectors
        assert "message" in buy_selectors
        assert buy_selectors["message"] == "Compra"

    def test_sell_selectors(self):
        """Test SELL operation selectors."""
        assert "SELL" in selectors.OPERATION_SELECTORS
        sell_selectors = selectors.OPERATION_SELECTORS["SELL"]
        assert "button" in sell_selectors
        assert "amount_input" in sell_selectors
        assert "message" in sell_selectors
        assert sell_selectors["message"] == "Venta"

    def test_confirm_buttons_selectors(self):
        """Test confirm buttons selectors."""
        assert "confirm_buttons" in selectors.OPERATION_SELECTORS
        confirm = selectors.OPERATION_SELECTORS["confirm_buttons"]
        assert "review_buy" in confirm
        assert "confirm" in confirm


class TestOrderSelectors:
    """Tests for ORDER_SELECTORS dictionary."""

    def test_order_selectors_exists(self):
        """Test that ORDER_SELECTORS dict exists."""
        assert hasattr(selectors, 'ORDER_SELECTORS')
        assert isinstance(selectors.ORDER_SELECTORS, dict)

    def test_orders_list_selector(self):
        """Test orders list selector."""
        assert "orders_list" in selectors.ORDER_SELECTORS

    def test_order_row_selector(self):
        """Test order row selector."""
        assert "order_row" in selectors.ORDER_SELECTORS

    def test_cancel_button_selector(self):
        """Test cancel button selector."""
        assert "cancel_button" in selectors.ORDER_SELECTORS


class TestCommonSelectors:
    """Tests for COMMON_SELECTORS dictionary."""

    def test_common_selectors_exists(self):
        """Test that COMMON_SELECTORS dict exists."""
        assert hasattr(selectors, 'COMMON_SELECTORS')
        assert isinstance(selectors.COMMON_SELECTORS, dict)

    def test_search_input_selector(self):
        """Test search input selector."""
        assert "search_input" in selectors.COMMON_SELECTORS
        assert "input" in selectors.COMMON_SELECTORS["search_input"]

    def test_continue_button_selector(self):
        """Test continue button selector."""
        assert "continue_button" in selectors.COMMON_SELECTORS

    def test_loading_spinner_selector(self):
        """Test loading spinner selector."""
        assert "loading_spinner" in selectors.COMMON_SELECTORS


class TestListSelectors:
    """Tests for LIST_SELECTORS dictionary."""

    def test_list_selectors_exists(self):
        """Test that LIST_SELECTORS dict exists."""
        assert hasattr(selectors, 'LIST_SELECTORS')
        assert isinstance(selectors.LIST_SELECTORS, dict)

    def test_search_list_selector(self):
        """Test search list selector."""
        assert "search_list" in selectors.LIST_SELECTORS

    def test_list_item_selector_function(self):
        """Test list item selector is callable."""
        assert "list_item" in selectors.LIST_SELECTORS
        assert callable(selectors.LIST_SELECTORS["list_item"])

    def test_list_item_selector_generates_correct_string(self):
        """Test list item selector generates correct CSS selector."""
        selector_fn = selectors.LIST_SELECTORS["list_item"]
        result = selector_fn("AAPL")
        assert "AAPL" in result
        assert "ul.MuiList-root.search-list" in result


class TestTransferSelectors:
    """Tests for TRANSFER_SELECTORS dictionary."""

    def test_transfer_selectors_exists(self):
        """Test that TRANSFER_SELECTORS dict exists."""
        assert hasattr(selectors, 'TRANSFER_SELECTORS')
        assert isinstance(selectors.TRANSFER_SELECTORS, dict)

    def test_withdraw_button_selector(self):
        """Test withdraw button selector."""
        assert "withdraw_button" in selectors.TRANSFER_SELECTORS

    def test_currency_selectors(self):
        """Test currency selectors."""
        assert "currency_ars" in selectors.TRANSFER_SELECTORS
        assert "currency_usd" in selectors.TRANSFER_SELECTORS

    def test_amount_input_selector(self):
        """Test amount input selector."""
        assert "amount_input" in selectors.TRANSFER_SELECTORS

    def test_continue_button_selector(self):
        """Test continue button selector."""
        assert "continue_button" in selectors.TRANSFER_SELECTORS


class TestMessageSelectors:
    """Tests for MESSAGE_SELECTORS dictionary."""

    def test_message_selectors_exists(self):
        """Test that MESSAGE_SELECTORS dict exists."""
        assert hasattr(selectors, 'MESSAGE_SELECTORS')
        assert isinstance(selectors.MESSAGE_SELECTORS, dict)

    def test_error_message_selector(self):
        """Test error message selector."""
        assert "error_message" in selectors.MESSAGE_SELECTORS

    def test_success_message_selector(self):
        """Test success message selector."""
        assert "success_message" in selectors.MESSAGE_SELECTORS

    def test_confirmation_dialog_selector(self):
        """Test confirmation dialog selector."""
        assert "confirmation_dialog" in selectors.MESSAGE_SELECTORS


class TestPortfolioSelectors:
    """Tests for PORTFOLIO_SELECTORS dictionary."""

    def test_portfolio_selectors_exists(self):
        """Test that PORTFOLIO_SELECTORS dict exists."""
        assert hasattr(selectors, 'PORTFOLIO_SELECTORS')
        assert isinstance(selectors.PORTFOLIO_SELECTORS, dict)

    def test_total_balance_selector(self):
        """Test total balance selector."""
        assert "total_balance" in selectors.PORTFOLIO_SELECTORS

    def test_portfolio_table_selector(self):
        """Test portfolio table selector."""
        assert "portfolio_table" in selectors.PORTFOLIO_SELECTORS

    def test_portfolio_item_selector_function(self):
        """Test portfolio item selector is callable."""
        assert "portfolio_item" in selectors.PORTFOLIO_SELECTORS
        assert callable(selectors.PORTFOLIO_SELECTORS["portfolio_item"])

    def test_portfolio_item_selector_generates_correct_string(self):
        """Test portfolio item selector generates correct CSS selector."""
        selector_fn = selectors.PORTFOLIO_SELECTORS["portfolio_item"]
        result = selector_fn("AAPL")
        assert "AAPL" in result
        assert "tr[data-ticker=" in result
