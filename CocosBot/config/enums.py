from enum import Enum

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

class OrderOperation(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class MarketType(Enum):
    STOCKS = "ACCIONES"
    CEDEARS = "CEDEARS"
    BONDS_CORP = "BONOS_CORP"
    BONDS_PUBLIC = "BONOS_PUBLICOS"
    LETTERS = "LETRAS"
    CAUCION = "CAUCION"
    FCI = "FCI"

class Currency(Enum):
    ARS = "ARS"
    USD = "USD"

class TimeFrame(Enum):
    DAILY = "1D"
    WEEKLY = "1W"
    MONTHLY = "1M"
    YEARLY = "1Y"
    MAX = "MAX"

class ElementState(Enum):
    VISIBLE = "visible"
    CLICKABLE = "clickable"
    HIDDEN = "hidden"