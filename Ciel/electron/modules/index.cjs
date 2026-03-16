// Central module exports for Electron modules
const websocketClient = require('./websocket-client.cjs');
const databaseClient = require('./database-client.cjs');
const websocketHelpers = require('./websocket-helpers.cjs');
const processChecker = require('./process-checker.cjs');
const screenManager = require('./screen-manager.cjs');

module.exports = {
  websocketClient,
  databaseClient,
  websocketHelpers,
  processChecker,
  screenManager
};
