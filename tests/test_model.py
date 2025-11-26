import os
import sys
import numpy as np
import onnxruntime as ort
import boto3

MODEL_PATH = "test_model.onnx"
BUCKET = "projectofinalml-santiagoprado"
MODEL_KEY = "mnist-8.onnx"

def download():
    if not os.path.exists(MODEL_PATH):
        s3 = boto3.client('s3')
        s3.download_file(BUCKET, MODEL_KEY, MODEL_PATH)
        print(f"Downloaded model from S3 to {MODEL_PATH}")

def test_prediction_runs():
    download()
    session = ort.InferenceSession(MODEL_PATH)
    dummy = np.random.rand(1, 1, 28, 28).astype(np.float32)
    inp = {session.get_inputs()[0].name: dummy}
    out = session.run(None, inp)
    assert out[0].shape[1] == 10  # para MNIST deben salir 10 logits

def test_max_logit_reasonable():
    download()
    session = ort.InferenceSession(MODEL_PATH)
    dummy = np.ones((1, 1, 28, 28), dtype=np.float32) * 0.5
    inp = {session.get_inputs()[0].name: dummy}
    out = session.run(None, inp)
    logits = out[0][0]
    # Ejemplo simple: el mayor logit debe estar por encima de cierto umbral
    assert logits.max() > 0.1
