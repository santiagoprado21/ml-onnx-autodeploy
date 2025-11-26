import os
import boto3

MODEL_PATH = os.environ.get("MODEL_PATH", "model.onnx")
BUCKET = "projectofinalml-santiagoprado"
KEY = "mnist-8.onnx"

# Si hay credenciales AWS, usa boto3; si no, intenta URL pública
if os.environ.get("AWS_ACCESS_KEY_ID"):
    s3 = boto3.client('s3')
    s3.download_file(BUCKET, KEY, MODEL_PATH)
    print(f"Downloaded model from S3 using credentials to {MODEL_PATH}")
else:
    import requests
    url = f"https://{BUCKET}.s3.amazonaws.com/{KEY}"
    r = requests.get(url)
    r.raise_for_status()
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)
    print(f"Downloaded model from public URL to {MODEL_PATH}")

