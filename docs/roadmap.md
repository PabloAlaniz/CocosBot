# Roadmap — CocosBot

> Última actualización: 2026-02-14

## ✅ Implementado

### Autenticación
- **Login con 2FA automático** — Autenticación completa usando código 2FA vía Gmail IMAP
- **Logout seguro** — Cierre de sesión con verificación
- **Manejo de dispositivo seguro** — Prompt automático para guardar dispositivo

### Datos de Usuario
- **get_user_data()** — Datos básicos del usuario
- **get_account_tier()** — Nivel de cuenta (tier)
- **get_portfolio_data()** — Datos completos del portafolio
- **fetch_portfolio_balance()** — Balance total
- **get_linked_accounts()** — Cuentas bancarias vinculadas (ARS/USD)
- **get_academy_data()** — Contenido educativo de la academia

### Operaciones de Mercado
- **create_order()** — Crear órdenes de compra/venta con soporte para órdenes límite
- **get_ticker_info()** — Info de ticker por tipo de mercado (stocks, cedears, bonos, letras, cauciones, FCI)
- **get_orders()** — Listar órdenes pendientes y ejecutadas
- **cancel_order()** — Cancelar órdenes existentes
- **get_market_schedule()** — Horarios de apertura/cierre del mercado
- **get_mep_value()** — Valor actual del dólar MEP

### Infraestructura
- **Arquitectura modular** — Separación en core/services/utils/config
- **Context manager** — Uso con `with` statement para manejo automático de recursos
- **Interceptación de API** — Captura de responses del frontend para extraer datos
- **Sistema de logging** — Logging estructurado en todos los módulos
- **Type hints completos** — Tipado en todos los métodos públicos

### Testing y Publicación
- **Suite de tests** — 169 tests con pytest
- **Coverage 59%** — Cobertura actual del código
- **Publicado en PyPI** — `pip install CocosBot`
- **Endpoint discovery** — Script para detectar nuevos endpoints de API

---

## 🚧 En progreso

*Nada actualmente en desarrollo activo*

---

## 📋 Backlog

- [ ] **CI/CD con GitHub Actions** — Automatizar tests y releases
- [ ] **Aumentar coverage a >80%** — Más tests para edge cases y servicios
- [ ] **Soporte 2FA manual** — Alternativa sin Gmail (input manual o TOTP)
- [ ] **CLI para operaciones rápidas** — Ejecutar operaciones desde terminal
- [ ] **Exportar histórico a CSV/Excel** — Dump de transacciones y portfolio
- [ ] **Rate limiting inteligente** — Evitar bloqueos por exceso de requests

---

## 💡 Ideas

- **Alertas de precios** — Notificaciones cuando un ticker alcanza cierto valor
- **Integración con Google Sheets** — Sync automático de portfolio (ver repo Cocos-Capital-To-Google-Spreadsheet)
- **Backtesting de estrategias** — Simular operaciones con datos históricos
- **Streaming de datos** — WebSocket para precios en tiempo real
- **Multi-cuenta** — Manejar varias cuentas de Cocos Capital

---

*Generado por Brújula 🧭*
