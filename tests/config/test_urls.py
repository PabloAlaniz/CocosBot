"""
Tests for CocosBot URLs config module.
"""
import pytest
from CocosBot.config import urls


class TestUrlsConfig:
    """Tests for URL configuration."""

    def test_web_app_root_exists(self):
        """Test that WEB_APP_ROOT is defined."""
        assert hasattr(urls, 'WEB_APP_ROOT')
        assert isinstance(urls.WEB_APP_ROOT, str)
        assert urls.WEB_APP_ROOT.startswith('https://')

    def test_api_root_exists(self):
        """Test that API_ROOT is defined."""
        assert hasattr(urls, 'API_ROOT')
        assert isinstance(urls.API_ROOT, str)
        assert urls.API_ROOT.startswith('https://')

    def test_web_app_urls_dict_exists(self):
        """Test that WEB_APP_URLS dict is defined."""
        assert hasattr(urls, 'WEB_APP_URLS')
        assert isinstance(urls.WEB_APP_URLS, dict)
        assert len(urls.WEB_APP_URLS) > 0

    def test_api_urls_dict_exists(self):
        """Test that API_URLS dict is defined."""
        assert hasattr(urls, 'API_URLS')
        assert isinstance(urls.API_URLS, dict)
        assert len(urls.API_URLS) > 0

    def test_web_app_root_value(self):
        """Test WEB_APP_ROOT has expected value."""
        assert urls.WEB_APP_ROOT == "https://app.cocos.capital"

    def test_api_root_value(self):
        """Test API_ROOT has expected value."""
        assert urls.API_ROOT == "https://api.cocos.capital/api"


class TestWebAppUrls:
    """Tests for WEB_APP_URLS dictionary."""

    def test_dashboard_url(self):
        """Test dashboard URL."""
        assert "dashboard" in urls.WEB_APP_URLS
        assert urls.WEB_APP_URLS["dashboard"] == "https://app.cocos.capital/"

    def test_login_url(self):
        """Test login URL."""
        assert "login" in urls.WEB_APP_URLS
        assert urls.WEB_APP_URLS["login"] == "https://app.cocos.capital/login"

    def test_portfolio_url(self):
        """Test portfolio URL."""
        assert "portfolio" in urls.WEB_APP_URLS
        assert urls.WEB_APP_URLS["portfolio"] == "https://app.cocos.capital/capital-portfolio"

    def test_orders_url(self):
        """Test orders URL."""
        assert "orders" in urls.WEB_APP_URLS
        assert urls.WEB_APP_URLS["orders"] == "https://app.cocos.capital/orders"

    def test_movements_url(self):
        """Test movements URL."""
        assert "movements" in urls.WEB_APP_URLS
        assert urls.WEB_APP_URLS["movements"] == "https://app.cocos.capital/movements"

    def test_market_urls(self):
        """Test all market URLs are present."""
        market_keys = [
            "market_bonds_corp",
            "market_bonds_public",
            "market_caucion",
            "market_cedears",
            "market_fci",
            "market_favorites",
            "market_letters",
            "market_stocks"
        ]
        for key in market_keys:
            assert key in urls.WEB_APP_URLS
            assert urls.WEB_APP_URLS[key].startswith("https://app.cocos.capital/market/")

    def test_all_web_app_urls_start_with_root(self):
        """Test that all web app URLs start with WEB_APP_ROOT."""
        for key, url in urls.WEB_APP_URLS.items():
            assert url.startswith(urls.WEB_APP_ROOT), f"{key} URL doesn't start with WEB_APP_ROOT"


class TestApiUrls:
    """Tests for API_URLS dictionary."""

    def test_auth_token_url(self):
        """Test auth token URL."""
        assert "auth_token" in urls.API_URLS
        assert "auth/v1/token" in urls.API_URLS["auth_token"]
        assert "grant_type=password" in urls.API_URLS["auth_token"]

    def test_account_tier_url(self):
        """Test account tier URL."""
        assert "account_tier" in urls.API_URLS
        assert urls.API_URLS["account_tier"] == "https://api.cocos.capital/api/v1/users/account-tier"

    def test_academy_url(self):
        """Test academy URL."""
        assert "academy" in urls.API_URLS
        assert urls.API_URLS["academy"] == "https://api.cocos.capital/api/v1/home/academy"

    def test_markets_schedule_url(self):
        """Test markets schedule URL."""
        assert "markets_schedule" in urls.API_URLS
        assert urls.API_URLS["markets_schedule"] == "https://api.cocos.capital/api/v1/markets/schedule"

    def test_markets_tickers_url(self):
        """Test markets tickers URL."""
        assert "markets_tickers" in urls.API_URLS
        assert urls.API_URLS["markets_tickers"] == "https://api.cocos.capital/api/v1/markets/tickers"

    def test_mep_prices_url(self):
        """Test MEP prices URL."""
        assert "mep_prices" in urls.API_URLS
        assert urls.API_URLS["mep_prices"] == "https://api.cocos.capital/api/v1/public/mep-prices"

    def test_orders_url(self):
        """Test orders URL."""
        assert "orders" in urls.API_URLS
        assert urls.API_URLS["orders"] == "https://api.cocos.capital/api/v2/orders"

    def test_portfolio_data_url(self):
        """Test portfolio data URL."""
        assert "portfolio_data" in urls.API_URLS
        assert "portfolio?currency=ARS&from=BROKER" in urls.API_URLS["portfolio_data"]

    def test_portfolio_balance_url(self):
        """Test portfolio balance URL."""
        assert "portfolio_balance" in urls.API_URLS
        assert "portfolio/balance" in urls.API_URLS["portfolio_balance"]
        assert "currency=ARS" in urls.API_URLS["portfolio_balance"]
        assert "period=MAX" in urls.API_URLS["portfolio_balance"]

    def test_user_accounts_url(self):
        """Test user accounts URL."""
        assert "user_accounts" in urls.API_URLS
        assert "transfers/accounts?currency=" in urls.API_URLS["user_accounts"]

    def test_user_data_url(self):
        """Test user data URL."""
        assert "user_data" in urls.API_URLS
        assert urls.API_URLS["user_data"] == "https://api.cocos.capital/api/v1/users/me"

    def test_all_api_urls_start_with_root(self):
        """Test that all API URLs start with API_ROOT."""
        for key, url in urls.API_URLS.items():
            assert url.startswith(urls.API_ROOT), f"{key} URL doesn't start with API_ROOT"
