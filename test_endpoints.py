import requests
import numpy as np

# IPs de los endpoints (puerto 80)
DEV_URL = "http://18.234.129.236/predict"
PROD_URL = "http://44.220.63.40/predict"  # Actualizar con la IP correcta de prod

# Generar datos de prueba (imagen MNIST de 28x28 = 784 valores)
# MNIST espera forma (1, 1, 28, 28) = batch, canales, altura, ancho
test_image = np.random.rand(1, 1, 28, 28).astype(np.float32)
test_data = test_image.flatten().tolist()  # Aplanamos para enviar como lista

print("=" * 50)
print("PROBANDO ENDPOINTS ML")
print("=" * 50)

# Probar DEV
print("\n🔵 Probando endpoint DEV...")
try:
    response = requests.post(DEV_URL, json={"data": test_data}, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Probar PROD
print("\n🟢 Probando endpoint PROD...")
try:
    response = requests.post(PROD_URL, json={"data": test_data}, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("✅ Pruebas completadas")
print("Verifica los logs en S3:")
print("  - predicciones_dev.txt")
print("  - predicciones_prod.txt")
print("=" * 50)

