# URLs Base
WEB_APP_ROOT = "https://app.cocos.capital"
API_ROOT = "https://api.cocos.capital/api"

# URLs de la Web App
WEB_APP_URLS = {
    "dashboard": f"{WEB_APP_ROOT}/",
    "login": f"{WEB_APP_ROOT}/login",
    "market_bonds_corp": f"{WEB_APP_ROOT}/market/BONOS_CORP",
    "market_bonds_public": f"{WEB_APP_ROOT}/market/BONOS_PUBLICOS",
    "market_caucion": f"{WEB_APP_ROOT}/market/CAUCION",
    "market_cedears": f"{WEB_APP_ROOT}/market/CEDEARS",
    "market_fci": f"{WEB_APP_ROOT}/market/FCI",
    "market_favorites": f"{WEB_APP_ROOT}/market/Favoritos",
    "market_letters": f"{WEB_APP_ROOT}/market/LETRAS",
    "market_stocks": f"{WEB_APP_ROOT}/market/ACCIONES",
    "movements": f"{WEB_APP_ROOT}/movements",
    "orders": f"{WEB_APP_ROOT}/orders",
    "portfolio": f"{WEB_APP_ROOT}/capital-portfolio",
}

# URLs de la API
API_URLS = {
    "auth_token": f"{API_ROOT}/auth/v1/token?grant_type=password",
    "account_tier": f"{API_ROOT}/v1/users/account-tier",
    "academy": f"{API_ROOT}/v1/home/academy",
    "markets_schedule": f"{API_ROOT}/v1/markets/schedule",
    "markets_tickers": f"{API_ROOT}/v1/markets/tickers",
    "mep_prices": f"{API_ROOT}/v1/public/mep-prices",
    "orders": f"{API_ROOT}/v2/orders",
    "portfolio_data": f"{API_ROOT}/portfolio?currency=ARS&from=BROKER",
    "portfolio_balance": f"{API_ROOT}/portfolio/balance?currency=ARS&period=MAX",
    "user_accounts": f"{API_ROOT}/v1/transfers/accounts?currency=",
    "user_data": f"{API_ROOT}/v1/users/me",
}


