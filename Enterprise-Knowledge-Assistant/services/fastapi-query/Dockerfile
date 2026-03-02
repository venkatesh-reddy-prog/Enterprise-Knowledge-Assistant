FROM python:3.11-slim
WORKDIR /app
COPY services/fastapi-query/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/fastapi-query/app /app/app
COPY services/shared /app/services/shared
RUN touch /app/services/__init__.py
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100", "--reload"]