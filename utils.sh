#!/bin/bash

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

main() {
    echo 'List of available commands:'
    echo '1. delete_local_block_data'
    echo '2. generate_signing_key_configuration_file'
    echo

    read -r -p "command: " answer

    if [[ "${answer}" == "1" ]]; then
        echo 'Deleting local block data...'
        delete_local_block_data
    elif [[ "${answer}" == "2" ]]; then
        echo 'Generating signing key configuration file...'
        generate_signing_key_configuration_file
    fi
}

main