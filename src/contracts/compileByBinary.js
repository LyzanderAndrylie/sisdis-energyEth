const fs = require("fs").promises;
var solc = require("solc");

const solidityBinaryPath = "./soljson-v0.4.11+commit.68ef5810.js"

async function main() {
  // Load the contract source code
  const sourceCode = await fs.readFile("FlexCoin.sol", "utf8");
  // Compile the source code and retrieve the ABI and bytecode
  const { abi, bytecode } = await compile(sourceCode, "FlexCoin");
  // Store the ABI and bytecode into a JSON file
  const artifact = JSON.stringify({ abi, bytecode }, null, 2);
  await fs.writeFile("FlexCoin.json", artifact);
}

function compile(sourceCode, contractName) {
  // Create the Solidity Compiler Standard Input and Output JSON
  const input = {
    language: "Solidity",
    sources: { main: { content: sourceCode } },
    settings: { outputSelection: { "*": { "*": ["abi", "evm.bytecode"] } } },
  };

  // Set up specific version of the Solidity compiler
  var solcV011 = solc.setupMethods(require(solidityBinaryPath));

  // Parse the compiler output to retrieve the ABI and bytecode
  const output = solcV011.compile(JSON.stringify(input));
  const artifact = JSON.parse(output).contracts.main[contractName];
  return {
    abi: artifact.abi,
    bytecode: artifact.evm.bytecode.object,
  };
}

main().then(() => process.exit(0));
