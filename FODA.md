# FODA - CocosBot

*Análisis: 22 de febrero 2026*

## 💪 Fortalezas

- **Arquitectura modular**: Separación clara entre core, services, utils y config
- **Tests completos**: 169 tests con 59% coverage global
- **Documentación**: README excelente con ejemplos, troubleshooting y guías
- **PyPI publicado**: Instalable via `pip install CocosBot`
- **Artículo en Medium**: Marketing content que trae usuarios
- **2FA automatizado**: Solución elegante con Gmail API
- **Script discovery**: Herramienta para encontrar nuevos endpoints cuando Cocos cambia
- **CI configurado**: GitHub Actions con tests en Python 3.11

## ⚠️ Debilidades

- **Coverage 59%**: Por debajo del target de 80% mencionado en roadmap
- **Dependencia Gmail obligatoria**: No hay alternativa para 2FA manual
- **Sin CLI**: Todo requiere escribir código Python
- **Sin exportación de datos**: No hay forma fácil de sacar históricos a CSV/Excel
- **Selectores CSS hardcodeados**: Vulnerables a cambios de UI

## 🚀 Oportunidades

- **CLI para operaciones rápidas**: `cocos portfolio`, `cocos buy AL30 100`
- **Integración con trading bots**: Señales automáticas, stop-loss
- **Histórico de operaciones**: Exportar a CSV para análisis fiscal
- **Dashboard web simple**: Ver portfolio sin abrir Python
- **Multi-broker**: Adaptar arquitectura para IOL, Balanz, etc.
- **Rate limiting inteligente**: Evitar bloqueos proactivamente

## 🔥 Amenazas

- **Cocos cambia endpoints**: Ya pasó una vez (por eso existe discover_endpoints.py)
- **Términos de servicio**: Cocos podría bloquear automatización
- **Playwright updates**: Breaking changes en browser automation
- **Seguridad de credenciales**: Usuarios guardan mal las keys
- **Gmail depreca app passwords**: Requeriría nueva solución 2FA
