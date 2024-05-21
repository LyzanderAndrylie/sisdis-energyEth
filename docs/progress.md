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
  - [Menyiapkan Web3Signer](#menyiapkan-web3signer)
    - [Membuat signing key configuration file](#membuat-signing-key-configuration-file)
    - [Utility](#utility)
    - [Menyiapkan Chainlens Blockchain explorer](#menyiapkan-chainlens-blockchain-explorer)
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

> **Note**: Ctrl+C untuk menghentikan node

![Node Test](/screenshot/node_test.png)

## Membuat jaringan privat dengan ethash (PoW)

Setiap perintah dijalankan pada node yang berbeda dengan working directory berupa `/ethash`.

1. Jalankan bootnode

  ```shell
  besu --config-file=./src/networks/ethash/config/node/bootnode.toml
  ```

  > **Note**: Jalankan node ini pada terminal baru

2. Jalankan 2 Node lainnya

  ```shell
  besu --config-file=./src/networks/ethash/config/node/node.toml --data-path=./src/networks/ethash/nodes/node-2/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30304
  besu --config-file=./src/networks/ethash/config/node/node.toml --data-path=./src/networks/ethash/nodes/node-3/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30305
  ```

  > **Note**: Buat 2 terminal baru untuk menjalankan node ini

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

> **Note**: Anda tidak perlu untuk mengikuti step 1 dan step 2 dibawah karena sudah disediakan private key pada repositori ini, tahapan 1 dan 2 digunakan jika anda ingin membuat private key yang baru

1. Membuat private key dengan format secp256k1.

```shell
# generate a private key
openssl ecparam -name secp256k1 -genkey -noout -out ec-secp256k1-private.pem

# extract the public key
openssl ec -in ec-secp256k1-private.pem -pubout -out ec-secp256k1-public.pem

# hexadecimal encoded private key string.
openssl ec -in ec-secp256k1-private.pem -text -noout
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

Pada folder `docker-compose` pada `chainles`, jalankan perintah berikut.

```shell
NODE_ENDPOINT=http://host.docker.internal:8545 docker-compose up
```

Stop chainlens dengan perintah berikut.

```shell
docker-compose down
```

### Simulasi LEM

Simulasi LEM dapat dilakukan dengan menjalankan script python pada folder berikut: [`/src/networks/ethash/interaction`](/src/networks/ethash/interaction).

## Note

1. Don't forget about local blcok data and genesis configuration option when running besu.

  Ref: <https://besu.hyperledger.org/private-networks/get-started/start-node>

2. Configuration

- `/config/node/` configuration file is used for node-level settings.

- `/config/network/` configuration file is used for network-wide settings (genesis file).
