# Dokumen Progress TK Sistem Terdistribusi 2023/2024: EnergyEth

Dokumen ini berisi progress yang telah dilakukan sepanjang TK. Tujuan dokumen ini dibuat untuk menampilkan hal-hal apa saja yang telah dilakukan sampai proyek TK ini selesai bagi tim.

## Daftar Konten

- [Dokumen Progress TK Sistem Terdistribusi 2023/2024: EnergyEth](#dokumen-progress-tk-sistem-terdistribusi-20232024-energyeth)
  - [Daftar Konten](#daftar-konten)
  - [Mempersiapkan Kebutuhan Sistem](#mempersiapkan-kebutuhan-sistem)
    - [VirtualBox](#virtualbox)
    - [Lainnya](#lainnya)
  - [Mengunduh Hyperledger Besu](#mengunduh-hyperledger-besu)
  - [Menjalankan sebuah node untuk testing](#menjalankan-sebuah-node-untuk-testing)
  - [Membuat jaringan privat dengan ethash (PoW)](#membuat-jaringan-privat-dengan-ethash-pow)
  - [Mendeploy smart contract ke ethash](#mendeploy-smart-contract-ke-ethash)
  - [Menyiapkan Web3Signer](#menyiapkan-web3signer)
    - [Membuat signing key configuration file](#membuat-signing-key-configuration-file)
    - [Utility](#utility)
    - [Menyiapkan Chainlens Blockchain explorer](#menyiapkan-chainlens-blockchain-explorer)
  - [Menjalankan Prometheus dan Grafana](#menjalankan-prometheus-dan-grafana)
  - [Menjalankan Kode Interaksi](#menjalankan-kode-interaksi)
    - [FlexCoin](#flexcoin)
  - [Note](#note)

## Mempersiapkan Kebutuhan Sistem

### VirtualBox

Untuk menjalankan [Hyperledger Besu](https://besu.hyperledger.org/) dengan jaringan privat, kita memerlukan sistem operasi Linux dengan ketentuan yang dapat diakses pada link <https://besu.hyperledger.org/private-networks/get-started/system-requirements>.

Untuk menjalankan Ubuntu Desktop pada VM dengan VirtualBox, kita dapat mengakses panduan pada link <https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview>.  

> Note: Jika kalian ingin mempersiapkan Ubuntu pada VirtualBox, pastikan versi yang kompatibel. Saat ini, VirtualBox 7.0.12 berjalan dengan baik dengan Ubuntu 22.04

### Lainnya

Kita juga bisa menggunakan WSL2, Docker, ataupun *dual-booting* untuk menjalankan Hyperledger Besu. Pilih opsi yang memudahkan kalian untuk menjalankan kode yang ada.

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
  besu --config-file=./src/networks/ethash/config/node/node.toml --data-path=./src/networks/ethash/nodes/node-2/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30304
  besu --config-file=./src/networks/ethash/config/node/node.toml --data-path=./src/networks/ethash/nodes/node-3/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30305
  ```

  > *Note*: Node-1 Enode URL dapat dilihat ketika menjalankan perintah `Jalankan bootnode`.

## Mendeploy smart contract ke ethash

untuk mendeploy, kita memerlukan hal berikut.

1. Node package manager (npm)
2. <https://www.npmjs.com/package/web3>
3. Truffle diinstal secara global

> **Note**: Setelah kalian mengunduh npm, jalankan perintah `npm i` untuk mengunduh packages yang dibutuhkan.

Jalankan perintah berikut untuk men-compile dan men-deploy smart contract:

```shell
truffle migrate --network besu
```

## Menyiapkan Web3Signer

Download Web3Signer dari link: <https://docs.web3signer.consensys.io/get-started/install-binaries>

### Membuat signing key configuration file

Signing key configuration file akan digunakan oleh Web3Signer dalam proses *signing*. Pada proyek ini, private key akan disimpan di folder `keyFiles` dan raw unencrypted files akan digunakan sebagai signing key configuration file untuk mempermudah proses pengerjaan. Hal ini berarti private key yang dihasilkan tidak aman dan hanya digunakan untuk kebutuhan proyek ini saja!

1. Membuat private key dengan format secp256k1.

```shell
# generate a private key
openssl ecparam -name secp256k1 -genkey -noout -out ./keyFiles/ec-secp256k1-private.pem

# extract the public key
openssl ec -in ./keyFiles/ec-secp256k1-private.pem -pubout -out ./keyFiles/ec-secp256k1-public.pem

# hexadecimal encoded private key string.
openssl ec -in ./keyFiles/ec-secp256k1-private.pem -text -noout
```

2. Membuat signing key configuration file dalam format yaml

```shell
type: "file-raw"
keyType: "SECP256K1"
privateKey: "0xaa3d882e938a86957904dcad27a46b044310bd672dba5741d9b61e9f542f6c6b"
```

3. Jalankan Web3Signer

```shell
web3signer --key-store-path=./keyFiles/ eth1 --chain-id=1337 --downstream-http-port=8545
```

> Note: sebelum menjalankan Web3Signer, jaringan hyperledger besu harus dijalankan terlebih dahulu.

4. Cek Web3Signer

```shell
curl -X GET http://127.0.0.1:9000/upcheck
```

5. Cek Web3Signer passing requests to Besu

```shell
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":51}' http://127.0.0.1:9000
```

### Utility

Untuk membuat private key sebanyak n dan menyimpannya pada signing key configuration file, kode `utils.sh` dapat digunakan. Untuk menjalankan Web3Signer dengan memanfaatkan private key yang dibuat, jalankan perintah berikut.

```shell
web3signer --key-store-path=./keyFiles/keys/ eth1 --chain-id=1337 --downstream-http-port=8545
```

### Menyiapkan Chainlens Blockchain explorer

Chainlens menyediakan informasi menyeluruh dari jaringan privat blockchain yang dibuat, seperti informasi block, contract metadata, dan pencarian transaksi. Untuk mempermudah *information retrieval* pada proyek ini, Chainlens akan digunakan sebagai Blockchain explorer.

> Note: Instal Docker dan Docker Compose terlebih dahulu

Pada folder `docker-compose` pada `chainlens`, jalankan perintah berikut.

```shell
NODE_ENDPOINT=http://host.docker.internal:8545 docker compose up -d
```

Setelah selesai, buka browser dan akses `http://localhost/dashboard` untuk melihat Chainlens Blockchain explorer.

Stop chainlens dengan perintah berikut.

```shell
docker compose down
```

## Menjalankan Prometheus dan Grafana

Untuk menjalankan Prometheus dan Grafana, ubah working directory ke folder `prometheus-grafana`. Kemudian, jalankan perintah berikut.

```shell
```

Kemudian, untuk mengakses Grafana, kita dapat mengakses <http://localhost:3000/login> dan mengisi kredensial sebagai berikut.

```txt
username: admin
password: admin
```

## Menjalankan Kode Interaksi

Untuk menjalankan kode interkasi, kita memerlukan:

1. Python3
2. pip
3. pipenv

> **Note**: Setelah kalian mengunduh pipenv, jalankan perintah `pipenv shell` untuk menjalankan virtual environment. Kemudian, jalankan perintah `pipenv install` untuk mengunduh semua dependensi yang diperlukan untuk menjalankan kode interkasi.

Kode interaksi terdapat pada folder `src/networks/ethash/interaction`.

### FlexCoin

Untuk menjalankan kode interkasi FlexCoin, jalankan perintah berikut.

```shell
python3 <path_ke_FlexCoin.py>
```

Kemudian, kita akan diminta untuk mengisi contract address dari *smart contract* FlexCoin melalui prompt terminal. Contract address dari *smart contract* FlexCoin dapat diakses pada file `FlexCoin.json` pada folder `build/contracts`. Berikut adalah contoh dari contract address *smart contract* FlexCoin.

```json
networks": {
    "1337": {
      "events": {},
      "links": {},
      "address": "0x42699A7612A82f1d9C36148af9C77354759b210b",
      "transactionHash": "0xb79a975a92afb3888096d74fc42ea1e1a75cb5b3dbfa0c295466fb3de65f94fe"
    },
    ...
}
```

Ambil `"address"` pada JSON tersebut dan masukkan ke prompt terminal ketika menjalankan kode interaksi dengan FlexCoin.

```txt
What is the contract address? - FlexCoin: 0x42699A7612A82f1d9C36148af9C77354759b210b
```

Contoh output adalah sebagai berikut.

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

Jika kita menjalankan kode FlexCoin.py untuk kedua kalinya, akan dijalankan uji coba transaksi FlexCoin dengan output sebagai berikut.

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

## Note

1. Don't forget about local blcok data and genesis configuration option when running besu.

  Ref: <https://besu.hyperledger.org/private-networks/get-started/start-node>

2. Configuration

- `/config/node/` configuration file is used for node-level settings.

- `/config/network/` configuration file is used for network-wide settings (genesis file).
