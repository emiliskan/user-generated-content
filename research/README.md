## Тестирование производительности Clickhouse и Vertica

Структура тестовой таблицы **events**

| имя столбца    | тип данных |
| -----------    | -----------|
| id             | UUID       |
| user_id        | UUID       |
| movie_id       | UUID       |
| viewed_frame   | Int        |
| event_time     | DATETIME   |

### Загрузка тестовых данных

### Выполнение запросов к БД