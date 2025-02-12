FROM python:3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /gunicorn /app
EXPOSE 8081
CMD  gunicorn  wsgi:app

