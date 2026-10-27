"""Create shop.db with a realistic volume. Deterministic, so runs are comparable."""
import random

from shop.db import DB_PATH, connect

CUSTOMERS, ORDERS, PRODUCTS = 2_000, 20_000, 200


def main():
    DB_PATH.unlink(missing_ok=True)
    rng = random.Random(42)
    conn = connect()
    conn.executemany(
        "INSERT INTO customers (id, name) VALUES (?, ?)",
        [(i, f"Customer {i}") for i in range(1, CUSTOMERS + 1)],
    )
    conn.executemany(
        "INSERT INTO orders (customer_id, product, amount, region) VALUES (?, ?, ?, ?)",
        [
            (
                rng.randint(1, CUSTOMERS),
                f"product-{rng.randint(1, PRODUCTS)}",
                round(rng.uniform(5, 500), 2),
                rng.choice(("eu", "us", "apac")),
            )
            for _ in range(ORDERS)
        ],
    )
    conn.commit()
    print(f"seeded {DB_PATH.name}: {CUSTOMERS} customers, {ORDERS} orders")


if __name__ == "__main__":
    main()
