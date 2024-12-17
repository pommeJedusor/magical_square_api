FROM python:3.12-alpine3.21

WORKDIR /app

COPY . .

CMD ["python", "server.py"]
