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
                "rating": <integer>,
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
                "rating": <integer>,
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