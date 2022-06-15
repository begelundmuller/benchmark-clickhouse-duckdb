import clickhouse_driver
from datetime import datetime
import duckdb

ITERATIONS = 10
BENCHMARKS = ["groupby", "self-join"]


def read_file(path):
    with open(path) as f:
        return f.read()


def run_db(db, execute_fn):
    for name in BENCHMARKS:
        query = read_file(f"queries/{name}.{db}.sql")
        deltas = []
        for _ in range(ITERATIONS):
            start = datetime.now()
            execute_fn(query)
            end = datetime.now()
            deltas.append((end - start).total_seconds())
        avg = sum(deltas) / len(deltas)
        print("{}:{}: avg={:.3f}s min={:.3f}s max={:.3f}s ({} runs)".format(
            db,
            name,
            avg,
            min(deltas),
            max(deltas),
            ITERATIONS,
        ))


def run():
    ddb = duckdb.connect("./duckdb/db.duckdb")
    run_db("duckdb", lambda query: ddb.execute(query))

    ch = clickhouse_driver.Client(host='localhost')
    run_db("clickhouse", lambda query: ch.execute(query))


if __name__ == "__main__":
    run()
