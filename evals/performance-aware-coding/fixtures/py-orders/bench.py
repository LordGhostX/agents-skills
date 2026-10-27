"""Build the dashboard report once against shop.db (run seed.py first)."""
from shop.db import connect
from shop.reports import dashboard_report

if __name__ == "__main__":
    report = dashboard_report(connect())
    print(len(report["lines"]), "lines,", len(report["top_products"]), "products")
