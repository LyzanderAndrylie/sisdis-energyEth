#!/bin/bash

# Define full paths to commands
besu="/opt/besu/bin/besu"
web3signer="/opt/web3signer/bin/web3signer"

delete_local_block_data() {
    rm -r ./src/networks/ethash/nodes/node-?/data/*
}

generate_signing_key_configuration_file() {
    read -r -p "Enter total generated private key: " total

    # Delete all files in keys directory
    rm -r ./keyFiles/keys/*

    # Create key.yaml
    for ((i=1; i<=total; i++)); do
        echo "Generating private key ${i}"
        openssl ecparam -name secp256k1 -genkey -noout -out ./keyFiles/keys/ec-secp256k1-private-${i}.pem

        # Convert private key to hexa
        hexa=$( openssl ec -in ./keyFiles/keys/ec-secp256k1-private-${i}.pem -text -noout | grep priv -A 3 | tail -n +2 | tr -d '\n[:space:]:')

        # Store to key.yaml
        echo "type: \"file-raw\"" >> ./keyFiles/keys/key.yaml
        echo "keyType: \"SECP256K1\"" >> ./keyFiles/keys/key.yaml
        echo "privateKey: \"0x${hexa}\"" >> ./keyFiles/keys/key.yaml

        if [[ "${i}" != "${total}" ]]; then
            echo "---" >> ./keyFiles/keys/key.yaml
        fi
    done

}

run_bootnode() {
    $besu --config-file=./src/networks/ethash/config/node/bootnode.toml
}

run_node_2() {
    $besu --config-file=./src/networks/ethash/config/node/node1.toml --data-path=./src/networks/ethash/nodes/node-2/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30304
}

run_node_3() {
    $besu --config-file=./src/networks/ethash/config/node/node2.toml --data-path=./src/networks/ethash/nodes/node-3/data --bootnodes=enode://6c2d168d2797090078406024ec1a9b726872046f6fa14ca7e0fbf448912a56fedd337c3908f2d9e66b98e7dc0f8024fcf41707d844dafbca530cbad4482a4edc@127.0.0.1:30303 --p2p-port=30305
}

truffle_migrate() {
    npx truffle migrate --network besu
}

run_web3signer() {
    $web3signer --key-store-path=./keyFiles/keys/ eth1 --chain-id=1337 --downstream-http-port=8545
}

ethash() {
    echo 'List of available commands:'
    echo '1. delete_local_block_data'
    echo '2. generate_signing_key_configuration_file'
    echo '3. run bootnode'
    echo '4. run node-2'
    echo '5. run node-3'
    echo '6. compile and deploy contract to ethash'
    echo '7. run web3signer'

    read -r -p "command: " answer

    if [[ "${answer}" == "1" ]]; then
        echo 'Deleting local block data...'
        delete_local_block_data
    elif [[ "${answer}" == "2" ]]; then
        echo 'Generating signing key configuration file...'
        generate_signing_key_configuration_file
    elif [[ "${answer}" == "3" ]]; then
        echo 'Running bootnode...'
        run_bootnode
    elif [[ "${answer}" == "4" ]]; then
        echo 'Running node-2...'
        run_node_2
    elif [[ "${answer}" == "5" ]]; then
        echo 'Running node-3...'
        run_node_3
    elif [[ "${answer}" == "6" ]]; then
        echo 'Compiling and deploying contract to ethash...'
        truffle_migrate
    elif [[ "${answer}" == "7" ]]; then
        echo 'Running web3signer...'
        run_web3signer
    fi
}

main() {
    echo 'List of available commands:'
    echo '1. ethash commands'
    echo

    read -r -p "command: " answer

    if [[ "${answer}" == "1" ]]; then
        ethash
    fi
}

main