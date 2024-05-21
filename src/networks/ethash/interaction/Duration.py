from web3 import Web3, HTTPProvider
import json
import numpy as np
import random
import copy
import matplotlib.pyplot as plt
import time

# Define the URL for the Web3 provider
host = 'http://localhost:9000'  # Web3Signer URL

web3 = Web3(HTTPProvider(host))

# Load and parse the ABI for Duration
jsonFile = open('./build/contracts/Duration.json', 'r')
values = json.load(jsonFile)
jsonFile.close()

abi = values['abi']
address = input("What is the contract address? - Duration: ")
Duration = web3.eth.contract(address=address, abi=abi)

# Load and parse the ABI for FlexCoin
jsonFileFlexCoin = open('./build/contracts/FlexCoin.json', 'r')
valuesFlexCoin = json.load(jsonFileFlexCoin)
jsonFileFlexCoin.close()

abiFlexCoin = valuesFlexCoin['abi']
addressFlexCoin = input("What is the contract address? - FlexCoin: ")
FlexCoin = web3.eth.contract(address=addressFlexCoin, abi=abiFlexCoin)

def wait_for_receipt(tx_hash, timeout=120):
    start_time = time.time()
    while True:
        try:
            receipt = web3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                return receipt
        except:
            pass
        time.sleep(0.5)
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

        if FlexCoin.functions.numHouses().call() <= i:
            tx_hash = FlexCoin.functions.newHouse().transact({'from': account})
            receipt = wait_for_receipt(tx_hash)
            print(f"Gas used for creating house for account {i}: {receipt.gasUsed}")

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
    binary = ['' for _ in range(_numSupply)]
    total = 0
    supplyCost = 0
    demandCost = 0

    for s in range(_numSupply):
        for t in range(_steps):
            tempBin = random.randint(0, 1)
            binary[s] = str(tempBin) + binary[s]
            total += tempBin

        account = web3.eth.accounts[s]

        tx_hash = Duration.functions.setNode(0, '', binary[s]).transact({'from': account})
        receipt = wait_for_receipt(tx_hash)
        supplyCost += receipt.gasUsed
        print(f"Gas used for setting node {s} (supply): {receipt.gasUsed}")

    demandString = ['' for _ in range(_numDemand)]
    demandHours = [0 for _ in range(_numDemand)]
    i = 0

    while total > sum(demandHours):
        demandHours[i] += 1
        i = (i + 1) % _numDemand

    for d in range(_numDemand):
        for t in range(_steps):
            demandString[d] = str(random.randint(150, 600)) + ',' + demandString[d]

        account = web3.eth.accounts[(d + 1) % len(web3.eth.accounts)]

        tx_hash = Duration.functions.setNode(demandHours[d], demandString[d], '').transact({'from': account})
        receipt = wait_for_receipt(tx_hash)
        demandCost += receipt.gasUsed
        print(f"Gas used for setting node {d} (demand): {receipt.gasUsed}")

    return demandCost, supplyCost

def getSystemData(_numNodes, _steps, iterator):
    """
    Fetches the energy data from the blockchain.
    """
    owner = ["0" for _ in range(_numNodes)]
    demandHours = [0 for _ in range(_numNodes)]
    tempDemandPrices = [['' for _ in range(_steps)] for _ in range(_numNodes)]
    endDemandPrices = [[999 for _ in range(_steps)] for _ in range(_numNodes)]
    endSupplyHours = [[0 for _ in range(_steps)] for _ in range(_numNodes)]

    lastNodeID = Duration.functions.numNodes().call() - 1
    firstNodeID = lastNodeID - _numNodes + 1

    for n in range(_numNodes):
        nodeData = Duration.functions.getNode(firstNodeID + n).call()
        owner[n], demandHours[n], demandPrices, supplyHours = nodeData

        if supplyHours == '':
            i = 0
            for t in range(_steps):
                while demandPrices[i] != ',':
                    tempDemandPrices[n][t] += demandPrices[i]
                    i += 1
                i += 1
                endDemandPrices[n][t] = int(tempDemandPrices[n][t])
        else:
            for t in range(_steps):
                endSupplyHours[n][t] = int(supplyHours[t])

    endDemandPrices = np.array(endDemandPrices).transpose()
    endSupplyHours = np.array(endSupplyHours).transpose()
    return owner, demandHours, endSupplyHours, endDemandPrices


def matching(owner, demandHours, supplyHours, demandPrices, steps):
    """
    Market calculation and payment processing.
    """
    sortedList = [[] for _ in range(steps)]
    addressFrom = [[] for _ in range(steps)]
    addressTo = [[] for _ in range(steps)]
    copyDemandPrices = copy.deepcopy(demandPrices.tolist())
    cost = 0

    for t in range(steps):
        for i in range(int(np.sum(supplyHours[t]))):
            sortedList[t].append(demandPrices[t].tolist().index(min(demandPrices[t])))
            demandPrices[t][sortedList[t][i]] = 999
            addressFrom[t].append(sortedList[t][i])
            addressTo[t].append(supplyHours[t].tolist().index(1))
            supplyHours[t][supplyHours[t].tolist().index(1)] = 0
            demandHours[sortedList[t][i]] -= 1
            if demandHours[sortedList[t][i]] == 0:
                for t2 in range(i, steps):
                    demandPrices[t2][sortedList[t][i]] = 999

        if len(sortedList[t]) > 0:
            for a in range(len(web3.eth.accounts) - 1):
                _, bal = FlexCoin.functions.getHouse(web3.eth.accounts[a]).call()
                if bal == 0:
                    tx_hash = FlexCoin.functions.newHouse().transact({'from': web3.eth.accounts[a]})
                    receipt = wait_for_receipt(tx_hash)
                    print(f"Gas used for creating new house: {receipt.gasUsed}")

            tx_hash = Duration.functions.checkAndTransfer(sortedList[t], addressFrom[t], addressTo[t], copyDemandPrices[t], t, FlexCoin.address).transact()
            receipt = wait_for_receipt(tx_hash)
            cost += receipt.gasUsed
            print(f"Gas used for check and transfer at step {t}: {receipt.gasUsed}")

    return cost

testRange = range(10, 11)  # testing dengan 10 nodes
centralCostResults = []
demandCostResults = []
supplyCostResults = []

# Testing node sensitivity
print("Testing Node Sensitivity")
for numNodes in testRange:
    centralCost, demandCost, supplyCost = nodeSensitivity(0, numNodes, 24)
    centralCostResults.append(centralCost)
    demandCostResults.append(demandCost)
    supplyCostResults.append(supplyCost)
    print(f"Results for {numNodes} nodes:")
    print(f"Central Cost: {centralCost}")
    print(f"Demand Cost: {demandCost}")
    print(f"Supply Cost: {supplyCost}")

# Testing step sensitivity
print("\nTesting Step Sensitivity")
startSteps = 0
stopSteps = 144  # 6 days with 24-hour steps
centralCostStepResults = []
demandCostStepResults = []
supplyCostStepResults = []

for numNodes in testRange:
    centralCost, demandCost, supplyCost = stepSensitivity(numNodes, startSteps, stopSteps)
    centralCostStepResults.append(centralCost)
    demandCostStepResults.append(demandCost)
    supplyCostStepResults.append(supplyCost)
    print(f"Results for {numNodes} nodes over {stopSteps - startSteps} steps:")
    print(f"Central Cost: {centralCost}")
    print(f"Demand Cost: {demandCost}")
    print(f"Supply Cost: {supplyCost}")
