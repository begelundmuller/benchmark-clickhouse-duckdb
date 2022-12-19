# Clickhouse vs. DuckDB benchmarks on local

This project benchmarks two simple queries against Clickhouse and DuckDB. It imports ~1.2GB of Parquet data into each datastore and runs the benchmarks as native queries. It runs all benchmark iterations in the same session and does not reset caches.

_Warning: This is far from a rigorous benchmark._

## Results

**Benchmarks:**

```
duckdb:groupby:       avg=2.120s min=1.977s max=3.252s (10 runs)
clickhouse:groupby:   avg=0.763s min=0.737s max=0.821s (10 runs)
duckdb:self-join:     avg=2.413s min=2.392s max=2.541s (10 runs)
clickhouse:self-join: avg=1.591s min=1.575s max=1.698s (10 runs)
```

<!--
Hacking the queries to run directly on the Parquet files (uses the Clickhouse File Table engine):

```
duckdb:groupby:         avg=6.235s min=5.890s max=6.466s (10 runs)
clickhouse:groupby:     avg=10.437s min=9.150s max=11.665s (10 runs)
duckdb:self-join:       avg=3.359s min=2.847s max=4.069s (10 runs)
clickhouse:self-join:   avg=9.691s min=9.217s max=10.460s (10 runs)
```
-->

Executed on a Macbook Pro (2018) with 2.2 GHz 6-Core Intel Core i7 and 16 GB memory.

**Disk usage:**

```
Parquet:    8.1G
Clickhouse: 14.9G
DuckDB:     17.4G
```

**Executable binary size:**

```
Clickhouse: 422.7M
DuckDB:     78.3M
```

## Instructions

1. Clone this repo and `cd` into it

2. Download `High Volume For-Hire Vehicle Trip Records` dataset for the year of 2021 and 2022 (~8.1GB of [NYC taxi data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page))

```shell
mkdir -p data
cd data
curl https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv -o taxi_zone_lookup.csv
for year in {2020..2021}; do for month in {01..12}; do wget https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_${year}-${month}.parquet; done; done;
cd ..
```

3. Install and run Clickhouse ([source](https://clickhouse.com/docs/en/quick-start)):

```shell
mkdir -p clickhouse
cd clickhouse
curl https://clickhouse.com/ | sh
./clickhouse server
```

4. In a new terminal, import data into Clickhouse:

```shell
./clickhouse/clickhouse client --queries-file clickhouse_create_trips.sql
./clickhouse/clickhouse client --max_memory_usage 0 --query='INSERT INTO trips FORMAT Parquet' < data/fhvhv_tripdata_*.parquet
```

5. Install DuckDB:

```shell
mkdir -p duckdb
cd duckdb
# Works on Intel Macs (for ARM and Linux, see: https://duckdb.org/docs/installation/index)
curl -O -L https://github.com/duckdb/duckdb/releases/download/v0.6.1/duckdb_cli-osx-universal.zip
unzip duckdb_cli-osx-amd64.zip
cd ..
```

6. Insert data into DuckDB:

```shell
./duckdb/duckdb ./duckdb/db.duckdb -c "CREATE TABLE trips AS SELECT * FROM read_parquet('data/fhvhv_tripdata_*.parquet')"
```

7. Run the benchmark (requires [Poetry](https://python-poetry.org/docs/#installation)):

```shell
poetry install
poetry run python benchmark.py
```

8. Compute data size on disk:

```
echo "Parquet:" && du -hs data
echo "Clickhouse:" && du -hs clickhouse/store
echo "DuckDB:" && du -hs duckdb/db.duckdb
```

9. Compute executable size:

```
echo "Clickhouse:" && du -hs clickhouse/clickhouse
echo "DuckDB:" && du -hs duckdb/duckdb
```
