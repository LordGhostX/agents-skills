const { buildMonthlyReport } = require("./report");

const invoiceIds = Array.from({ length: 40 }, (_, i) => 4200 + i);
buildMonthlyReport(42, invoiceIds).then((report) => console.log(report.rows.length, "rows"));
