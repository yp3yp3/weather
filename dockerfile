FROM python:3
WORKDIR /app
COPY /gunicorn /app
RUN pip install flask requests gunicorn
EXPOSE 8081
CMD  gunicorn  wsgi:app

