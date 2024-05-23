def matching(flexFlag, transactions, demand, supply):
    """
    This function matches supply and demand, filling the results into a transactions vector.
    """
    i, j = 0, 0

    while len(demand[0]) > i and len(supply[0]) > j and flexFlag != 2:
        if demand[1][i] == 0:
            i += 1
        elif supply[1][j] == 0:
            j += 1
        elif demand[1][i] <= supply[1][j]:
            transactions[0].append(supply[0][j])
            transactions[1].append(demand[0][i])
            transactions[2].append(demand[1][i])
            supply[1][j] -= demand[1][i]
            demand[1][i] = 0
            i += 1
        else:
            transactions[0].append(supply[0][j])
            transactions[1].append(demand[0][i])
            transactions[2].append(supply[1][j])
            demand[1][i] -= supply[1][j]
            supply[1][j] = 0
            j += 1

    matchingResult = [[] for _ in range(2)]
    if len(demand[0]) == i:
        flexFlag = 0
        for k in range(j, len(supply[0])):
            matchingResult[0].append(supply[0][k])
            matchingResult[1].append(supply[1][k])
    elif len(supply[0]) == j:
        flexFlag = 1
        for k in range(i, len(demand[0])):
            matchingResult[0].append(demand[0][k])
            matchingResult[1].append(demand[1][k])

    return flexFlag, transactions, matchingResult
