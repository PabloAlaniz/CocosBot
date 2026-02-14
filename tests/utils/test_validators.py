"""
Tests for CocosBot validators module.
"""
import pytest
from CocosBot.utils.validators import (
    validate_order_params,
    validate_currency,
    validate_market_type,
    validate_credentials
)
from CocosBot.config.enums import Currency, MarketType


class TestValidateOrderParams:
    """Tests for validate_order_params function."""

    def test_valid_buy_order(self):
        """Test valid BUY order parameters."""
        operation, ticker = validate_order_params("AAPL", "BUY", 1000)
        assert operation == "BUY"
        assert ticker == "AAPL"

    def test_valid_sell_order(self):
        """Test valid SELL order parameters."""
        operation, ticker = validate_order_params("GOOGL", "SELL", 500, limit=150.5)
        assert operation == "SELL"
        assert ticker == "GOOGL"

    @pytest.mark.parametrize("input_op,expected", [
        ("buy", "BUY"),
        ("sell", "SELL"),
        ("Buy", "BUY"),
        ("Sell", "SELL"),
    ])
    def test_operation_case_insensitive(self, input_op, expected):
        """Test that operation is normalized to uppercase."""
        operation, _ = validate_order_params("AAPL", input_op, 1000)
        assert operation == expected

    def test_invalid_ticker_empty_string(self):
        """Test that empty ticker raises ValueError."""
        with pytest.raises(ValueError, match="El ticker debe ser una cadena no vacía"):
            validate_order_params("", "BUY", 1000)

    def test_invalid_ticker_not_string(self):
        """Test that non-string ticker raises ValueError."""
        with pytest.raises(ValueError, match="El ticker debe ser una cadena no vacía"):
            validate_order_params(123, "BUY", 1000)

    def test_invalid_operation(self):
        """Test that invalid operation raises ValueError."""
        with pytest.raises(ValueError, match="La operación debe ser 'BUY' o 'SELL'"):
            validate_order_params("AAPL", "HOLD", 1000)

    def test_invalid_amount_zero(self):
        """Test that zero amount raises ValueError."""
        with pytest.raises(ValueError, match="El monto debe ser un número positivo"):
            validate_order_params("AAPL", "BUY", 0)

    def test_invalid_amount_negative(self):
        """Test that negative amount raises ValueError."""
        with pytest.raises(ValueError, match="El monto debe ser un número positivo"):
            validate_order_params("AAPL", "BUY", -100)

    def test_invalid_amount_not_number(self):
        """Test that non-numeric amount raises ValueError."""
        with pytest.raises(ValueError, match="El monto debe ser un número positivo"):
            validate_order_params("AAPL", "BUY", "1000")

    def test_invalid_limit_zero(self):
        """Test that zero limit raises ValueError."""
        with pytest.raises(ValueError, match="El límite debe ser un número positivo"):
            validate_order_params("AAPL", "BUY", 1000, limit=0)

    def test_invalid_limit_negative(self):
        """Test that negative limit raises ValueError."""
        with pytest.raises(ValueError, match="El límite debe ser un número positivo"):
            validate_order_params("AAPL", "BUY", 1000, limit=-50)

    def test_valid_with_float_amount(self):
        """Test that float amounts are accepted."""
        operation, ticker = validate_order_params("AAPL", "BUY", 1000.50)
        assert operation == "BUY"
        assert ticker == "AAPL"

    def test_valid_with_float_limit(self):
        """Test that float limits are accepted."""
        operation, ticker = validate_order_params("AAPL", "BUY", 1000, limit=150.75)
        assert operation == "BUY"
        assert ticker == "AAPL"


class TestValidateCurrency:
    """Tests for validate_currency function."""

    def test_valid_ars(self):
        """Test valid ARS currency."""
        result = validate_currency("ARS")
        assert result == Currency.ARS

    def test_valid_usd(self):
        """Test valid USD currency."""
        result = validate_currency("USD")
        assert result == Currency.USD

    def test_case_insensitive(self):
        """Test that currency validation is case insensitive."""
        assert validate_currency("ars") == Currency.ARS
        assert validate_currency("usd") == Currency.USD
        assert validate_currency("Ars") == Currency.ARS

    def test_invalid_currency(self):
        """Test that invalid currency raises ValueError."""
        with pytest.raises(ValueError, match="Moneda no válida: EUR"):
            validate_currency("EUR")

    def test_empty_currency(self):
        """Test that empty currency raises ValueError."""
        with pytest.raises(ValueError):
            validate_currency("")


class TestValidateMarketType:
    """Tests for validate_market_type function."""

    def test_valid_stocks_string(self):
        """Test valid STOCKS market type as string."""
        result = validate_market_type("STOCKS")
        assert result == MarketType.STOCKS

    def test_valid_cedears_string(self):
        """Test valid CEDEARS market type as string."""
        result = validate_market_type("CEDEARS")
        assert result == MarketType.CEDEARS

    def test_valid_market_type_enum(self):
        """Test that passing MarketType enum directly works."""
        result = validate_market_type(MarketType.STOCKS)
        assert result == MarketType.STOCKS

    def test_case_insensitive(self):
        """Test that market type validation is case insensitive."""
        assert validate_market_type("stocks") == MarketType.STOCKS
        assert validate_market_type("cedears") == MarketType.CEDEARS
        assert validate_market_type("Stocks") == MarketType.STOCKS

    @pytest.mark.parametrize("type_str,expected", [
        ("STOCKS", MarketType.STOCKS),
        ("CEDEARS", MarketType.CEDEARS),
        ("BONDS_CORP", MarketType.BONDS_CORP),
        ("BONDS_PUBLIC", MarketType.BONDS_PUBLIC),
        ("LETTERS", MarketType.LETTERS),
        ("CAUCION", MarketType.CAUCION),
        ("FCI", MarketType.FCI),
    ])
    def test_all_market_types(self, type_str, expected):
        """Test all valid market types."""
        assert validate_market_type(type_str) == expected

    def test_invalid_market_type_string(self):
        """Test that invalid market type raises ValueError."""
        with pytest.raises(ValueError, match="Tipo de mercado no válido"):
            validate_market_type("INVALID")

    def test_invalid_type(self):
        """Test that invalid type raises ValueError."""
        with pytest.raises(ValueError, match="Tipo de mercado no soportado"):
            validate_market_type(123)


class TestValidateCredentials:
    """Tests for validate_credentials function."""

    def test_valid_credentials(self):
        """Test valid credentials list."""
        credentials = ["username", "password", "email", "app_pass"]
        validate_credentials(credentials)  # Should not raise

    def test_empty_credential(self):
        """Test that empty credential raises ValueError."""
        with pytest.raises(ValueError, match="Todos los parámetros de credenciales deben ser cadenas no vacías"):
            validate_credentials(["username", "", "email"])

    def test_whitespace_only_credential(self):
        """Test that whitespace-only credential raises ValueError."""
        with pytest.raises(ValueError, match="Todos los parámetros de credenciales deben ser cadenas no vacías"):
            validate_credentials(["username", "   ", "email"])

    def test_non_string_credential(self):
        """Test that non-string credential raises ValueError."""
        with pytest.raises(ValueError, match="Todos los parámetros de credenciales deben ser cadenas no vacías"):
            validate_credentials(["username", 123, "email"])

    def test_none_credential(self):
        """Test that None credential raises ValueError."""
        with pytest.raises(ValueError, match="Todos los parámetros de credenciales deben ser cadenas no vacías"):
            validate_credentials(["username", None, "email"])

    def test_single_valid_credential(self):
        """Test single valid credential."""
        validate_credentials(["username"])  # Should not raise

    def test_empty_list(self):
        """Test empty credentials list."""
        validate_credentials([])  # Should not raise (all() returns True for empty)
