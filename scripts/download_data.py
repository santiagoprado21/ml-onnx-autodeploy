import requests
import os

test_data_url = os.environ.get("TEST_DATA_URL", "https://projectofinalml-santiagoprado.s3.amazonaws.com/test_data.csv")
test_labels_url = os.environ.get("TEST_LABELS_URL", "https://projectofinalml-santiagoprado.s3.amazonaws.com/test_labels.csv")

def download(url, dest):
    r = requests.get(url)
    with open(dest, "wb") as f:
        f.write(r.content)
    print(f"Descargado {dest}")

download(test_data_url, "test_data.csv")
download(test_labels_url, "test_labels.csv")