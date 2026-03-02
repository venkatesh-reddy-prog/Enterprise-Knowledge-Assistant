FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY services/fastapi-ingest/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/fastapi-ingest/app /app/app
COPY services/shared /app/services/shared
RUN touch /app/services/__init__.py
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200", "--reload"]