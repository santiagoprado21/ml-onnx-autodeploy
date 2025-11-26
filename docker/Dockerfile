FROM python:3.10-slim
WORKDIR /code
COPY ./app /code/app
COPY ./app/requirements.txt /code/app/requirements.txt
RUN pip install --no-cache-dir -r /code/app/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
