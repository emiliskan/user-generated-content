# Запуск etl

## Установить сертификаты Yandex Cloud ClickHouse

### Linux:

``` 
sudo mkdir -p /usr/local/share/ca-certificates/Yandex && \
sudo wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O /usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt && \
sudo chmod 655 /usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt 
```
### Windows:

```
mkdir -Force $HOME\.clickhouse; `
(Invoke-WebRequest https://storage.yandexcloud.net/cloud-certs/CA.pem).RawContent.Split([Environment]::NewLine)[-31..-1] `
  | Out-File -Encoding ASCII $HOME\.clickhouse\YandexInternalRootCA.crt; `
Import-Certificate `
  -FilePath  $HOME\.clickhouse\YandexInternalRootCA.crt `
  -CertStoreLocation cert:\CurrentUser\Root
```

## Установить сертификаты Yandex Cloud Kafka

### Linux:

``` 
sudo mkdir -p /usr/local/share/ca-certificates/Yandex && \
sudo wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O /usr/local/share/ca-certificates/Yandex/YandexCA.crt && \
sudo chmod 655 /usr/local/share/ca-certificates/Yandex/YandexCA.crt
```
### Windows:

```
mkdir $HOME\.kafka; curl.exe -o $HOME\.kafka\YandexCA.crt https://storage.yandexcloud.net/cloud-certs/CA.pem
```

## Добавить в переменные окружения выше указанные адреса к установленным сертификатам
Пример (windows):
```
CLICKHOUSE_SSL_CAFILE=C:/users/user_name/.clickhouse/YandexInternalRootCA.crt
KAFKA_SSL_CAFILE=C:/Users/user_name/.kafka/YandexCA.crt
```

## Запуск

```
python etl.py
```