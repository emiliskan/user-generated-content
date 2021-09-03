FROM python:3.9

ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PATH="${PATH}:/root/.local/bin"

RUN apt update && apt -y upgrade && apt install -y python3-setuptools netcat
RUN pip install pipenv

# Prepearing cert for Kafka
RUN apt install -y wget && \
mkdir -p /usr/local/share/ca-certificates/Yandex/ && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O /usr/local/share/ca-certificates/Yandex/YandexCA.crt && \
chmod 655 /usr/local/share/ca-certificates/Yandex/YandexCA.crt

RUN mkdir /app
WORKDIR /app/
COPY / /app/

RUN pipenv install --system --deploy --skip-lock

ENTRYPOINT ["python", "/app/main.py"]