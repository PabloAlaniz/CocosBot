from typing import Union, Optional, List
from CocosBot.config.selectors import OPERATION_SELECTORS
from CocosBot.config.enums import Currency
from CocosBot.config.enums import MarketType

def validate_order_params(
        ticker: str,
        operation: str,
        amount: Union[int, float],
        limit: Optional[Union[int, float]] = None
) -> tuple[str, str]:
    """
    Valida los parámetros de una orden de compra/venta.

    Args:
        ticker (str): Símbolo del ticker
        operation (str): Tipo de operación ('BUY' o 'SELL')
        amount (Union[int, float]): Monto a invertir o cantidad de acciones
        limit (Optional[Union[int, float]]): Precio límite para la orden

    Returns:
        tuple[str, str]: Operation normalizada y ticker validado

    Raises:
        ValueError: Si algún parámetro no es válido
    """
    if not isinstance(ticker, str) or not ticker:
        raise ValueError("El ticker debe ser una cadena no vacía")

    operation = operation.upper()
    if operation not in OPERATION_SELECTORS:
        raise ValueError("La operación debe ser 'BUY' o 'SELL'")

    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("El monto debe ser un número positivo")

    if limit is not None and (not isinstance(limit, (int, float)) or limit <= 0):
        raise ValueError("El límite debe ser un número positivo")

    return operation, ticker


def validate_currency(currency: str) -> Currency:
    """
    Valida que la moneda sea una de las permitidas y la convierte a Enum.

    Args:
        currency (str): Moneda como cadena (e.g., 'ARS', 'USD')

    Returns:
        Currency: Instancia del Enum Currency

    Raises:
        ValueError: Si la moneda no es válida
    """
    try:
        return Currency[currency.upper()]
    except KeyError:
        raise ValueError(f"Moneda no válida: {currency}. Use 'ARS' o 'USD'")




def validate_market_type(market_type: Union[str, MarketType]) -> MarketType:
    """
    Valida y convierte el tipo de mercado a una instancia de MarketType.

    Args:
        market_type (Union[str, MarketType]): Tipo de mercado como cadena o instancia de MarketType.

    Returns:
        MarketType: Instancia validada de MarketType.

    Raises:
        ValueError: Si el tipo de mercado no es válido.
    """
    if isinstance(market_type, MarketType):
        return market_type
    elif isinstance(market_type, str):
        try:
            return MarketType[market_type.upper()]
        except KeyError:
            raise ValueError(f"Tipo de mercado no válido: {market_type}. Use uno de {list(MarketType)}.")
    else:
        raise ValueError(f"Tipo de mercado no soportado: {type(market_type)}")



def validate_credentials(credentials: List[str]) -> None:
    """
    Valida que todas las credenciales sean cadenas no vacías.

    Args:
        credentials (List[str]): Lista de credenciales a validar.

    Raises:
        ValueError: Si alguna de las credenciales no es válida.
    """
    if not all(isinstance(cred, str) and cred.strip() for cred in credentials):
        raise ValueError("Todos los parámetros de credenciales deben ser cadenas no vacías.")

