# mama-detector

Plataforma académica de apoyo a la detección temprana de cáncer de mama.
Sistema multimodal (mamografía + histopatología + genómica) con fusión de resultados.
**No es un dispositivo médico certificado.**

## Estructura

- `apps/web` — dashboard Next.js (Plan 2)
- `services/*` — microservicios FastAPI (gateway + 3 modalidades + fusión)
- `packages/contracts` — contratos compartidos (fuente de verdad de los tipos)
- `federated/` — andamiaje de federated learning (futuro)
- `infra/` — orquestación local (docker-compose)

## Correr en local

```bash
just up      # levanta todo el sistema con mocks
just test    # corre los tests de los servicios
```
