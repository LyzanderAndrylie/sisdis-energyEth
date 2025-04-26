# Progress Document for Distributed Systems Project 2023/2024: EnergyEth

This document contains the progress made throughout the project. The purpose of this document is to showcase the tasks completed until the project is finalized.

## Table of Contents

- [Progress Document for Distributed Systems Project 2023/2024: EnergyEth](#progress-document-for-distributed-systems-project-20232024-energyeth)
  - [Table of Contents](#table-of-contents)
  - [Preparing System Requirements](#preparing-system-requirements)
    - [VirtualBox](#virtualbox)
    - [Others](#others)
  - [Downloading Hyperledger Besu](#downloading-hyperledger-besu)
  - [Running a Node for Testing](#running-a-node-for-testing)
  - [Creating a Private Network with Ethash (PoW)](#creating-a-private-network-with-ethash-pow)
  - [Deploying Smart Contracts to Ethash](#deploying-smart-contracts-to-ethash)
  - [Setting Up Web3Signer](#setting-up-web3signer)
    - [Creating a Signing Key Configuration File](#creating-a-signing-key-configuration-file)
    - [Utility](#utility)
  - [Running Prometheus and Grafana](#running-prometheus-and-grafana)
    - [PromQL Metric Query Configuration for Prometheus](#promql-metric-query-configuration-for-prometheus)
    - [Setting Up Chainlens Blockchain Explorer](#setting-up-chainlens-blockchain-explorer)
  - [Running Interaction Code](#running-interaction-code)
    - [FlexCoin](#flexcoin)
    - [Trading Mechanisms](#trading-mechanisms)
    - [LEM Simulation](#lem-simulation)

## Preparing System Requirements

### VirtualBox

To run [Hyperledger Besu](https://besu.hyperledger.org/) with a private network, we need a Linux operating system that meets the requirements listed at <https://besu.hyperledger.org/private-networks/get-started/system-requirements>.

To run Ubuntu Desktop on a VM using VirtualBox, refer to the guide at <https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview>.  

> Note: If you plan to set up Ubuntu on VirtualBox, ensure compatibility. Currently, VirtualBox 7.0.12 works well with Ubuntu 22.04.

### Others

You can also use WSL2, Docker, or dual-booting to run Hyperledger Besu. Choose the option that best suits your needs.

## Downloading Hyperledger Besu

Version: 24.3.3

Links:

1. <https://github.com/hyperledger/besu/releases/tag/24.3.3>
2. <https://yehiatarek67.medium.com/install-hyperledger-besu-on-linux-for-beginners-a5a67d1f54c7>

```shell
besu --help
```

## Running a Node for Testing

```shell
besu --config-file=./src/networks/test/config/node/test.toml
```

> **Note**: Press Ctrl+C to stop the node.

![Node Test](/screenshot/node_test.png)

## Creating a Private Network with Ethash (PoW)

Each command is executed on a different node with the working directory set to `/ethash`.

1. Start the bootnode:

  ```shell
  besu --config-file=./src/networks/ethash/config/node/bootnode.toml
  ```

  > **Note**: Run this node in a new terminal.

2. Start 2 additional nodes:

  ```shell
  besu --config-file=./src/networks/ethash/config/node/node1.toml --data-path=./src/networks/ethash/nodes/node-2/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30304
  besu --config-file=./src/networks/ethash/config/node/node2.toml --data-path=./src/networks/ethash/nodes/node-3/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30305
  ```

  > **Note**: Open 2 new terminals to run these nodes.

  > *Note*: The Enode URL for Node-1 can be viewed when running the `Start the bootnode` command.

## Deploying Smart Contracts to Ethash

To deploy, the following are required:

1. Node Package Manager (npm)
2. <https://www.npmjs.com/package/web3>
3. Truffle installed globally

> **Note**: After downloading npm, run the command `npm i` to download the required packages.

Run the following command to compile and deploy the smart contract:

```shell
truffle migrate --network besu
```

## Setting Up Web3Signer

Download Web3Signer from the link: <https://docs.web3signer.consensys.io/get-started/install-binaries>

### Creating a Signing Key Configuration File

The signing key configuration file will be used by Web3Signer during the signing process. In this project, private keys will be stored in the `keyFiles` folder, and raw unencrypted files will be used as the signing key configuration file for simplicity. This means the generated private keys are not secure and are only used for this project!

> **Note**: You do not need to follow steps 1 and 2 below as private keys are already provided in this repository. These steps are for creating new private keys if needed.

1. Generate a private key in the secp256k1 format.

```shell
# generate a private key
openssl ecparam -name secp256k1 -genkey -noout -out ./keyFiles/ec-secp256k1-private.pem

# extract the public key
openssl ec -in ./keyFiles/ec-secp256k1-private.pem -pubout -out ./keyFiles/ec-secp256k1-public.pem

# hexadecimal encoded private key string.
openssl ec -in ./keyFiles/ec-secp256k1-private.pem -text -noout
```

2. Create a signing key configuration file in YAML format.

```yaml
type: "file-raw"
keyType: "SECP256K1"
privateKey: "0xaa3d882e938a86957904dcad27a46b044310bd672dba5741d9b61e9f542f6c6b"
```

3. Run Web3Signer.

```shell
web3signer --key-store-path=./keyFiles/ eth1 --chain-id=1337 --downstream-http-port=8545
```

> **Note**: Ensure the Hyperledger Besu network is running before starting Web3Signer.

4. Check Web3Signer.

```shell
curl -X GET http://127.0.0.1:9000/upcheck
```

5. Verify Web3Signer is passing requests to Besu.

```shell
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":51}' http://127.0.0.1:9000
```

### Utility

To generate `n` private keys and save them in signing key configuration files, the `utils.sh` script can be used. To run Web3Signer using the generated private keys, execute the following command:

```shell
web3signer --key-store-path=./keyFiles/keys/ eth1 --chain-id=1337 --downstream-http-port=8545
```

## Running Prometheus and Grafana

- Installation Link for [Prometheus](https://prometheus.io/docs/prometheus/latest/installation/)
- Installation Link for [Grafana](https://grafana.com/docs/grafana/latest/installation/)
- Installation Link for [Node Exporter](https://prometheus.io/docs/guides/node-exporter/)

Before running Prometheus, ensure Node Exporter is running first. Navigate to the `node_exporter` folder and execute the following command:

```shell
sudo docker compose up -d
```

The above command will run Node Exporter on port 9100.
![Node Exporter](/screenshot/node-exporter.png)

Once Prometheus is installed, ensure it is running using the `prometheus.yml` configuration file located in the `prometheus` folder.

```shell
prometheus --config.file=prometheus/prometheus.yml 
```

You can access Prometheus on port 9090.
![Prometheus](/screenshot/prometheus.png)

For Grafana, follow the installation guide linked above. After installation, you can access Grafana on port 3000. Before that, configure Prometheus as a data source in Grafana (this can also be done after accessing Grafana).

```shell
sudo cp ./grafana/provisioning/datasources/datasource.yml /etc/grafana/provisioning/datasources/
```

Restart Grafana.

```shell
sudo systemctl restart grafana-server
```

Access Grafana on port 3000.
![Grafana](/screenshot/grafana.png)

Default Grafana credentials:

```txt
username: admin
password: admin
```

On the Grafana homepage, add a data source by selecting Prometheus (if not already configured). Set the URL to `http://localhost:9090` and click `Save & Test`.

To access pre-configured dashboards, visit [Grafana Dashboard](https://grafana.com/grafana/dashboards) and search for dashboards that suit your needs. Recommended dashboards for this context:

- [Node Exporter Full](https://grafana.com/grafana/dashboards/1860)
- [Besu Overview](https://grafana.com/grafana/dashboards/10273-besu-overview/)
- [Besu Full](https://grafana.com/grafana/dashboards/16455-besu-full/)

Import dashboards at `<ip_address>:3000/dashboard/import` using the dashboard ID or by uploading the downloaded JSON file.

### PromQL Metric Query Configuration for Prometheus

1. **CPU Usage**: Percentage of total user and system CPU time per second over the last 5 minutes.

  ```promql
  sum(rate(process_cpu_seconds_total{job="besu"}[5m])) by (instance) * 100
  ```

2. **Memory Usage**: Percentage of memory used relative to allocated virtual memory.

  ```promql
  process_resident_memory_bytes{job="besu"} / process_virtual_memory_bytes{job="besu"} * 100
  ```

3. **Transaction Count**: Number of transactions performed in the last 5 minutes.

  ```promql
  sum(rate(besu_blockchain_chain_head_transaction_count{job="besu"}[5m]))
  ```

4. **Gas Used**: Gas used in a transaction.

  ```promql
  besu_blockchain_chain_head_gas_used
  ```

### Setting Up Chainlens Blockchain Explorer

Chainlens provides comprehensive information about the private blockchain network created, such as block information, contract metadata, and transaction search. To facilitate information retrieval in this project, Chainlens will be used as the Blockchain Explorer.

> Note: Install Docker and Docker Compose first.

In the `docker-compose` folder within `chainlens`, run the following command:

```shell
NODE_ENDPOINT=http://host.docker.internal:8545 docker compose up -d
```

Once completed, open a browser and access `http://localhost/dashboard` to view the Chainlens Blockchain Explorer.

Stop Chainlens with the following command:

```shell
docker compose down
```

## Running Interaction Code

To run the interaction code, the following are required:

1. Python3
2. pip
3. pipenv

> **Note**: After downloading pipenv, run the command `pipenv shell` to activate the virtual environment. Then, run the command `pipenv install` to download all dependencies required to run the interaction code.

The interaction code is located in the folder `src/networks/ethash/interaction`.

### FlexCoin

To run the FlexCoin interaction code, execute the following command:

```shell
python3 <path_to_FlexCoin.py>
```

You will then be prompted to enter the contract address of the FlexCoin smart contract via the terminal prompt. The contract address of the FlexCoin smart contract can be found in the `FlexCoin.json` file in the `build/contracts` folder. Below is an example of the contract address for the FlexCoin smart contract:

```json
"networks": {
  "1337": {
    "events": {},
    "links": {},
    "address": "0x42699A7612A82f1d9C36148af9C77354759b210b",
    "transactionHash": "0xb79a975a92afb3888096d74fc42ea1e1a75cb5b3dbfa0c295466fb3de65f94fe"
  },
  ...
}
```

Copy the `"address"` from the JSON and input it into the terminal prompt when running the interaction code with FlexCoin.

```txt
What is the contract address? - FlexCoin: 0x42699A7612A82f1d9C36148af9C77354759b210b
```

An example output is as follows:

```txt
Number of houses: 0
Number of accounts: 10
Accounts: ['0x23b7A96F30309eabd68d741C0FeA7802F7Bdd1b5', '0x279842E43ce3036f1E5A9953cF6839e46c78dD05', '0x3517Fb977581Bba4994250A6d01270299922CeE6', '0x45947460FcBd49B5dDec563ea665f3B248B4b5bB', '0x665A8Bc0ae227A5A707011C8FC6F108aE3b04f15', '0x84bE6E63C852A2F898386b1B8f5544Af4a37b8f4', '0x8C07ccE42a6bDDA7d38Bf3338C0D8552005F213e', '0x8F6b731F3EA13eAf15F0d30CA647D66Ad79210F2', '0x95EA5EFf2c878446Fd6C6412750ceD9f6f01F86D', '0xF8445E68553d5dd728A68726ae0397A93C5A9bb2']
House made for node:  0
Transaction Hash: 0x488230b946831cb6612a4c729f131b7712d44e7cca6696c5a6e8087b534ea70b
House made for node:  1
Transaction Hash: 0x77db909ccdcd7cb2a6b47dfa8fe0cdd679d072619215b44830242df536a66fc8
House made for node:  2
Transaction Hash: 0xb97a8c13d3a64e55e501707aebd06cb00a416c27f821cae090c5581eb0f01ef5
House made for node:  3
Transaction Hash: 0x75d55d9c667727f6f70a0bfdd9b14dac8f0ae7517c05acef9f03817b52f8d8d3
House made for node:  4
Transaction Hash: 0xd1ca6ecd94538123606c3a1dc17d8e41d144e3130d1603ae038df9a97c97cc6f
House made for node:  5
Transaction Hash: 0xe447263c383cc6c6baa62c98a7ef6db2bd1506a99e4ef18a280dbcdcd88ecc81
House made for node:  6
Transaction Hash: 0xec80bb0720c6256fbf2c5adb16acaf948074ed13708bb0f933d16b8305b5f0c9
House made for node:  7
Transaction Hash: 0x51477977fbfb81294e290be37902bea86095b3e6c52aa49718816d116e62b587
House made for node:  8
Transaction Hash: 0x1a38ea1ce9a6684fe49397d0d241f7605c1216185ca3409464fd965be16d5422
House made for node:  9
Transaction Hash: 0x5ab2b7866aa12477a4f321b8ba67ae6aef4c5fc42758d36a6204fdca2174014e
```

If you run the `FlexCoinExample.py` code, it will execute a test transaction for FlexCoin with the following output:

```txt
Number of houses: 10
Number of accounts: 10
Accounts: ['0x23b7A96F30309eabd68d741C0FeA7802F7Bdd1b5', '0x279842E43ce3036f1E5A9953cF6839e46c78dD05', '0x3517Fb977581Bba4994250A6d01270299922CeE6', '0x45947460FcBd49B5dDec563ea665f3B248B4b5bB', '0x665A8Bc0ae227A5A707011C8FC6F108aE3b04f15', '0x84bE6E63C852A2F898386b1B8f5544Af4a37b8f4', '0x8C07ccE42a6bDDA7d38Bf3338C0D8552005F213e', '0x8F6b731F3EA13eAf15F0d30CA647D66Ad79210F2', '0x95EA5EFf2c878446Fd6C6412750ceD9f6f01F86D', '0xF8445E68553d5dd728A68726ae0397A93C5A9bb2']
Total houses: 10
House 0 - ETH: 0, FlexCoin: ['0x23b7A96F30309eabd68d741C0FeA7802F7Bdd1b5', 200000000000]

House 1 - ETH: 0, FlexCoin: ['0x279842E43ce3036f1E5A9953cF6839e46c78dD05', 200000000000]

House 2 - ETH: 0, FlexCoin: ['0x3517Fb977581Bba4994250A6d01270299922CeE6', 200000000000]

House 3 - ETH: 0, FlexCoin: ['0x45947460FcBd49B5dDec563ea665f3B248B4b5bB', 200000000000]

House 4 - ETH: 0, FlexCoin: ['0x665A8Bc0ae227A5A707011C8FC6F108aE3b04f15', 200000000000]

House 5 - ETH: 0, FlexCoin: ['0x84bE6E63C852A2F898386b1B8f5544Af4a37b8f4', 200000000000]

House 6 - ETH: 0, FlexCoin: ['0x8C07ccE42a6bDDA7d38Bf3338C0D8552005F213e', 200000000000]

House 7 - ETH: 0, FlexCoin: ['0x8F6b731F3EA13eAf15F0d30CA647D66Ad79210F2', 200000000000]

House 8 - ETH: 0, FlexCoin: ['0x95EA5EFf2c878446Fd6C6412750ceD9f6f01F86D', 200000000000]

House 9 - ETH: 0, FlexCoin: ['0xF8445E68553d5dd728A68726ae0397A93C5A9bb2', 200000000000]

Transferring FlexCoin from 0x23b7A96F30309eabd68d741C0FeA7802F7Bdd1b5 to 0x279842E43ce3036f1E5A9953cF6839e46c78dD05
House 1 - FlexCoin: ['0x23b7A96F30309eabd68d741C0FeA7802F7Bdd1b5', 199999999999]
House 2 - FlexCoin: ['0x279842E43ce3036f1E5A9953cF6839e46c78dD05', 200000000001]
```

### Trading Mechanisms

To run interactions for each trading mechanism, simply execute the corresponding code in the folder `src/networks/ethash/interaction`:

```shell
python3 src/networks/ethash/interaction/Duration.py
python3 src/networks/ethash/interaction/DurationSecure.py
python3 src/networks/ethash/interaction/RealTime.py
python3 src/networks/ethash/interaction/FutureBlock.py
```

### LEM Simulation

LEM simulation can be performed by running the Python script in the following folder: [`/src/networks/ethash/interaction`](/src/networks/ethash/interaction).
