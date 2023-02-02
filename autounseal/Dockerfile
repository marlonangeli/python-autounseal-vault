FROM python:3.10-slim-bullseye

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir requests

ENV VAULT_ADDR http://vault:8200
ENV KEYS_PATH /run/secrets/keys
ENV INTERVAL 60

COPY . /app
WORKDIR /app

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
