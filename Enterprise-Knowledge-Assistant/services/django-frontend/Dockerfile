FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY services/django-frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/django-frontend/project /app/project
RUN useradd -m appuser && chown -R appuser /app
USER appuser
WORKDIR /app/project
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]