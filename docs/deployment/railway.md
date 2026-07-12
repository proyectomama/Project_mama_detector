# Despliegue — Railway (borrador)

> **Estado: plan aparte pendiente.** Este documento captura lo aprendido y la configuración
> objetivo, pero la configuración final (`railway.json` por servicio, variables reales,
> dominios) todavía no está definida. No usar como guía de despliegue en producción sin
> revisarlo primero.

## Plan de Railway

- Plan **Hobby (US$5/mes)** o el **trial** gratuito son suficientes para desplegar los 5
  servicios de `mama-detector`. **No hace falta el plan Pro** para este alcance (5 servicios
  livianos, FastAPI + uvicorn, sin GPU).

## Topología

- **5 servicios**, cada uno buildea su propia imagen desde su `Dockerfile`
  (`services/<nombre>/Dockerfile`): `mammography`, `histopathology`, `genomics`, `fusion`,
  `gateway`. Esto refleja `infra/docker-compose.yml`, usado hoy para el equivalente local.
- Los servicios se comunican entre sí por la **red interna de Railway**, usando el hostname
  `*.railway.internal` que Railway asigna a cada servicio del mismo proyecto (equivalente al
  DNS por nombre de servicio de Docker Compose en local).
- **Solo `gateway` se expone públicamente** (dominio público de Railway o dominio propio); el
  resto de los servicios permanecen en red interna, sin puerto público. Esto es coherente con el
  diseño (ver [`../architecture/overview.md`](../architecture/overview.md)): el gateway es la
  única superficie pública del sistema.

## Variables de entorno

`gateway` necesita apuntar a los 4 servicios internos vía las mismas variables que ya usa
localmente (`services/gateway/app/config.py`), pero con los hosts `*.railway.internal` de cada
servicio desplegado:

| Variable | Servicio destino |
|---|---|
| `MAMMOGRAPHY_URL` | `mammography` |
| `HISTOPATHOLOGY_URL` | `histopathology` |
| `GENOMICS_URL` | `genomics` |
| `FUSION_URL` | `fusion` |

Ejemplo (host interno ilustrativo, a confirmar al desplegar):

```
MAMMOGRAPHY_URL=http://mammography.railway.internal:8000
HISTOPATHOLOGY_URL=http://histopathology.railway.internal:8000
GENOMICS_URL=http://genomics.railway.internal:8000
FUSION_URL=http://fusion.railway.internal:8000
```

## Pendiente (plan aparte)

- Definir `railway.json` (o configuración equivalente en el dashboard) por servicio: build desde
  Dockerfile, puerto interno, health check (`GET /health`, ya implementado en los 5 servicios).
- Definir si cada servicio vive como un "service" separado dentro de un mismo proyecto Railway
  (recomendado, para compartir la red interna) o como proyectos distintos.
- Definir manejo de secretos/variables por entorno (staging vs. producción académica).
- Definir dominio público final de `gateway` y, si aplica, HTTPS/CORS.
- Este documento se actualizará cuando exista ese plan de despliegue formal; hasta entonces, el
  despliegue de referencia para desarrollo y demos es el local (ver siguiente sección y
  [`../runbook.md`](../runbook.md)).

## Alternativa local (sin Railway, sin Docker)

Para desarrollo o demo sin infraestructura en la nube, correr los 5 servicios como procesos
`uv run uvicorn` en paralelo, cada uno en su propio puerto, tal como se documenta en
[`../runbook.md`](../runbook.md#alternativa-sin-docker-5-procesos-uv-run-uvicorn).
