import os
import sys
import numpy as np
import onnxruntime as ort
import requests

MODEL_URL = os.environ.get("MODEL_URL", "https://projectofinalml-santiagoprado.s3.amazonaws.com/mnist-8.onnx")
MODEL_PATH = "test_model.onnx"

def download():
    if not os.path.exists(MODEL_PATH):
        r = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)

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
