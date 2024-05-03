# Dokumen Progress TK Sistem Terdistribusi 2023/2024: EnergyEth

Dokumen ini berisi progress yang telah dilakukan sepanjang TK. Tujuan dokumen ini dibuat untuk menampilkan hal-hal apa saja yang telah dilakukan sampai proyek TK ini selesai bagi tim.

## Daftar Konten

- [Dokumen Progress TK Sistem Terdistribusi 2023/2024: EnergyEth](#dokumen-progress-tk-sistem-terdistribusi-20232024-energyeth)
  - [Daftar Konten](#daftar-konten)
  - [Mempersiapkan Kebutuhan Sistem](#mempersiapkan-kebutuhan-sistem)
  - [Mengunduh Hyperledger Besu](#mengunduh-hyperledger-besu)
  - [Menjalankan sebuah node untuk testing](#menjalankan-sebuah-node-untuk-testing)
  - [Membuat jaringan privat dengan ethash (PoW)](#membuat-jaringan-privat-dengan-ethash-pow)
  - [Mendeploy smart contract ke ethash](#mendeploy-smart-contract-ke-ethash)
  - [Note](#note)

## Mempersiapkan Kebutuhan Sistem

Untuk menjalankan [Hyperledger Besu](https://besu.hyperledger.org/) dengan jaringan privat, kita memerlukan sistem operasi Linux dengan ketentuan yang dapat diakses pada link <https://besu.hyperledger.org/private-networks/get-started/system-requirements>.

Untuk menjalankan Ubuntu Desktop pada VM dengan VirtualBox, kita dapat mengakses panduan pada link <https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview>.  

> Note: Jika kalian ingin mempersiapkan Ubuntu pada VirtualBox, pastikan versi yang kompatibel. Saat ini, VirtualBox 7.0.12 berjalan dengan baik dengan Ubuntu 22.04

## Mengunduh Hyperledger Besu

Versi: 24.3.3

Link:

1. <https://github.com/hyperledger/besu/releases/tag/24.3.3>
2. <https://yehiatarek67.medium.com/install-hyperledger-besu-on-linux-for-beginners-a5a67d1f54c7>

```shell
besu --help
```

## Menjalankan sebuah node untuk testing

```shell
besu --config-file=./src/networks/test/config/node/test.toml
```

![Node Test](/screenshot/node_test.png)

## Membuat jaringan privat dengan ethash (PoW)

Setiap perintah dijalankan pada node yang berbeda dengan working directory berupa `/ethash`.

1. Jalankan bootnode

  ```shell
  besu --config-file=./src/networks/ethash/config/node/bootnode.toml
  ```

2. Jalankan 2 Node lainnya

  ```shell
  besu --config-file=./src/networks/ethash/config/node/node.toml --data-path=./src/networks/ethash/nodes/node-2/data--bootnodes=<Node-1 Enode URL> --p2p-port=30304
  besu --config-file=./src/networks/ethash/config/node/node.toml --data-path=./src/networks/ethash/nodes/node-3/data --bootnodes=<Node-1 Enode URL> --p2p-port=30305
  ```

  > *Note*: Node-1 Enode URL dapat dilihat ketika menjalankan perintah `Jalankan bootnode`.

## Mendeploy smart contract ke ethash

untuk mendeploy, kita memerlukan hal berikut.

1. Node package manager (npm)
2. <https://www.npmjs.com/package/web3>

> **Note**: Setelah kalian mengunduh npm, jalankan perintah `npm i` untuk mengunduh packages yang dibutuhkan.

`CompilerByRemote.js` memiliki bug terkait dengan `Invalid member of stdlib` (ref: <https://github.com/ethereum/solc-js/issues/537>). Dengan demikian, pakai `compileByBinary.js` sesuai dengan arahan pada github issues yang telah disebutkan.

## Note

1. Don't forget about local blcok data and genesis configuration option when running besu.

  Ref: <https://besu.hyperledger.org/private-networks/get-started/start-node>

2. Configuration

- `/config/node/` configuration file is used for node-level settings.

- `/config/network/` configuration file is used for network-wide settings (genesis file).
