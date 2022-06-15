# Clickhouse vs. DuckDB benchmarks on local

This project benchmarks two simple queries against ~1.2GB of Parquet data in Clickhouse and DuckDB. It imports the data into each datastore and runs the benchmarks as native queries. It runs all benchmark iterations in the same session and does not reset caches.

Warning: I put the benchmark together pretty quickly, it hasn't been code reviewed, it only covers two queries, and I ran it all on my local.

## Results

**Disk usage:**

```
Raw parquet: 1.2G
Clickhouse: 2.2G
DuckDB: 7.1G
```

**Benchmarks:**

```
duckdb:groupby:         avg=4.575s min=4.527s max=4.717s (10 runs)
clickhouse:groupby:     avg=0.729s min=0.707s max=0.784s (10 runs)
duckdb:self-join:       avg=1.741s min=1.646s max=1.832s (10 runs)
clickhouse:self-join:   avg=0.711s min=0.698s max=0.737s (10 runs)
```

## Setup

1. Download data (~1GB of [NYC taxi data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page))

```shell
mkdir -p data
cd data
curl https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv -o taxi_zone_lookup.csv
curl -O https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_2022-01.parquet
curl -O https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_2022-02.parquet
curl -O https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_2022-03.parquet
cd ..
```

2. Install and run Clickhouse ([source](https://clickhouse.com/docs/en/quick-start)):

```shell
mkdir -p clickhouse
cd clickhouse
curl https://clickhouse.com/ | sh
./clickhouse server
```

3. In a new tab, import data into Clickhouse:

```shell
cd ..
./clickhouse/clickhouse client --queries-file clickhouse_create_trips.sql
./clickhouse/clickhouse client --max_memory_usage 0 --query='INSERT INTO trips FORMAT Parquet' < data/fhvhv_tripdata_2022-01.parquet
./clickhouse/clickhouse client --max_memory_usage 0 --query='INSERT INTO trips FORMAT Parquet' < data/fhvhv_tripdata_2022-02.parquet
./clickhouse/clickhouse client --max_memory_usage 0 --query='INSERT INTO trips FORMAT Parquet' < data/fhvhv_tripdata_2022-03.parquet
```

4. Install DuckDB:

```shell
mkdir -p duckdb
cd duckdb
# For Intel Mac. For ARM and Linux, see: https://duckdb.org/docs/installation/index
curl -O -L https://github.com/duckdb/duckdb/releases/download/v0.3.2/duckdb_cli-osx-amd64.zip
unzip duckdb_cli-osx-amd64.zip
cd ..
```

5. Insert data into DuckDB:

```shell
./duckdb/duckdb ./duckdb/db.duckdb -c "CREATE TABLE trips AS SELECT * FROM read_parquet('data/fhvhv_tripdata_2022-01.parquet')"
./duckdb/duckdb ./duckdb/db.duckdb -c "INSERT INTO trips SELECT * FROM read_parquet('data/fhvhv_tripdata_2022-02.parquet')"
./duckdb/duckdb ./duckdb/db.duckdb -c "INSERT INTO trips SELECT * FROM read_parquet('data/fhvhv_tripdata_2022-03.parquet')"
```

6. Run the benchmark

```shell
poetry install
poetry run python benchmark.py
```

7. Compute data size on disk

```
echo "Raw parquet:" && du -hs data
echo "Clickhouse:" && du -hs clickhouse/store
echo "DuckDB:" && du -hs duckdb/db.duckdb
```
