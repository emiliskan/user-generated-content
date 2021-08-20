# Описание структуры проекта

- architecture: здесь изложено описание архитектуры всего проекта
- research: результаты исследования для выбора между ClickHouse и Vertica
- etl: сервис перегрузки данных из Kafka в ClickHouse
- ugc_api: сервис для сохранения пользовательских событий
- nginx: сервис с nginx, чтоб открыть ugc_api во внешний мир

# Запуск проекта

# Auth

Запуск сервиса авторизации:

```shell
git clone https://github.com/vctecc/Auth_sprint_2
cd Auth_sprint_2
```
Задаем **SECRET_KEY** и **JWT_SECRET_KEY**
```
docker compose up --build
```

# UGC

Запуск сервиса:

```shell
docker compose up --build
```

# ClickHouse, Kafka

ClickHouse и Kafka подняты в Yandex Cloud
Параметры соединения к ним прописаны в env файле
