### Задачи исследования
Измерить скорость добавления и чтения данных хранилища при следующих требованиях: 
- количество пользователей: 500000
- количество фильмов: 20000
- максимальное время ответа: 200мс

### Выводы исследования
MongoDB удовлетворяет требуемым показателям производительности и может быть использовано
для хранения пользовательских оценок и отзывов.

### Структура данных

БД разделена на следующие коллекции:

- **user_bookmarks**
    - схема данных:
      
            {
                "_id": <uuid_string>,
                "bookmarks": [<uuid_string>, ...]
            }    
    - ключ шардирования: **_id**
    
- **movie_scores**
    - схема данных:
      
            {
                "_id": <uuid_string>,
                "movie_id": <uuid_string>,
                "user_id": <uuid_string>,
                "score": <integer>
            }  
    - ключ шардирования: **movie_id**
    
- **movies**
    - схема данных:
      
            {
                "_id": <uuid_string>,
                "rating": <double>,
                "scores_quality": <integer>,
                "scores": [<uuid_string>, ...],
                "reviews": [<uuid_string>, ...]
            }
    - не шардируется
    
- **reviews**
    - схема данных:
      
            {
                "_id": <uuid_string>,
                "user_id": <uuid_string>,
                "movie_id": <uuid_string>,
                "pub_date": <datetime>,
                "text": <string>,
                "movie_score_id": <uuid_string>,
                "rating": <double>,
                "scores": [<uuid_string>, ...],
                "scores_quality": <integer>
            }
    - ключ шардирования: **movie_id**
    
- **review_scores**
    - схема данных:
      
            {
                "_id": <uuid_string>,
                "review_id": <uuid_string>,
                "user_id": <uuid_string>,
                "score": <integer>
            }  
    - ключ шардирования: **review_id**
    
### Результаты тестирования
- итераций теста: 10

#### Операции чтения

| получение                                     | среднее время выполнения, с |
|-----------------------------------------------|-----------------------------|
| закладок пользователя                         | 0.0018                      |
| отсортированных по дате рецензий к фильму     | 0.0041                      |
| отсортированных по оценкам рецензий к фильму  | 0.0024                      |
| популярных у пользователя фильмов             | 0.01973                     |
| популярных у пользователя рецензий            | 0.09689                     |
| количества оценок у фильма                    | 0.0014                      |
| списка положительных рецензий на фильм        | 0.0021                      |

#### Операции записи

| добавление            | среднее время выполнения, с |
|-----------------------|-----------------------------|
| закладки пользователю | 0.0013                      |
| рецензии к фильму     | 0.0368                      |
| оценки к рецензии     | 0.0238                      |
| оценки к фильму       | 0.0266                      |