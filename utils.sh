#!/bin/bash

delete_local_block_data() {
    rm -r ./src/networks/ethash/nodes/node-?/data/*
}

main() {
    echo 'List of available commands:'
    echo '1. delete_local_block_data'
    echo

    read -r -p "command: " answer

    if [[ "${answer}" == "1" ]]; then
        echo 'Deleting local block data...'
        delete_local_block_data
    fi
}

main