# CocosBot

CocosBot es un paquete de Python diseñado para automatizar operaciones y obtener datos de la API del broker argentino **Cocos Capital**. Utiliza **Playwright** para interactuar con la plataforma web de manera programática.

> **📖 Artículo en Medium:** [Automatizando Cocos Capital con Python](https://medium.com/@PabloAlaniz/automatizando-cocos-capital-con-python-d3a0e389277b)

## 🎯 ¿Por qué CocosBot?

Cocos Capital no ofrece API pública. CocosBot resuelve esto interceptando requests de la web app, permitiendo:
- Automatizar operaciones de compra/venta
- Obtener datos de mercado en tiempo real
- Gestionar portafolios programáticamente
- Integrar con estrategias de trading custom

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

### 1. Instalar el paquete
```bash
pip install CocosBot
```

### 2. Instalar navegadores de Playwright
Playwright requiere descargar navegadores la primera vez:
```bash
playwright install chromium
```

### 3. (Opcional) Instalación desde código fuente
Para desarrollo o testing:
```bash
git clone https://github.com/PabloAlaniz/CocosBot.git
cd CocosBot
pip install -e ".[dev]"
playwright install chromium
```

## 🔐 Configuración de Credenciales

CocosBot necesita:
- **Usuario y contraseña** de Cocos Capital
- **Gmail** para autenticación 2FA (contraseña de aplicación)

### Variables de entorno (recomendado)
```bash
export COCOS_USERNAME="tu_usuario"
export COCOS_PASSWORD="tu_contraseña"
export GMAIL_USER="tu_gmail@gmail.com"
export GMAIL_APP_PASS="tu_contraseña_de_aplicación"
```

O crear un archivo `.env`:
```env
COCOS_USERNAME=tu_usuario
COCOS_PASSWORD=tu_contraseña
GMAIL_USER=tu_gmail@gmail.com
GMAIL_APP_PASS=tu_contraseña_de_aplicación
```

### Obtener contraseña de aplicación de Gmail
1. Ir a [Contraseñas de aplicación de Google](https://myaccount.google.com/apppasswords)
2. Crear nueva contraseña para "CocosBot"
3. Copiar la contraseña generada (sin espacios)

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

## 🔧 Troubleshooting

### Error: "Playwright browser not installed"
```bash
playwright install chromium
```

### Error de autenticación 2FA
- Verificar que la contraseña de Gmail sea **contraseña de aplicación**, no la contraseña normal
- Verificar que el email tenga acceso a la cuenta de Cocos Capital
- Revisar bandeja de spam por el código 2FA

### Timeout en operaciones
Aumentar timeout en contexto manager:
```python
with CocosCapital(..., headless=False) as cocos:
    # Si ves que la página tarda, ejecuta en modo NO headless primero
    cocos.login()
```

### Debug visual
Ejecutar con `headless=False` para ver el navegador:
```python
with CocosCapital(..., headless=False) as cocos:
    cocos.login()
    # Puedes ver qué está haciendo Playwright
```

## Testing

El proyecto incluye una suite completa de tests:

```bash
pip install -e ".[dev]"
pytest
```

**Coverage actual:** 169 tests, 59% coverage global.

## 📋 Roadmap

### Próximas features
- [ ] Soporte 2FA manual (sin Gmail)
- [ ] Modo async para operaciones concurrentes
- [ ] Webhooks para notificaciones de órdenes ejecutadas
- [ ] CLI para operaciones rápidas desde terminal
- [ ] Exportar histórico de operaciones a CSV/Excel
- [ ] Integración con frameworks de backtesting (backtrader, etc.)
- [ ] Rate limiting inteligente para evitar bloqueos
- [ ] Soporte para otros brokers argentinos (IOL, etc.)

### Mejoras técnicas
- [ ] Aumentar coverage a >80%
- [ ] CI/CD con GitHub Actions
- [ ] Documentación de API completa con Sphinx
- [ ] Type stubs para mejor autocompletado en IDEs

## 🛡️ Seguridad

### Mejores prácticas
- **Nunca** hardcodees credenciales en el código
- Usa variables de entorno o archivos `.env` (y agrega `.env` a `.gitignore`)
- Rota credenciales periódicamente
- Usa contraseñas de aplicación de Gmail (nunca la contraseña principal)
- Ejecuta en ambientes seguros (nunca en máquinas compartidas con `headless=False`)

### Responsabilidad
Este proyecto es para automatización personal. **No lo uses para**:
- Operaciones no autorizadas
- Manipulación de mercado
- Violación de términos de servicio de Cocos Capital

Usalo bajo tu propio riesgo.

## Contribución

¡Contribuciones bienvenidas! Si tenés ideas o mejoras:
1. Fork el proyecto
2. Crea un branch (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -m 'feat: nueva feature'`)
4. Push al branch (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

### Reportar bugs
Si encontrás un bug o tenés preguntas, [abrí un issue](https://github.com/PabloAlaniz/CocosBot/issues).

## 📚 Recursos

- **Artículo en Medium**: [Automatizando Cocos Capital con Python](https://medium.com/@PabloAlaniz/automatizando-cocos-capital-con-python-d3a0e389277b) — Deep dive técnico en la implementación
- **GitHub Issues**: [Reportar bugs o pedir features](https://github.com/PabloAlaniz/CocosBot/issues)
- **PyPI**: [Página del paquete](https://pypi.org/project/CocosBot/)

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT** — puedes usarlo libremente con atribución.

---

**Hecho con ☕ por [@PabloAlaniz](https://github.com/PabloAlaniz)**
