const http = require("http");
const { buildMonthlyReport } = require("./report");
const { loadPlugins } = require("./plugins");

const plugins = loadPlugins();

http
  .createServer(async (req, res) => {
    const match = req.url.match(/^\/customers\/(\d+)\/monthly-report$/);
    if (!match) {
      res.writeHead(404).end();
      return;
    }
    const invoiceIds = Array.from({ length: 40 }, (_, i) => Number(match[1]) * 100 + i);
    const report = await buildMonthlyReport(Number(match[1]), invoiceIds);
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ ...report, plugins: plugins.length }));
  })
  .listen(3000);
