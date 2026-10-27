"""Reports for the admin dashboard. GET /dashboard calls dashboard_report()."""
from shop.rates import rate_for

REGIONS = ("eu", "us", "apac")


def dashboard_report(conn):
    orders = conn.execute(
        "SELECT id, customer_id, product, amount, region FROM orders"
    ).fetchall()
    lines = []
    for order_id, customer_id, product, amount, region in orders:
        name = conn.execute(
            "SELECT name FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()[0]
        lines.append((order_id, name, product, amount * rate_for(region), region))
    return {
        "lines": lines,
        "top_products": top_products(lines),
        "by_region": totals_by_region(lines),
    }


def top_products(lines):
    """Largest single order (in USD) for each product."""
    top = []
    for product in sorted({line[2] for line in lines}):
        ranked = sorted(lines, key=lambda line: line[3], reverse=True)
        best = next(line for line in ranked if line[2] == product)
        top.append((product, best[0], round(best[3], 2)))
    return top


def totals_by_region(lines):
    totals = {}
    for region in REGIONS:
        totals[region] = round(sum(line[3] for line in lines if line[4] == region), 2)
    return totals
