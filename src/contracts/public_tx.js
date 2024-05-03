const path = require("path");
const fs = require("fs-extra");
const { Web3 } = require("web3");
const { LegacyTransaction } = require("@ethereumjs/tx");
const { Common, Hardfork } = require("@ethereumjs/common");

const host = "http://localhost:8545";

async function main() {
  const web3 = new Web3(host);
  // use an existing account, or make an account
  const privateKey =
    "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63";
  const account = web3.eth.accounts.privateKeyToAccount(privateKey);

  // read in the contracts
  const contractJsonPath = path.resolve(__dirname, "FlexCoin.json");
  const contractJson = JSON.parse(fs.readFileSync(contractJsonPath, "utf8"));
  const contractAbi = contractJson.abi;
  const contractBinPath = path.resolve(__dirname, "FlexCoin.bin");
  const contractBin = fs.readFileSync(contractBinPath);
  // initialize the default constructor with a value `47 = 0x2F`; this value is appended to the bytecode
  const contractConstructorInit =
    "000000000000000000000000000000000000000000000000000000000000002F";

  // get txnCount for the nonce value
  const txnCount = await web3.eth.getTransactionCount(account.address);

  const rawTxOptions = {
    nonce: web3.utils.numberToHex(txnCount),
    from: account.address,
    value: "0x00",
    data: "0x" + contractBin + contractConstructorInit, // contract binary appended with initialization value
    gasPrice: "0x0", //ETH per unit of gas
    gasLimit: "0x24A22", //max number of gas units the tx is allowed to use
  };

  // Creating transaction
  console.log("Creating transaction...");
  const commonWithCustomChainId = Common.custom({
    chainId: 1337,
    defaultHardfork: Hardfork.Berlin,
  });
  const tx = LegacyTransaction.fromTxData(rawTxOptions, {
    common: commonWithCustomChainId,
    allowUnlimitedInitCodeSize: true,
  });

  // Signing transaction
  console.log("Signing transaction...");
  const privateKeyArr = Buffer.from(privateKey.slice(2), "hex");
  const signedTx = tx.sign(privateKeyArr);

  // Sending transaction
  console.log("Sending transaction...");
  const serializedTx = signedTx.serialize();

  const signedTransation = "0x" + Buffer.from(serializedTx).toString("hex");

  const pTx = await web3.eth.sendSignedTransaction(signedTransation);
  console.log("tx transactionHash: " + pTx.transactionHash);
  console.log("tx contractAddress: " + pTx.contractAddress);
}

main().then(() => process.exit(0));
