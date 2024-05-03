const PrivateKeyProvider = require("@truffle/hdwallet-provider");
const privateKey = "8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63";
const privateKeyProvider = new PrivateKeyProvider(
  privateKey,
  "http://localhost:8545",
);

module.exports = {
  networks: {
    besu: {
      host: "localhost",
      port: 8545,
      network_id: "*",
      from: "0xfe3b557e8fb62b89f4916b721be55ceb828dbd73",
      provider: privateKeyProvider
    },
  },
  compilers: {
    solc: {
      version: "0.4.11",
    },
  },
};