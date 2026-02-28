FROM python:3.11-slim
WORKDIR /app
RUN pip install django
COPY project /app/project
CMD ["python", "project/manage.py"]