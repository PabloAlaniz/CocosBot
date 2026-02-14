"""
Tests for CocosBot data_transformations module.
"""
import pytest
from CocosBot.utils.data_transformations import process_mep_data


class TestProcessMepData:
    """Tests for process_mep_data function."""

    def test_valid_mep_data(self):
        """Test processing valid MEP data."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.5,
                "bid": 101.8,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.0,
                "bid": 102.2,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 102.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)

        assert result is not None
        assert "open" in result
        assert "close" in result
        assert "overnight" in result

    def test_open_section(self):
        """Test that open section is correctly processed."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.5,
                "bid": 101.8,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.0,
                "bid": 102.2,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 102.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)
        
        assert result["open"]["ticker"] == "AL30D"
        assert result["open"]["ask"] == 102.5
        assert result["open"]["bid"] == 101.8
        assert result["open"]["settlement_buy"] == "24hs"
        assert result["open"]["settlement_sell"] == "48hs"

    def test_close_section(self):
        """Test that close section is correctly processed."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.5,
                "bid": 101.8,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.0,
                "bid": 102.2,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 102.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)
        
        assert result["close"]["ticker"] == "AL30"
        assert result["close"]["ask"] == 103.0
        assert result["close"]["bid"] == 102.2
        assert result["close"]["settlement_buy"] == "24hs"
        assert result["close"]["settlement_sell"] == "48hs"

    def test_overnight_section(self):
        """Test that overnight section is correctly processed."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.5,
                "bid": 101.8,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.0,
                "bid": 102.2,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 102.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)
        
        assert result["overnight"]["ticker"] == "AL30C"
        assert result["overnight"]["ask"] == 102.8
        assert result["overnight"]["bid"] == 102.0
        assert result["overnight"]["settlement_buy"] == "CI"
        assert result["overnight"]["settlement_sell"] == "CI"

    def test_missing_key_open(self):
        """Test that missing key in open returns None."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                # Missing other keys
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.0,
                "bid": 102.2,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 102.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)
        assert result is None

    def test_missing_section(self):
        """Test that missing top-level section returns None."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.5,
                "bid": 101.8,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            # Missing close section
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 102.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)
        assert result is None

    def test_empty_dict(self):
        """Test that empty dict returns None."""
        result = process_mep_data({})
        assert result is None

    def test_none_input(self):
        """Test that None input returns None."""
        with pytest.raises(TypeError):
            process_mep_data(None)

    def test_field_name_transformation(self):
        """Test that camelCase fields are transformed to snake_case."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.5,
                "bid": 101.8,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.0,
                "bid": 102.2,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 102.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)
        
        # Check that output uses snake_case
        assert "settlement_buy" in result["open"]
        assert "settlement_sell" in result["open"]
        assert "settlementForBuy" not in result["open"]
        assert "settlementForSell" not in result["open"]

    def test_zero_bid_value(self):
        """Test that zero bid value is processed correctly."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.5,
                "bid": 0.0,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.0,
                "bid": 0.0,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.8,
                "bid": 0.0,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)

        assert result is not None
        assert result["open"]["bid"] == 0.0
        assert result["close"]["bid"] == 0.0

    def test_empty_string_fields(self):
        """Test processing with empty string settlement fields."""
        mep_data = {
            "open": {
                "short_ticker": "",
                "ask": 0,
                "bid": 0,
                "settlementForBuy": "",
                "settlementForSell": ""
            },
            "close": {
                "short_ticker": "",
                "ask": 0,
                "bid": 0,
                "settlementForBuy": "",
                "settlementForSell": ""
            },
            "overnight": {
                "short_ticker": "",
                "ask": 0,
                "bid": 0,
                "settlementForBuy": "",
                "settlementForSell": ""
            }
        }

        result = process_mep_data(mep_data)

        assert result is not None
        assert result["open"]["ticker"] == ""
        assert result["open"]["settlement_buy"] == ""

    def test_numeric_values_preserved(self):
        """Test that numeric values are preserved correctly."""
        mep_data = {
            "open": {
                "short_ticker": "AL30D",
                "ask": 102.567,
                "bid": 101.891,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "close": {
                "short_ticker": "AL30",
                "ask": 103.123,
                "bid": 102.234,
                "settlementForBuy": "24hs",
                "settlementForSell": "48hs"
            },
            "overnight": {
                "short_ticker": "AL30C",
                "ask": 102.845,
                "bid": 102.056,
                "settlementForBuy": "CI",
                "settlementForSell": "CI"
            }
        }

        result = process_mep_data(mep_data)
        
        assert result["open"]["ask"] == 102.567
        assert result["open"]["bid"] == 101.891
        assert isinstance(result["open"]["ask"], float)
        assert isinstance(result["open"]["bid"], float)
