# TK Distributed Systems 2023/2024: EnergyEth

Repository for the Distributed Systems coursework project on the topic of Economic Feasibility of Consensus based on the thesis code [energyEth](https://github.com/fredrbl/energyEth)

- [TK Distributed Systems 2023/2024: EnergyEth](#tk-distributed-systems-20232024-energyeth)
  - [Folder Structure](#folder-structure)
  - [Documentation](#documentation)

## Folder Structure

- `/build` contains the compiled *smart contracts* using Truffle
- `/chainlens` contains the `compose.yaml` to run Chainlens Blockchain Explorer
- `/contracts` contains the energyEth *smart contracts*
- `/docs` contains the project documentation
- `/grafana` contains the necessary Grafana configurations
- `/keyFiles` contains account configurations (public and private keys) managed by Web3Signer
- `/migrations` contains the code to deploy *smart contracts* to Hyperledger Besu using Truffle
- `/node-exporter` contains `compose.yml` to run `node-exporter` for Prometheus
- `/prometheus` contains the necessary Prometheus configurations
- `/screenshot` contains screenshots of the project work
- `/src` contains the ethash network configuration using Hyperledger Besu
  - `/src/networks/ethash/config/node` contains node-level configuration files
  - `/src/networks/ethash/config/network` contains network-level configuration files (genesis file)
  - `/src/networks/ethash/interaction` contains Python code to interact with the deployed *smart contracts*
  - `/src/networks/ethash/nodes` contains local block data for each *node* participating in the ethash blockchain network
- `package.json` contains JavaScript (Node.js) dependencies
- `Pipfile` contains Python dependencies
- `truffle-config.js` contains the Truffle configuration
- `utils.sh` contains bash scripts to simplify blockchain network operations

## Documentation

Tutorials and documentation for recreating our project work can be found at: [`./docs/progress.md`](./docs/progress.md).
