FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir http-server

EXPOSE 3001

CMD ["python", "-m", "http.server", "3001"]
