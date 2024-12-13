import logging

logger = logging.getLogger(__name__)

def process_mep_data(mep_data):
    """Procesa los datos crudos del valor MEP."""
    try:
        processed_data = {
            "open": {
                "ticker": mep_data["open"]["short_ticker"],
                "ask": mep_data["open"]["ask"],
                "bid": mep_data["open"]["bid"],
                "settlement_buy": mep_data["open"]["settlementForBuy"],
                "settlement_sell": mep_data["open"]["settlementForSell"],
            },
            "close": {
                "ticker": mep_data["close"]["short_ticker"],
                "ask": mep_data["close"]["ask"],
                "bid": mep_data["close"]["bid"],
                "settlement_buy": mep_data["close"]["settlementForBuy"],
                "settlement_sell": mep_data["close"]["settlementForSell"],
            },
            "overnight": {
                "ticker": mep_data["overnight"]["short_ticker"],
                "ask": mep_data["overnight"]["ask"],
                "bid": mep_data["overnight"]["bid"],
                "settlement_buy": mep_data["overnight"]["settlementForBuy"],
                "settlement_sell": mep_data["overnight"]["settlementForSell"],
            },
        }
        return processed_data
    except KeyError as e:
        logger.error(f"Error al procesar los datos MEP: clave faltante {e}")
        return None
