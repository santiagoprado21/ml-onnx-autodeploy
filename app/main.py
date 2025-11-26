from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np
import requests
import os
import boto3

app = FastAPI()
MODEL_URL = os.environ.get("MODEL_URL", "https://projectofinalml-santiagoprado.s3.amazonaws.com/mnist-8.onnx")
MODEL_PATH = "model.onnx"
session = None

class PredictionRequest(BaseModel):
    data: list

def append_prediction_to_s3(prediction, env):
    log_filename = f"predicciones_{env}.txt"
    bucket = "projectofinalml-santiagoprado"
    session_boto = boto3.Session(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    )
    s3 = session_boto.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket, Key=log_filename)
        content = obj['Body'].read().decode('utf-8')
    except s3.exceptions.NoSuchKey:
        content = ''
    content += str(prediction) + '\n'
    s3.put_object(Bucket=bucket, Key=log_filename, Body=content.encode('utf-8'))

@app.on_event("startup")
def load_model():
    global session
    if not os.path.exists(MODEL_PATH):
        # Descargar modelo desde S3 usando boto3
        bucket = "projectofinalml-santiagoprado"
        key = "mnist-8.onnx"
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, MODEL_PATH)
        print(f"Model downloaded from S3: {bucket}/{key}")
    session = ort.InferenceSession(MODEL_PATH)
    print(f"Model loaded successfully")

@app.post("/predict")
def predict(request: PredictionRequest):
    global session
    try:
        input_data = np.array(request.data, dtype=np.float32)
        if input_data.ndim == 1:
            input_data = np.expand_dims(input_data, 0)
        inputs = {session.get_inputs()[0].name: input_data}
        output = session.run(None, inputs)[0]
        pred = int(np.argmax(output, axis=1)[0])

        env = os.environ.get('APP_ENV', 'dev')
        append_prediction_to_s3(pred, env)

        return {"prediction": pred}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))