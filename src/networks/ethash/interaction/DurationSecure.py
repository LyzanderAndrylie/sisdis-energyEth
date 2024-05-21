from web3 import Web3, HTTPProvider
import json
import numpy as np
import random
import copy
import matplotlib.pyplot as plt

# Define the URL for the Web3 provider
host = 'http://localhost:9000'  # Web3Signer URL

web3 = Web3(HTTPProvider(host))

# Load and parse the ABI for DurationSecure
jsonFile = open('./build/contracts/DurationSecure.json', 'r')
values = json.load(jsonFile)
jsonFile.close()

abi = values['abi']
address = input("What is the contract address? - DurationSecure: ")
DurationSecure = web3.eth.contract(address=address, abi=abi)

# Load and parse the ABI for FlexCoin
jsonFileFlexCoin = open('./build/contracts/FlexCoin.json', 'r')
valuesFlexCoin = json.load(jsonFileFlexCoin)
jsonFileFlexCoin.close()

abiFlexCoin = valuesFlexCoin['abi']
addressFlexCoin = input("What is the contract address? - FlexCoin: ")
FlexCoin = web3.eth.contract(address=addressFlexCoin, abi=abiFlexCoin)

totTransactions = 0

def wait_for_receipt(tx_hash, timeout=120):
    start_time = time.time()
    while True:
        try:
            receipt = web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                return receipt
        except:
            pass
        time.sleep(1)
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Transaction {tx_hash} not confirmed in {timeout} seconds")

def nodeSensitivity(start, stop, steps):
    """
    Performs sensitivity analysis on the number of nodes in the day-ahead trading.
    """
    nodes = range(start, stop, 1)
    demandCost = [0 for _ in range(stop)]
    supplyCost = [0 for _ in range(stop)]
    centralCost = [0 for _ in range(stop)]
    iterator = 0

    for i in range(stop):
        account = web3.eth.accounts[i % len(web3.eth.accounts)]
        if web3.eth.get_balance(account) < 123456789101112131415:
            web3.eth.send_transaction({'to': account, 'from': web3.eth.coinbase, 'value': 123456789101112131415})

        if FlexCoin.functions.numHouses().call() <= i:
            tx_hash = FlexCoin.functions.newHouse().transact({'from': account})
            receipt = wait_for_receipt(tx_hash)
            print(f"Gas used for creating house for account {i}: {receipt.gasUsed}")

        add, tot = FlexCoin.functions.getHouse(account).call()

    for n in nodes:
        if n % 2 == 0:
            demandCost[n], supplyCost[n] = setSystemData(n // 2, n // 2, steps)
            owner, demandHours, supplyHours, demandPrices = getSystemData(n, steps, iterator)
            centralCost[n] = matching(owner, demandHours, supplyHours, demandPrices, steps)
        else:
            demandCost[n], supplyCost[n] = setSystemData((n + 1) // 2, (n - 1) // 2, steps)
            owner, demandHours, supplyHours, demandPrices = getSystemData(n, steps, iterator)
            centralCost[n] = matching(owner, demandHours, supplyHours, demandPrices, steps)
        iterator += 1

    return centralCost, demandCost, supplyCost

def stepSensitivity(numNodes, start, stop):
    """
    Performs sensitivity analysis on the amount of time steps in the day-ahead trading.
    """
    steps = range(start, stop, 24)
    demandCost = [0 for _ in range(stop)]
    supplyCost = [0 for _ in range(stop)]
    centralCost = [0 for _ in range(stop)]

    _numDemand = (numNodes + 1) // 2 if numNodes % 2 != 0 else numNodes // 2
    _numSupply = numNodes - _numDemand

    iterator = 0
    for t in steps:
        demandCost[t], supplyCost[t] = setSystemData(_numSupply, _numDemand, t)
        owner, demandHours, supplyHours, demandPrices = getSystemData(numNodes, t, iterator)
        centralCost[t] = matching(owner, demandHours, supplyHours, demandPrices, t)
        iterator += 1

    return centralCost, demandCost, supplyCost

def setSystemData(_numSupply, _numDemand, _steps):
    """
    Sets energy data for the supply and demand side into the blockchain.
    """
    global totTransactions
    binary = [[0 for _ in range(_steps)] for _ in range(_numSupply)]
    total = 0
    supplyCost = 0
    demandCost = 0

    for s in range(_numSupply):
        for t in range(_steps):
            binary[s][t] = random.randint(0, 1)
            total += binary[s][t]

        account = web3.eth.accounts[s]
        if web3.eth.get_balance(account) < 99999999999:
            web3.personal.unlockAccount(account, 'pass')
            web3.eth.send_transaction({'to': account, 'from': web3.eth.coinbase, 'value': 999999999999})

        tx_hash = DurationSecure.functions.setNode(0, [0], binary[s]).transact({'from': account})
        receipt = wait_for_receipt(tx_hash)
        supplyCost += receipt.gasUsed
        totTransactions += 1
        print(f"Gas used for setting node {s} (supply): {receipt.gasUsed}")

    demandPrices = [[0 for _ in range(_steps)] for _ in range(_numDemand)]
    demandHours = [0 for _ in range(_numDemand)]
    i = 0

    while total > sum(demandHours):
        demandHours[i] += 1
        i = (i + 1) % _numDemand

    for d in range(_numDemand):
        for t in range(_steps):
            demandPrices[d][t] = random.randint(150, 600)

        account = web3.eth.accounts[(d + 1) % len(web3.eth.accounts)]
        if web3.eth.get_balance(account) < 99999999999:
            web3.personal.unlockAccount(account, 'pass')
            web3.eth.send_transaction({'to': account, 'from': web3.eth.coinbase, 'value': 999999999999})

        tx_hash = DurationSecure.functions.setNode(demandHours[d], demandPrices[d], [0]).transact({'from': account})
        receipt = wait_for_receipt(tx_hash)
        demandCost += receipt.gasUsed
        totTransactions += 1
        print(f"Gas used for setting node {d} (demand): {receipt.gasUsed}")

    return demandCost, supplyCost

def getSystemData(_numNodes, _steps, iterator):
    """
    Fetches the energy data from the blockchain.
    """
    owner = ["0" for _ in range(_numNodes)]
    demandHours = [0 for _ in range(_numNodes)]
    demandPrices = [[] for _ in range(_numNodes)]
    supplyHours = [[] for _ in range(_numNodes)]
    testDemandPrices = [0 for _ in range(_numNodes)]
    testSupplyHours = [0 for _ in range(_numNodes)]

    lastNodeID = DurationSecure.functions.numNodes().call() - 1
    firstNodeID = lastNodeID - _numNodes + 1

    for n in range(_numNodes):
        nodeData = DurationSecure.functions.getNode(firstNodeID + n, 0, 1).call()
        owner[n], demandHours[n], testDemandPrices[n], testSupplyHours[n] = nodeData

        if demandHours[n] != 0:
            for t in range(_steps):
                supplyHours[n].append(0)
                demandPrices[n].append(DurationSecure.functions.getNode(firstNodeID + n, t, 1).call()[2])
        else:
            for t in range(_steps):
                demandPrices[n].append(999)
                supplyHours[n].append(DurationSecure.functions.getNode(firstNodeID + n, t, 0).call()[3])

    demandPrices = np.array(demandPrices).transpose()
    supplyHours = np.array(supplyHours).transpose()
    return owner, demandHours, supplyHours, demandPrices

def matching(owner, demandHours, supplyHours, demandPrices, steps):
    """
    Market calculation and payment processing.
    """
    global totTransactions
    sortedList = [[] for _ in range(steps)]
    addressFrom = [[] for _ in range(steps)]
    addressTo = [[] for _ in range(steps)]
    copyDemandPrices = copy.deepcopy(demandPrices.tolist())
    cost = 0

    numNodes = len(supplyHours[0])
    lastNodeID = DurationSecure.functions.numNodes().call() - 1
    firstNodeID = lastNodeID - numNodes + 1

    for t in range(steps):
        length = int(np.sum(supplyHours[t]))

        for i in range(length):
            sortedList[t].append(demandPrices[t].tolist().index(min(demandPrices[t])))
            demandPrices[t][sortedList[t][i]] = 998
            addressFrom[t].append(sortedList[t][i])
            addressTo[t].append(supplyHours[t].tolist().index(1))
            supplyHours[t][supplyHours[t].tolist().index(1)] = 0
            demandHours[sortedList[t][i]] -= 1
            if demandHours[sortedList[t][i]] == 0:
                for t2 in range(i, steps):
                    demandPrices[t2][sortedList[t][i]] = 998

        if length > 0:
            for a in range(len(web3.eth.accounts) - 1):
                _, bal = FlexCoin.functions.getHouse(web3.eth.accounts[a]).call()
                if bal == 0:
                    tx_hash = FlexCoin.functions.newHouse().transact({'from': web3.eth.accounts[a]})
                    receipt = wait_for_receipt(tx_hash)
                    print(f"Gas used for creating new house: {receipt.gasUsed}")

            tx_hash = DurationSecure.functions.checkAndTransfer(sortedList[t], addressFrom[t], addressTo[t], t, FlexCoin.address).transact()
            receipt = wait_for_receipt(tx_hash)
            cost += receipt.gasUsed
            totTransactions += 1
            print(f"Gas used for check and transfer at step {t}: {receipt.gasUsed}")

    return cost
