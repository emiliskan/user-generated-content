CREATE DATABASE IF NOT EXISTS benchmarks_db ON CLUSTER 'company_cluster';

CREATE TABLE IF NOT EXISTS benchmarks_db.events ON CLUSTER 'company_cluster' (
    id UUID DEFAULT generateUUIDv4(),
    user_id      UUID,
    movie_id     UUID,
    viewed_frame INTEGER,
    event_time DateTime
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/table', '{replica}')
PARTITION BY toDateTime(event_time)
ORDER BY (id);

CREATE TABLE IF NOT EXISTS benchmarks_db.events_distr ON CLUSTER 'company_cluster' AS benchmarks_db.events
ENGINE = Distributed('company_cluster', benchmarks_db, events, id);