# ROADMAP - CocosBot

*Actualizado: 22 de febrero 2026*

## ✅ Completado

- [x] Arquitectura modular con servicios especializados
- [x] Autenticación con 2FA automático via Gmail
- [x] Operaciones de mercado (compra, venta, órdenes)
- [x] Consulta de portfolio y balance
- [x] Tests unitarios básicos
- [x] Publicación en PyPI
- [x] Script de discovery de endpoints
- [x] CI/CD básico con GitHub Actions
- [x] Artículo en Medium

## 🎯 Próximos pasos (v1.1)

### Alta prioridad

- [ ] **Aumentar coverage a 80%**
  - Tests de integración para auth flow
  - Mocks más completos para market service
  - Edge cases en validators

- [ ] **CLI básico**
  ```bash
  cocos login
  cocos portfolio
  cocos balance
  cocos buy GGAL 10
  cocos sell AL30 5 --limit 50000
  ```

### Media prioridad

- [ ] **Exportar histórico de operaciones**
  - CSV con todas las operaciones
  - Formato compatible con Excel
  - Filtros por fecha/ticker

- [ ] **2FA alternativo**
  - Input manual de código cuando Gmail no disponible
  - Opción de guardar sesión (con warning de seguridad)

### Baja prioridad

- [ ] **Rate limiting inteligente**
  - Detectar patrones de throttling
  - Backoff exponencial automático
  - Logs de requests para debug

## 🔮 Futuro (v2.0)

- [ ] Soporte multi-broker (IOL, Balanz, Bull Market)
- [ ] Alertas de precio via Telegram/webhook
- [ ] Backtesting de estrategias
- [ ] Dashboard web standalone
- [ ] API REST wrapper local

## 📊 Métricas objetivo

| Métrica | Actual | Target |
|---------|--------|--------|
| Test coverage | 59% | 80% |
| Tests | 169 | 200+ |
| Documentación | ✅ | ✅ |
| PyPI downloads/mes | ? | Monitorear |

## 🏷️ Versiones

- **v1.0**: Release actual (PyPI)
- **v1.1**: CLI + coverage 80%
- **v2.0**: Multi-broker + alertas
