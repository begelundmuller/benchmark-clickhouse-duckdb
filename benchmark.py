import clickhouse_driver
from datetime import datetime
import duckdb

# Number of times to benchmark each query
ITERATIONS = 10

# Names of queries to load from the "./queries/" folder
BENCHMARKS = ["groupby", "self-join"]


def benchmark_db(db, execute_fn):
    """ Benchmarks all queries against one datastore """
    for name in BENCHMARKS:
        # Load query
        with open(f"queries/{name}.{db}.sql") as f:
            query = f.read()
        
        # Run benchmark and track query durations
        deltas = []
        for _ in range(ITERATIONS):
            start = datetime.now()
            execute_fn(query)
            end = datetime.now()
            deltas.append((end - start).total_seconds())

        # Print result
        avg = sum(deltas) / len(deltas)
        print("{}:{}: avg={:.3f}s min={:.3f}s max={:.3f}s ({} runs)".format(
            db,
            name,
            avg,
            min(deltas),
            max(deltas),
            ITERATIONS,
        ))


def main():
    ddb = duckdb.connect("./duckdb/db.duckdb")
    benchmark_db("duckdb", lambda query: ddb.execute(query))

    ch = clickhouse_driver.Client(host='localhost')
    benchmark_db("clickhouse", lambda query: ch.execute(query))


if __name__ == "__main__":
    main()
