# Auto-Deployment ML System (ONNX)

Este repositorio implementa un sistema de despliegue automático para modelos ONNX basado en FastAPI, Docker y AWS con pipelines CI/CD en GitHub Actions.

## Arquitectura General

- **Modelo ONNX**: Referenciado, descargado desde un bucket (ejemplo: S3 pública)
- **Dataset de prueba**: Referenciado y descargado dinámicamente
- **Logs**: Predicciones guardadas en archivos TXT en el bucket
- **Endpoints:**
    - `dev`: Rama de desarrollo, despliegue automático
    - `prod`: Rama de producción, despliegue automático

## Estructura del Repositorio

```
/
├── .github/workflows/      # Pipelines GitHub Actions (por rama)
├── app/                    # API FastAPI y lógica del modelo
├── docker/                 # Dockerfile
├── scripts/                # Scripts auxiliares (descarga modelo/datos)
├── tests/                  # Pruebas automáticas
├── README.md
```

## Pipeline CI/CD (GitHub Actions)

- **Test:** Descarga modelo/dataset y corre pruebas automáticas.
- **Build/Promote:** Construye imagen Docker, despliega en AWS.

## Variables Importantes

- `MODEL_URL`: Enlace al modelo ONNX
- `TEST_DATA_URL`: Enlace a datos de prueba
- `PREDICTIONS_LOG_S3`: Ruta/URL bucket S3 para logs

## Próximos pasos
- Poblar código fuente en `app/`, scripts y workflows en `/github/workflows`
- Subir variables a GitHub Secrets para CI/CD
- Adaptar Dockerfile y configuración infraestructura automatizada
