var { Web3 } = require('web3');
const fs = require('fs');

const web3 = new Web3('http://localhost:8545');

const jsonData = fs.readFileSync('./build/contracts/FlexCoin.json');
const contractData = JSON.parse(jsonData);
const abi = contractData.abi;

const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

readline.question("What is the contract address? - FlexCoin: ", function(address) {
    const FlexCoin = new web3.eth.Contract(abi, address);
    const numAccounts = 5;

    const newAccounts = [];
    for (let i = 0; i < numAccounts; i++) {
        const newAccount = web3.eth.accounts.create();
        web3.eth.accounts.wallet.add(newAccount);
        newAccounts.push(newAccount);
    }

    console.log(`Created ${numAccounts} new accounts:`);
    newAccounts.forEach((account, index) => {
        console.log(`Account ${index + 1}:`, account.address);
    });

    FlexCoin.methods.numHouses().call()
        .then(numHouses => {
            console.log("Number of houses:", numHouses);
            console.log("Number of nodes:", web3.eth.accounts.length);
            console.log("Accounts:", web3.eth.accounts);

            if (numHouses === 0) {
                for (let i = 0; i < web3.eth.accounts.length; i++) {
                    FlexCoin.methods.newHouse().send({ from: web3.eth.accounts[i] })
                        .then(() => {
                            console.log("House made for node:", i);
                        })
                        .catch(error => {
                            console.error("Error making house for node:", i, error);
                        });
                }
            }
        })
        .catch(error => {
            console.error("Error:", error);
        })
        .finally(() => {
            readline.close();
        });
});
