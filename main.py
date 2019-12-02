import random

house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8, 
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1:"Adams", 2:"Cabot", 3:"Currier", 4:"Dunster", 5:"Eliot", 6:"Kirkland", 7:"Leverett", 8:"Lowell", 
    9:"Mather", 10:"Pfoho", 11:"Quincy", 12:"Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Leverett": {}, "Lowell": {}, 
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size

def main():
    total_groups = int(raw_input())

    # accept groups in the format: [groupsize, starting house name, rankings rep. in number values
    # adding each individual into the system, with group name and preference ordering
    for group in range(total_groups):
        input = list(raw_input().split())
        blocking_name = [input[0]]
        groupSize = int(input[1])
        startingHouse = input[2]

        if groupSize < 0 or groupSize > 8:
            print("\nInput group size between 1 and 8 inclusive")
            return False

        # checking if one house appears twice in preference ordering, checking if original house appears in order
        if len(set(input[3:] + [str(house_mapping[startingHouse])])) != len(input[3:] + [str(house_mapping[startingHouse])]):
            print("\nIncorrect preference order format")
            return False

        # consider if blocking group name is used before

        try:
            group_prefs[startingHouse][groupSize].append(blocking_name.append(map(int, input[3:])))
        except:
            group_prefs[startingHouse][groupSize] = [blocking_name.append(map(int, input[3:]))]

    # running 8 rounds for all of the possible blocking group sizes
    rounds = 8
    graph = preprocessing(8)
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


def runTTC(round):
    """Function runs TTC for the blocking groups, accepts preferences and round # as inputs, 
    outputs paired trades, updates global ledger
    """


def removeGroups()
    """Cleans up and removes groups that have already been used"""


def runDFS():
    """Graph search algorithm for finding cycles, accepts input graph in adjacency list format, outputs cycles
    and clears the current market, returns number of cycles cleared
    """


if __name__ == "__main__":
    main()