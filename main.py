# still needs to run over multiple preferences, 1-12

import random

house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8, 
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1:"Adams", 2:"Cabot", 3:"Currier", 4:"Dunster", 5:"Eliot", 6:"Kirkland", 7:"Leverett", 8:"Lowell", 
    9:"Mather", 10:"Pfoho", 11:"Quincy", 12:"Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Kirkland":{}, "Leverett": {}, "Lowell": {},
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size

def main():
    total_groups = int(raw_input())
    totalTrades = 0
    # accept groups in the format: {[(['groupname'], 'Quincy', [10, 5, 7, 2, 9, 4, 3, 8, 1, 12, 6])]
    # adding each individual into the system, with group name and preference ordering
    for group in range(total_groups):
        input = list(raw_input().split())
        blocking_name = input[0]
        groupSize = int(input[1])
        startingHouse = input[2]

        if groupSize < 0 or groupSize > 8:
            print("\nInput group size between 1 and 8 inclusive")
            return False

        # checking if one house appears twice in preference ordering, checking if original house appears in order
        if len(set(specs[3:] + [str(house_mapping[startingHouse])])) != len(specs[3:] + [str(house_mapping[startingHouse])]):
            print("\nIncorrect preference order format")
            return False

        # consider if blocking group name is used before
        try:
            group_prefs[startingHouse][groupSize].append((blocking_name, list((map(int, specs[3:])))))
        except:
            group_prefs[startingHouse][groupSize] = [(blocking_name, list(map(int, specs[3:])))]
    print(group_prefs)
    # running 8 rounds for all of the possible blocking group sizes
    # rounds = 8
    # graph = preprocessing(8)
    # for groupSize in range(rounds):
    #     # preprocessing the lists in dictionary to order by the largest group size first
    #     graph = preprocessing(groupSize)
    #     if len(graph) == 0:
    #         return False
    #     print("Running group size of size " + str(groupSize))
    #     runTTC(graph, groupSize)

def preprocessing(total): 
    """preprocessing pairs up items into groups, both by size and the most preferred item available, 
    and this output is used as the method by which each round matches and finds cycles
    """
    pairs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Leverett": {}, "Lowell": {}, 
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}}

    # pairing up by group size, according to target
    for key, house in group_prefs.items():
        frontPtr, endPtr = 0, total
        # within each house, comparing groups to see if they would form a pair pointing to same house
        while frontPtr <= endPtr:
            try: 
                for group in house[frontPtr]:
                    for comp_group in house[endPtr]:
                        if group[1][0] == comp_group[1][0]:
                            names = [group[0], comp_group[0]]
                            try:
                                pairs[house][total].append([names, group[1][0]])
                            except:
                                pairs[house][total] = [[names, group[1][0]]]
            except ValueError:
                pass 
            finally:
                frontPtr += 1
                endPtr -= 1
    return pairs

def runTTC(prefs, round):
    """Function runs TTC for the blocking groups, accepts preferences and round # as inputs, 
    outputs paired trades, updates global ledger
    """


def removeGroups():
    """Cleans up and removes groups that have already been used"""

def multiGraphMaker(block_size, group_prefs):
    house_graph = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Kirkland":{}, "Leverett": {}, "Lowell": {},
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}}
    for name, house in group_prefs.items():
        out_edges = [0] * 12
        for _, pref in house[block_size]:
            out_edges[pref[0]-1] += 1
        for k in range(len(out_edges)):
            if out_edges[k] != 0:
                house_graph[name] = (num_mapping[k], out_edges[k])
    print(house_graph)


def runDFS():
    """Graph search algorithm for finding cycles, accepts input graph in adjacency list format, outputs cycles
    and clears the current market, returns number of cycles cleared
    """
    # running 8 rounds for all of the possible blocking group sizes
    rounds = 8
    # graph = preprocessing(rounds)

    for groupSize in range(rounds, 0, -1): 
        # preprocessing the lists in dictionary to order by the largest group size firsts
        print("Running group size of size " + str(groupSize))
        totalTrades += runTTC(groupSize)
        print("totaltrades: " + str(totalTrades))
    return totalTrades

if __name__ == "__main__":
    main()