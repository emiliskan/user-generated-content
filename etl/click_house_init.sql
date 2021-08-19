CREATE TABLE IF NOT EXISTS db_ucg.movies_progress (
    id UUID DEFAULT generateUUIDv4(),
    user_id      UUID,
    movie_id     UUID,
    viewed_frame INTEGER,
    event_time DateTime
)
ENGINE = MergeTree()
PARTITION BY toDateTime(event_time)
ORDER BY (id);
