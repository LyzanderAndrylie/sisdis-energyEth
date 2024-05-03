const fs = require("fs").promises;
const solc = require("solc");

const solidityVersion = "v0.4.11+commit.68ef5810";

async function main() {
  // Load the contract source code
  const sourceCode = await fs.readFile("FlexCoin.sol", "utf8");
  // Compile the source code and retrieve the ABI and bytecode
  const { abi, bytecode } = await compile(sourceCode, "FlexCoin");
  // Store the ABI and bytecode into a JSON file
  const artifact = JSON.stringify({ abi, bytecode }, null, 2);
  await fs.writeFile("FlexCoin.json", artifact);
}

async function compile(sourceCode, contractName) {
  let artifact = {};

  const output = await compileByVersion(solidityVersion, sourceCode);
  artifact = JSON.parse(output).contracts.main[contractName];

  return {
    abi: artifact?.abi,
    bytecode: artifact?.evm.bytecode.object,
  };
}

async function compileByVersion(solidityVersion, sourceCode) {
  return new Promise((resolve, reject) => {
    solc.loadRemoteVersion(solidityVersion, (err, solcSnapshot) => {
      if (err) {
        console.error("Error loading compiler:", err.message);
        reject(err);
      }

      // Create the Solidity Compiler Standard Input and Output JSON
      const input = {
        language: "Solidity",
        sources: { main: { content: sourceCode } },
        settings: {
          outputSelection: { "*": { "*": ["abi", "evm.bytecode"] } },
        },
      };
      // Parse the compiler output to retrieve the ABI and bytecode
      const output = solcSnapshot.compile(JSON.stringify(input));

      resolve(output);
    });
  });
}

main().then(() => process.exit(0));
