# Sistema de Despliegue Automático para Modelos ONNX

Sistema completo de CI/CD para despliegue automático de modelos de Machine Learning en formato ONNX, con endpoints separados para desarrollo y producción.

## 🎯 Propósito del Proyecto

Este repositorio implementa un **sistema de despliegue automático (MLOps)** que permite actualizar modelos de Machine Learning en producción de forma segura, rápida y sin intervención manual.

### Problema que resuelve

En producción, actualizar modelos ML manualmente es:
- ⏱️ **Lento**: Puede tomar horas de trabajo manual
- 🐛 **Propenso a errores**: Riesgo de romper el servicio
- 💰 **Costoso**: Requiere personal DevOps dedicado
- 🔄 **No escalable**: Difícil de mantener con múltiples modelos

### Solución propuesta

Un pipeline automatizado que:
- ✅ **Prueba** el modelo antes de desplegarlo
- ✅ **Despliega** automáticamente si pasa las pruebas
- ✅ **Separa** entornos de desarrollo y producción
- ✅ **Registra** todas las predicciones para monitoreo
- ✅ **Funciona 24/7** sin intervención humana

### Caso de uso

**Modelo implementado:** Clasificador de dígitos manuscritos (MNIST)
- **Entrada:** Imagen de 28x28 píxeles (784 valores)
- **Salida:** Dígito reconocido (0-9)
- **Aplicación real:** Reconocimiento de números en cheques, formularios, documentos escaneados

## 🏗️ Arquitectura del Sistema

### Componentes principales

```

![Diagrama de arquitectura](assets/MLFinalProject.png)

```

### Tecnologías utilizadas

- **Modelo ONNX**: Almacenado en S3, descargado dinámicamente (nunca en el repo)
- **Datos de prueba**: En S3, descargados en pipeline CI/CD
- **Logs de predicción**: Guardados automáticamente en S3 (`predicciones_dev.txt`, `predicciones_prod.txt`)
- **API**: FastAPI sirviendo predicciones del modelo
- **Contenedores**: Docker + AWS ECR
- **Orquestación**: AWS ECS Fargate
- **CI/CD**: GitHub Actions

## 📁 Estructura del Repositorio

```
/
├── .github/workflows/
│   └── test-and-deploy.yml    # Pipeline CI/CD
├── app/
│   ├── main.py                # API FastAPI
│   └── requirements.txt       # Dependencias Python
├── docker/
│   └── Dockerfile             # Imagen del contenedor
├── scripts/
│   ├── download_model.py      # Descarga modelo desde S3
│   ├── download_data.py       # Descarga datos de prueba
│   └── upload_prediction_log.py
├── tests/
│   └── test_model.py          # Tests unitarios
└── README.md
```

## 🚀 Pipeline CI/CD

### Ramas y Endpoints

| Rama | Servicio ECS | Endpoint | Archivo de logs |
|------|-------------|----------|-----------------|
| `dev` | api-dev | http://44.210.82.145 | predicciones_dev.txt |
| `prod` | api-prod | http://34.204.77.202 | predicciones_prod.txt |

### Etapas del Pipeline

**1. Test**
- Descarga modelo ONNX desde S3
- Descarga datos de prueba desde S3
- Ejecuta pruebas unitarias:
  - Verifica que el modelo responde correctamente
  - Valida métricas de rendimiento

**2. Build & Deploy**
- Construye imagen Docker
- Sube imagen a AWS ECR
- Actualiza servicio ECS correspondiente (dev o prod)

## ⚙️ Configuración Inicial

### 1. Recursos AWS

**S3 Bucket** (`projectofinalml-santiagoprado`):
```
modelo.onnx
test_data.csv
test_labels.csv
predicciones_dev.txt (vacío inicial)
predicciones_prod.txt (vacío inicial)
```

**ECR Repositories**:
- `ml-onnx-autodeploy-dev`
- `ml-onnx-autodeploy-prod`

**ECS Cluster**: `ml-autodeploy-cluster`

**ECS Services**:
- `api-dev` (con variable `APP_ENV=dev`)
- `api-prod` (con variable `APP_ENV=prod`)

### 2. Secrets de GitHub

En Settings > Secrets > Actions, agregar:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_ID
AWS_DEFAULT_REGION (ej: us-east-1)
```

### 3. Variables de Entorno

```bash
MODEL_URL=https://projectofinalml-santiagoprado.s3.amazonaws.com/mnist-8.onnx
TEST_DATA_URL=https://projectofinalml-santiagoprado.s3.amazonaws.com/test_data.csv
TEST_LABELS_URL=https://projectofinalml-santiagoprado.s3.amazonaws.com/test_labels.csv
APP_ENV=dev  # o prod
AWS_ACCESS_KEY_ID=tu-key
AWS_SECRET_ACCESS_KEY=tu-secret
AWS_DEFAULT_REGION=us-east-1
```

## 🧪 Uso Local

### Instalar dependencias
```bash
pip install -r app/requirements.txt pytest
```

### Descargar modelo y datos
```bash
export MODEL_URL=https://projectofinalml-santiagoprado.s3.amazonaws.com/mnist-8.onnx
python scripts/download_model.py
python scripts/download_data.py
```

### Ejecutar tests
```bash
pytest tests/
```

### Correr API localmente
```bash
export APP_ENV=dev
uvicorn app.main:app --reload
```

### Hacer predicción
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [0.1, 0.2, ..., 0.5]}'  # 784 valores para MNIST
```

**Respuesta esperada:**
```json
{
  "prediction": 7
}
```

### Probar endpoints en vivo
```bash
python test_endpoints.py
```

**Output:**
```
==================================================
PROBANDO ENDPOINTS ML
==================================================

🔵 Probando endpoint DEV...
Status: 200
Respuesta: {'prediction': 7}

🟢 Probando endpoint PROD...
Status: 200
Respuesta: {'prediction': 3}

==================================================
✅ Pruebas completadas
==================================================
```

## 🔄 Flujo de Trabajo Completo

### Ciclo de vida del despliegue

```
1. Desarrollador hace cambios en código
   ↓
2. git push origin dev
   ↓
3. GitHub Actions detecta el push
   ↓
4. ETAPA TEST:
   - Descarga modelo desde S3
   - Descarga datos de prueba desde S3
   - Ejecuta tests unitarios
   - ¿Pasan? → Continúa | ¿Fallan? → Detiene pipeline
   ↓
5. ETAPA BUILD:
   - Construye imagen Docker
   - Etiqueta con SHA del commit
   - Sube imagen a AWS ECR
   ↓
6. ETAPA DEPLOY:
   - Actualiza servicio ECS (api-dev)
   - ECS descarga nueva imagen
   - Reemplaza contenedor antiguo
   - Endpoint actualizado (sin downtime)
   ↓
7. Usuario hace request a /predict
   ↓
8. API procesa y devuelve predicción
   ↓
9. Predicción se guarda en S3 (predicciones_dev.txt)
```

### Promoción a producción

1. **Desarrollo**: Hacer cambios en rama `dev`
2. **Push**: `git push origin dev`
3. **CI/CD automático**: Tests + Build + Deploy a dev
4. **Validación**: Probar endpoint dev
5. **Promoción a prod**: Merge `dev` → `prod`
6. **Deploy prod**: Pipeline actualiza `api-prod`

## 📊 Monitoreo

Cada predicción se registra automáticamente en S3:
- `predicciones_dev.txt`: logs del endpoint dev
- `predicciones_prod.txt`: logs del endpoint prod

Formato: una predicción por línea.

## 🛠️ Troubleshooting

**Error: Unable to assume service linked role**
```bash
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
```

**Error: No images found in ECR**
- Hacer push inicial manual o esperar primer pipeline exitoso

**Error: boto3 credentials**
- Verificar variables de entorno AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY

## 📝 Requisitos Cumplidos

✅ Repositorio GitHub con CI/CD  
✅ Dos ramas (dev y prod) con endpoints separados  
✅ Etapa test: descarga modelo/datos, ejecuta pruebas  
✅ Etapa build/promote: construye y despliega contenedor  
✅ Modelo ONNX NO en repo, solo referencia  
✅ Datos de prueba descargados dinámicamente  
✅ Logs de predicción en archivos TXT en S3  
✅ Pipeline ejecuta en cada push a dev/prod  

## 📚 Tecnologías

- Python 3.10
- FastAPI
- ONNX Runtime
- Docker
- AWS (S3, ECR, ECS, Fargate)
- GitHub Actions
- boto3

## 👤 Autor

Santiago Prado - Proyecto Final ML
