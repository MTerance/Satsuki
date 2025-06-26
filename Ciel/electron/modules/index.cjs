// Central module exports for Electron modules
const websocketClient = require('./websocket-client.cjs');
const databaseClient = require('./database-client.cjs');
const websocketHelpers = require('./websocket-helpers.cjs');

module.exports = {
  websocketClient,
  databaseClient,
  websocketHelpers
};
