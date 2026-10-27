const { fetchCustomer, fetchAccount, fetchInvoice } = require("./api");

const taxRates = {};
for (let i = 0; i < 500; i++) taxRates[`sku-${i}`] = (i % 20) / 100;
const SETTINGS_JSON = JSON.stringify({ currency: "EUR", rounding: 2, taxRates });

async function buildMonthlyReport(customerId, invoiceIds) {
  const customer = await fetchCustomer(customerId);
  const account = await fetchAccount(customer.accountId);

  const invoices = [];
  for (const id of invoiceIds) {
    invoices.push(await fetchInvoice(id));
  }

  const rows = [];
  for (const invoice of invoices) {
    for (const line of invoice.lines) {
      const settings = JSON.parse(SETTINGS_JSON);
      const net = line.qty * line.unitPrice;
      const tax = net * settings.taxRates[line.sku];
      rows.push({ invoice: invoice.id, sku: line.sku, total: +(net + tax).toFixed(settings.rounding) });
    }
  }
  return { customer: customer.name, account: account.name, rows };
}

module.exports = { buildMonthlyReport };
