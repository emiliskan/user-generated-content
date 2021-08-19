# Тестирование производительности Clickhouse и Vertica

Структура тестовой таблицы **events**

| имя столбца    | тип данных |
| -----------    | -----------|
| id             | UUID       |
| user_id        | UUID       |
| movie_id       | UUID       |
| viewed_frame   | Int        |
| event_time     | DATETIME   |

## Результаты тестов:

### ClickHouse

Tests results without load:

| test_type            | total time | average time |
| -------------------- | -----------| ------------ |
| unique_user_exact    | 0.363      | 0.036        |
| unique_movies_exact  | 0.346      | 0.035        |
| unique_movies_count  | 0.340      | 0.034        |
| unique_users_count   | 0.334      | 0.033        |
| user_stat            | 0.897      | 0.090        |

Tests results under load:

| test_type            | total time | average time |
| -------------------- | -----------| ------------ |
| unique_user_exact    | 0.462      | 0.046        |
| unique_movies_exact  | 0.456      | 0.046        |
| unique_movies_count  | 0.444      | 0.044        |
| unique_users_count   | 0.438      | 0.044        |
| user_stat            | 1.322      | 0.132        |

Total insert operation time: 280.202

### Vertica

Tests results without load:

| test_type            | total time | average time |
| -------------------- | -----------| ------------ |
| unique_user_exact    | 3.618      | 0.362        |
| unique_movies_exact  | 3.103      | 0.310        |
| unique_movies_count  | 2.092      | 0.209        |
| unique_users_count   | 2.089      | 0.209        |
| user_stat            | 4.862      | 0.486        |

Tests results under load:

| test_type            | total time | average time |
| -------------------- | -----------| ------------ |
| unique_user_exact    | 3.515      | 0.351        |
| unique_movies_exact  | 3.519      | 0.352        |
| unique_movies_count  | 2.179      | 0.218        |
| unique_users_count   | 2.186      | 0.219        |
| user_stat            | 5.559      | 0.556        |

Total insert operation time: 403.185