## Resumen

<!-- Qué cambia y por qué (el porqué, no el qué — el diff ya muestra el qué). -->

Cierra #<issue>

## Checklist (Definition of Done)

Ver [`docs/psp/definition-of-done.md`](../docs/psp/definition-of-done.md) para el detalle de cada punto.

- [ ] Tests pasan (`uv run pytest` en cada servicio tocado)
- [ ] Contratos regenerados sin diff (si aplica — `packages/contracts/generate.sh`)
- [ ] Sin PHI en logs/respuestas/nombres de rama/mensajes de commit
- [ ] Disclaimer clínico presente (si la salida expone score, riesgo, BI-RADS o alerta)
- [ ] Trazabilidad actualizada (`docs/requisitos.md` y `docs/psp/traceability.md`)
- [ ] Commit(s) siguen la convención `tipo(#N): descripción`
- [ ] Cierra #<issue>

## Seguridad clínica

- **¿Este cambio afecta salida clínica o el manejo de datos sensibles (PHI)?** Sí / No
- **Si afecta, ¿fue revisado con el experto correspondiente?**
  `/mama-radiologo` | `/mama-patologo` | `/mama-gobernanza-ia` | `/mama-audit`

## Cómo probar

<!-- Comandos o pasos para verificar el cambio localmente. -->
