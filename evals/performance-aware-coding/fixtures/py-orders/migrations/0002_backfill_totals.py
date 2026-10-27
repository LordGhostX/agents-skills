"""One-off: fill orders.total_usd for rows created before the column existed.

Run once by hand during the 2026-09 release; kept for the record.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shop.db import connect  # noqa: E402
from shop.rates import rate_for  # noqa: E402


def main():
    conn = connect()
    rows = conn.execute("SELECT id, amount, region FROM orders WHERE total_usd IS NULL").fetchall()
    for order_id, amount, region in rows:
        conn.execute("UPDATE orders SET total_usd = ? WHERE id = ?", (amount * rate_for(region), order_id))
    conn.commit()
    print(f"backfilled {len(rows)} orders")


if __name__ == "__main__":
    main()
