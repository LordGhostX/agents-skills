// Stub of the billing API client. Each call costs one network round trip (~15 ms).
const ROUND_TRIP_MS = 15;

const wait = (value) => new Promise((resolve) => setTimeout(() => resolve(value), ROUND_TRIP_MS));

async function fetchCustomer(id) {
  return wait({ id, name: `Customer ${id}`, accountId: `acct-${id % 7}` });
}

async function fetchAccount(accountId) {
  return wait({ id: accountId, name: `Account ${accountId}`, region: "eu" });
}

async function fetchInvoice(id) {
  const lines = Array.from({ length: 25 }, (_, i) => ({
    sku: `sku-${(id * 31 + i) % 500}`,
    qty: 1 + (i % 4),
    unitPrice: 10 + ((id + i) % 90),
  }));
  return wait({ id, lines });
}

module.exports = { fetchCustomer, fetchAccount, fetchInvoice };
