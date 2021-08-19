CREATE DATABASE IF NOT EXISTS db_ucg ON CLUSTER 'company_cluster';

CREATE TABLE IF NOT EXISTS db_ucg.movies_progress ON CLUSTER 'company_cluster' (
    id UUID DEFAULT generateUUIDv4(),
    user_id      UUID,
    movie_id     UUID,
    viewed_frame INTEGER,
    event_time DateTime
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/table', '{replica}')
PARTITION BY toDateTime(event_time)
ORDER BY (id);

CREATE TABLE IF NOT EXISTS db_ucg.movies_progress_distr ON CLUSTER 'company_cluster' AS db_ucg.movies_progress
ENGINE = Distributed('company_cluster', db_ucg, movies_progress, id);