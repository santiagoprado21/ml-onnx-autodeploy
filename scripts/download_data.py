import boto3
import os

BUCKET = "projectofinalml-santiagoprado"
s3 = boto3.client('s3')

# Descargar datos de prueba
s3.download_file(BUCKET, "test_data.csv", "test_data.csv")
print("Descargado test_data.csv")

s3.download_file(BUCKET, "test_labels.csv", "test_labels.csv")
print("Descargado test_labels.csv")