import os
import requests

MODEL_URL = os.environ.get("MODEL_URL", "https://projectofinalml-santiagoprado.s3.amazonaws.com/mnist-8.onnx")
MODEL_PATH = os.environ.get("MODEL_PATH", "model.onnx")

r = requests.get(MODEL_URL)
with open(MODEL_PATH, "wb") as f:
    f.write(r.content)
print(f"Downloaded model to {MODEL_PATH}")
