# Описание структуры проекта

- architecture: здесь изложено описание архитектуры всего проекта
- research: результаты исследования для выбора между ClickHouse и Vertica
- etl: сервис перегрузки данных из Kafka в ClickHouse
- uga_api: сервис для сохранения пользовательской активности
- ugc_api: сервис для сохранения пользовательских оценок
- nginx: сервис с nginx, чтоб открыть ugc_api и uga_api во внешний мир

# CI

Для репозитория настроены CI процессы.
Все изменения проверяются на двух версиях python, линтерами flake8 и mypy и тестами pytest.
Результаты проверок выгружаются в html и публикуются в github pages.

Отчеты доступны по ссылке:
https://emiliskan.github.io/ugc_sprint_2/
>   
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

Задаем **JWT_SECRET_KEY**
```shell
docker compose up --build
```

# Хранилища и всякое
ClickHouse, Kafka и MongoDB подняты в Yandex Cloud.
Параметры соединения к ним прописаны в env файле.

Результаты тестирования MongoDB и возможно актуальную структуру БД можно найти [тут](https://github.com/emiliskan/ugc_sprint_2/blob/main/research/mongo/README.md). 
