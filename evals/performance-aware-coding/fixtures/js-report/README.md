# js-report

Billing service. `GET /customers/:id/monthly-report` calls `buildMonthlyReport()` in `report.js`. A customer has 20 to 60 invoices a month. The billing API (`api.js`, stubbed here with a fixed delay) allows 20 concurrent requests per client.

```sh
node bench.js              # builds one 40-invoice report
node server.js             # serves the endpoint on :3000
```
