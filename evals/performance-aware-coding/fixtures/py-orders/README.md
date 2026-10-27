# py-orders

Admin dashboard for a small shop. `GET /dashboard` calls `shop.reports.dashboard_report()` on every page load; ops notes put peak traffic at about 30 dashboard loads a minute. The `orders` table grows by roughly 5,000 rows a day and is never archived.

```sh
python3 seed.py            # creates shop.db: 2,000 customers, 20,000 orders, 200 products
python3 bench.py           # builds the dashboard report once
```

Production uses the same SQLite file on the app server.
