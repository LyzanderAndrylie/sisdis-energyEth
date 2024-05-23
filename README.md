# TK Sistem Terdistribusi 2023/2024: EnergyEth

Repository TK Sistem Terdistribusi dengan topik Economic Feasibility of Consensus dari kode tesis [energyEth](https://github.com/fredrbl/energyEth)

- [TK Sistem Terdistribusi 2023/2024: EnergyEth](#tk-sistem-terdistribusi-20232024-energyeth)
  - [Struktur Folder](#struktur-folder)
  - [Dokumentasi](#dokumentasi)

## Struktur Folder

- `/build` berisi *smart contract* yang telah di-*compile* dengan menggunakan Truffle
- `/chainlens` berisi `compose.yaml` untuk menjalankan Chainlens Blockchain Explorer
- `/contracts` berisi *smart contract* energyEth.
- `/docs` berisi dokumentasi pengerjaan proyek ini.
- `/grafana` berisi konfigurasi grafana yang diperlukan.
- `/keyFiles` berisi konfigurasi accounts (public key dan private key) yang dikelola oleh Web3Signer.
- `/migrations` berisi kode untuk melakukan deployment *smart contract* oleh Truffle ke Hyperledger Besu.
- `/node-exporter` berisi `compose.yml` untuk menjalankan `node-exporter` untuk Prometheus.
- `/prometheus` berisi konfigurasi prometheus yang diperlukan.
- `/screenshot` berisi tangkapan layar dari pengerjaan proyek ini.
- `/src` berisi konfigurasi jaringan ethash dengan Hyperledger Besu.
  - `/src/networks/ethash/config/node` file konfigurasi untuk tingkat node.
  - `/src/networks/ethash/config/network` file konfigurasi untuk tingkat jaringan (file genesis).
  - `/src/networks/ethash/interaction` berisi kode python untuk berinterkasi dengan *smart contract* yang telah di-*deploy*.
  - `/src/networks/ethash/nodes` berisi local block data untuk setiap *nodes* yang berpartisipasi dalam jaringan blockchain ethash.
- `package.json` berisi dependensi JavaScript (Node).
- `Pipfile` berisi dependensi Python.
- `truffle-config.js` berisi konfigrausi Truffle.
- `utils.sh` berisi script bash untuk mempermudah menjalankan jaringan blockchain.

## Dokumentasi

Dokumentasi terkait tutorial untuk mengrekreasi hasil kerja kami dapat dilihat pada : [`./docs/progress.md`](./docs/progress.md).
