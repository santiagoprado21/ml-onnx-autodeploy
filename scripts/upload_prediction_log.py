import boto3
import os
import sys

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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python upload_prediction_log.py <prediction> <env(dev|prod)>")
        sys.exit(1)
    pred = sys.argv[1]
    env = sys.argv[2]
    append_prediction_to_s3(pred, env)
    print(f"Predicción '{pred}' registrada en log {env}.")
