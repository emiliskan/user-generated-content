FROM python:3.9-slim

WORKDIR opt/etl

COPY ./Pipfile /opt/etl/Pipfile
RUN apt update && apt install -y wget && pip install pipenv && \
 pipenv install --system --deploy --skip-lock && \
 mkdir -p /var/log/ugc/ && \
 mkdir -p /usr/local/share/ca-certificates/Yandex && \
 wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
 -O /usr/local/share/ca-certificates/Yandex/YandexCA.crt && \
 chmod 655 /usr/local/share/ca-certificates/Yandex/YandexCA.crt
ENV PYTHONUNBUFFERED 1
ENV CLICKHOUSE_SSL_CAFILE "/usr/local/share/ca-certificates/Yandex/YandexCA.crt"
ENV KAFKA_SSL_CAFILE "/usr/local/share/ca-certificates/Yandex/YandexCA.crt"

COPY . etl/
CMD ["python3", "-u", "./etl/etl.py"]