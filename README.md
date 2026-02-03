# CocosBot

CocosBot es un paquete de Python diseñado para automatizar operaciones y obtener datos de la API del broker argentino Cocos Capital. Utiliza Playwright para interactuar con la web app.

La historia del proyecto en Medium: [CocosBot](https://medium.com/@PabloAlaniz/automatizando-cocos-capital-con-python-d3a0e389277b)

## Características

- Arquitectura modular con servicios especializados
- Automatización de operaciones en la plataforma Cocos Capital
- Interceptación inteligente de endpoints de API
- Soporte para 2FA (autenticación de dos factores) utilizando cuentas de Gmail
- Sistema robusto de manejo de errores
- Tipado completo con type hints

## Arquitectura

```plaintext
cocos_bot/
├── core/                 # Componentes fundamentales
│   ├── browser.py       # Abstracción de Playwright
│   ├── cocos_capital.py # Orquestador principal
│   ├── exceptions.py    # Sistema de errores
├── config/              # Configuración centralizada
│   ├── constants.py     # URLs y configs
│   ├── urls.py        # Urls de la plataforma
│   └── selectors.py    # Selectores UI
│   └── enums.py        # Enums
├── utils/              # Utilidades
│   ├── validators.py   # Validación
│   ├── helpers.py     # Funciones auxiliares
│   ├── gmail_2fa.py   # Manejo 2FA
│   └── data_transformations.py
└── services/           # Lógica de negocio
    ├── auth.py        # Autenticación
    ├── market.py      # Operaciones
    └── user.py        # Gestión de usuario
```

## Requisitos

- Python 3.10 o superior (testeado en 3.10, 3.11 y 3.12).
- Cuenta en Cocos Capital.
- Credenciales de Gmail configuradas para autenticación 2FA.

## Instalación

Instala el paquete y las dependencias ejecutando:
```bash
pip install CocosBot
```
Esto va a instalar automáticamente las dependencias necesarias, como `playwright` y `beautifulsoup4`.

## Uso

### Ejemplo básico

```python
from CocosBot.core.cocos_capital import CocosCapital

# Configurar credenciales

username = "tu_usuario"
password = "tu_contraseña"
gmail_user = "tu_gmail@gmail.com"
gmail_app_pass = "tu_contraseña_de_aplicación"

with CocosCapital(username, password, gmail_user, gmail_app_pass, headless=False) as cocos:
    cocos.login()

    # Probar view accounts
    cuentas = cocos.get_linked_accounts()
    print("Cuentas:", cuentas)

    # Probar get_orders
    orders = cocos.get_orders()
    print("Orders:", orders)

    # Probar get_mep_value
    mep_value = cocos.get_mep_value()
    print("MEP Value:", mep_value)

    # Probar get_ticker_info
    ticker_info = cocos.get_ticker_info("AAPL", "CEDEARS")
    print("Ticker Info:", ticker_info)

    # Probar Create Order
    order= cocos.create_order("FIPL", "BUY", 20000, 335.5 )
    print("Order", order)
```
### Métodos Disponibles

#### Autenticación
- `login() -> bool`: Inicia sesión en la plataforma usando 2FA automático
- `logout() -> bool`: Realiza el cierre de sesión seguro

#### Usuario y Cuenta
- `get_user_data() -> Dict[str, Any]`: Obtiene los datos del usuario
- `get_account_tier() -> Dict[str, Any]`: Obtiene el nivel de cuenta del usuario
- `get_portfolio_data() -> Dict[str, Any]`: Obtiene los datos del portafolio
- `fetch_portfolio_balance() -> float`: Obtiene el balance total del portafolio
- `get_linked_accounts(amount: float = 5000, currency: Currency = Currency.ARS) -> Dict[str, Any]`: Obtiene información de cuentas vinculadas
- `get_academy_data() -> Dict[str, Any]`: Obtiene datos de la sección Academia

#### Mercado y Operaciones
- `create_order(ticker: str, operation: OrderOperation, amount: float, limit: Optional[float] = None) -> bool`: Crea una orden
- `get_ticker_info(ticker: str, ticker_type: Union[str, MarketType], segment: str = "C") -> Dict[str, Any]`: Obtiene información de un ticker
- `get_market_schedule() -> Dict[str, Any]`: Obtiene los horarios del mercado
- `get_orders() -> Dict[str, Any]`: Obtiene las órdenes del usuario
- `get_mep_value() -> Dict[str, Any]`: Obtiene el valor del dólar MEP
---

## Testing

El proyecto incluye una suite completa de tests:

```bash
pip install -e ".[dev]"
pytest
```

**Coverage actual:** 169 tests, 59% coverage global.

## To-Do
- 2FA manual (sin Gmail)
- Documentación adicional de métodos avanzados

## Contribución

¡Contribuciones bienvenidas! Si tenés ideas o mejoras, por favor abrí un issue o crea un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
