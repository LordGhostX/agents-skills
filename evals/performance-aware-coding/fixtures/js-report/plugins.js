const fs = require("fs");
const path = require("path");

// Called once when the server starts.
function loadPlugins(dir = path.join(__dirname, "plugins")) {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((file) => file.endsWith(".json"))
    .map((file) => JSON.parse(fs.readFileSync(path.join(dir, file), "utf8")));
}

module.exports = { loadPlugins };
