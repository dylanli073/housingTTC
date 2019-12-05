import random

house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8, 
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1:"Adams", 2:"Cabot", 3:"Currier", 4:"Dunster", 5:"Eliot", 6:"Kirkland", 7:"Leverett", 8:"Lowell", 
    9:"Mather", 10:"Pfoho", 11:"Quincy", 12:"Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Leverett": {}, "Lowell": {}, 
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size
totalTrades = 0

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
            group_prefs[startingHouse][groupSize].append((blocking_name, (map(int, input[3:]))))
        except:
            group_prefs[startingHouse][groupSize] = [(blocking_name, (map(int, input[3:])))]

    # running 8 rounds for all of the possible blocking group sizes
    rounds = 8
    # graph = preprocessing(rounds)

    for groupSize in range(rounds): 
        # preprocessing the lists in dictionary to order by the largest group size first
        graph = preprocessing(groupSize)
        if len(graph) == 0:
            return False
        print("Running group size of size " + str(groupSize))
        runTTC(graph, groupSize)

    return totalTrades
# def preprocessing(total): 
#     """preprocessing pairs up items into groups, both by size and the most preferred item available, 
#     and this output is used as the method by which each round matches and finds cycles
#     """
#     pairs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Leverett": {}, "Lowell": {}, 
#     "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}}

#     # pairing up by group size, according to target
#     for key, house in group_prefs.items():
#         frontPtr, endPtr = 0, total
#         # within each house, comparing groups to see if they would form a pair pointing to same house
#         while frontPtr <= endPtr:
#             try: 
#                 for group in house[frontPtr]:
#                     for comp_group in house[endPtr]:
#                         if group[1][0] == comp_group[1][0]:
#                             names = [group[0], comp_group[0]]
#                             try:
#                                 pairs[house][total].append([names, group[1][0]])
#                             except:
#                                 pairs[house][total] = [[names, group[1][0]]]
#             except ValueError:
#                 pass 
#             finally:
#                 frontPtr += 1
#                 endPtr -= 1
#     return pairs


def runTTC(groupSize):
    """Function runs TTC for the blocking groups, accepts preferences and round # as inputs, 
    outputs paired trades, updates global ledger
    """
    iteration = {"Adams": 0, "Cabot": 0, "Currier": 0, "Dunster": 0, "Eliot": 0, "Kirkland": 0, "Leverett": 0, "Lowell": 0, 
            "Mather": 0, "Pfoho": 0, "Quincy": 0, "Winthrop": 0}
    allHouses = set(["Adams", "Cabot", "Currier", "Dunster", "Eliot", "Kirkland", "Leverett", "Lowell", 
            "Mather", "Pfoho", "Quincy", "Winthrop"])

    # shuffling each list 
    for house in remainingHouses: 
        random.shuffle(group_prefs[house][groupSize])

    empty_houses = set()

    halted = False # checks if there is a stall in the TTC, where one group must move down
    while len(empty_houses) < 11: # some case for when TTC would end for size 8 blocking group size
        remainingHouses = allHouses.difference(empty_houses)
        if halted:
            chosen_house = random.sample(remainingHouses, 1)[0] # move one down ledger for this house
            iteration[chosen_house] += 1
            if iteration[chosen_house] >= len(group_prefs[house][groupSize])
                empty_houses.add(chosen_house)
                continue

        # adding the names and preference ordering for each node within the graph
        graph_nodes = []
        for house in remainingHouses: 
            associated_houses[house] = group_prefs[house][groupSize][iteration[chosen_house]][0] # name asssociated with each house
            graph_nodes.append(associated_houses[house]) # returns the tuple associated

        visited = set()
        graph = preprocessing(graph_nodes)
        def runDFS(house):
            """Graph search algorithm for finding cycles, accepts input graph in adjacency list format, outputs cycles
            and clears the current market, returns number of cycles cleared
            """
            visited.add(house)
            stack = [house]
            remainingHouses.remove(house)
            while graph[house] not in visited:
                house = graph[house]
                remainingHouses.remove(house)
                stack.append(graph[house])
            try: 
                cycle_start = stack.index(graph[house])
                for house in range(cycle_start, len(stack)):
                    iteration[house] += 1
                    # making the trade here

                    totalTrades += groupSize

                    if iteration[house] >= len(group_prefs[house][groupSize]) # checking if iterations is greater than the 
                        empty_houses.add(house) # already in visited set, will not be visited later
                return True
            except ValueError:
                return False
                
        # based on guarantee that each node has one outgoing edge
        halted = True
        while len(remainingHouses) > 0:
            if runDFS(random.sample(remainingHouses, 1)[0]): 
                halted = False


def preprocessing(graph_nodes):
    """preprocessing creates adjacency list representation for the given length
        and this output is used as the method by which each round matches and finds cycles
    """
    adjacency_list = {}
    for node in graph_nodes: 
        adjacency_list[node[1][1]] = num_mapping[node[1][2]] # node[1][2] is the top choice house, num_mapping translates to house name
    return adjacency_list


if __name__ == "__main__":
    main()