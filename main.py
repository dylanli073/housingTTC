# still needs to run over multiple preferences, 1-12

import random

house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8, 
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1:"Adams", 2:"Cabot", 3:"Currier", 4:"Dunster", 5:"Eliot", 6:"Kirkland", 7:"Leverett", 8:"Lowell", 
    9:"Mather", 10:"Pfoho", 11:"Quincy", 12:"Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Leverett": {}, "Lowell": {}, "Kirkland":{},
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size


def runTTC(groupSize, pref_number):
    """Function runs TTC for the blocking groups, accepts preferences and round # as inputs, 
    outputs paired trades, updates global ledger
    """
    # iteration = {"Adams": 0, "Cabot": 0, "Currier": 0, "Dunster": 0, "Eliot": 0, "Kirkland": 0, "Leverett": 0, "Lowell": 0, 
    #         "Mather": 0, "Pfoho": 0, "Quincy": 0, "Winthrop": 0}
    allHouses = set(["Adams", "Cabot", "Currier", "Dunster", "Eliot", "Kirkland", "Leverett", "Lowell", 
            "Mather", "Pfoho", "Quincy", "Winthrop"])
    numTrades = 0


    empty_houses = set()
    # shuffling each list, RSD mechanism implemented by each house
    for house in allHouses: 
        try:
            random.shuffle(group_prefs[house][groupSize])
        except: 
            empty_houses.add(house)

    halted = False # checks if there is a stall in the TTC, where one group must move down
    while len(empty_houses) < 11: # some case for when TTC would end for size 8 blocking group size
        remainingHouses = allHouses.difference(empty_houses)
        if halted:
            chosen_house = random.sample(remainingHouses, 1)[0] # move one down ledger for this house
            # iteration[chosen_house] += 1
            # print("DL1", house, iteration[chosen_house], len(group_prefs[chosen_house][groupSize]))
            group_prefs[chosen_house][groupSize].pop(0)
            if len(group_prefs[chosen_house][groupSize]) <= 0:
                empty_houses.add(chosen_house)
                continue
        # adding the names and preference ordering for each node within the graph
        graph_nodes = []

        for house in remainingHouses: 
            graph_nodes.append(group_prefs[house][groupSize][0]) # returns the tuple associated
        visited = set()
        graph = preprocessing(graph_nodes, pref_number)

        def runDFS(house):
            """Graph search algorithm for finding cycles, accepts input graph in adjacency list format, outputs cycles
            and clears the current market, returns number of cycles cleared
            """
            visited.add(house)
            stack = [house]
            numTradesDFS = 0
            remainingHouses.remove(house)
            if house not in graph:
                remainingHouses.remove(house)

            # check this while loop, should be finding the house and removing house when it has been considered, consider switching *visited* to *remainingHouses*
            while house in graph and graph[house] not in visited: # while house in remainingHouses? 
                house = graph[house]
                if house in remainingHouses:
                    remainingHouses.remove(house)
                    stack.append(house)
                else:
                    return 0
            try: 
                cycle_start = stack.index(graph[house])
                for chose_house in range(cycle_start, len(stack)):
                    housename = stack[chose_house]
                    # iteration[housename] += 1

                    # making the trade here
                    numTradesDFS = numTradesDFS + groupSize
                    group_prefs[housename][groupSize].pop(0)
                    if len(group_prefs[housename][groupSize]) <= 0: # checking if iterations is greater than the number that want to trade
                        empty_houses.add(housename) # already in visited set, will not be visited later
                        group_prefs[housename].pop(groupSize)
                return numTradesDFS
            except ValueError: 
                return 0
                
        # based on guarantee that each node has one outgoing edge
        halted = True
        while len(remainingHouses) > 0:
            subtraded = runDFS(random.sample(remainingHouses, 1)[0])
            if subtraded > 0: 
                halted = False
                numTrades += subtraded
        return numTrades


def preprocessing(graph_nodes, pref_number):
    """preprocessing creates adjacency list representation for the given length
        and this output is used as the method by which each round matches and finds cycles
    """
    adjacency_list = {}
    for node in graph_nodes: 
        adjacency_list[node[1]] = num_mapping[node[2][pref_number]] # node[1][2] is the top choice house, num_mapping translates to house name
    return adjacency_list


def main():
    total_groups = int(input())
    totalTrades = 0
    # accept groups in the format: {[(['groupname'], 'Quincy', [10, 5, 7, 2, 9, 4, 3, 8, 1, 12, 6])]
    # adding each individual into the system, with group name and preference ordering
    for group in range(total_groups):
        pref_list = list(input().split())
        blocking_name = pref_list[0]
        groupSize = int(pref_list[1])
        startingHouse = pref_list[2]

        if groupSize < 0 or groupSize > 8:
            print("\nInput group size between 1 and 8 inclusive")
            return False

        # checking if one house appears twice in preference ordering, checking if original house appears in order
        if len(set(pref_list[3:] + [str(house_mapping[startingHouse])])) != len(pref_list[3:] + [str(house_mapping[startingHouse])]):
            print("\nIncorrect preference order format")
            return False

        # consider if blocking group name is used before
        try:
            group_prefs[startingHouse][groupSize].append((blocking_name, startingHouse, (list(map(int, pref_list[3:])))))
        except:
            group_prefs[startingHouse][groupSize] = [(blocking_name, startingHouse, (list(map(int, pref_list[3:]))))]
    # running 8 rounds for all of the possible blocking group sizes
    rounds = 8
    # graph = preprocessing(rounds)

    print(group_prefs)

    for groupSize in range(rounds, 0, -1): 
        # preprocessing the lists in dictionary to order by the largest group size firsts
        print("Running group size of size " + str(groupSize))
        for pref_number in range(5):
            totalTrades += runTTC(groupSize, pref_number)
        print("totaltrades: " + str(totalTrades))
    return totalTrades

if __name__ == "__main__":
    main()