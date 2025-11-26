# Sistema de Despliegue Automático para Modelos ONNX

Sistema completo de CI/CD para despliegue automático de modelos de Machine Learning en formato ONNX, con endpoints separados para desarrollo y producción..

## 🏗️ Arquitectura

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
| `dev` | api-dev | http://54.157.149.20 | predicciones_dev.txt |
| `prod` | api-prod | http://18.234.193.125 | predicciones_prod.txt |

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

## 🔄 Flujo de Trabajo

1. **Desarrollo**: Hacer cambios en rama `dev`
2. **Push**: `git push origin dev`
3. **CI/CD automático**:
   - Tests se ejecutan
   - Si pasan, imagen Docker se construye
   - Imagen se sube a ECR
   - Servicio `api-dev` se actualiza
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
