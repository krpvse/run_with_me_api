FROM python:3.10

WORKDIR /api

COPY requirements-main.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements-main.txt

COPY .env .
COPY . .

CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
