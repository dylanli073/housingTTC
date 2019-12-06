import random

house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8, 
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1:"Adams", 2:"Cabot", 3:"Currier", 4:"Dunster", 5:"Eliot", 6:"Kirkland", 7:"Leverett", 8:"Lowell", 
    9:"Mather", 10:"Pfoho", 11:"Quincy", 12:"Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Leverett": {}, "Lowell": {}, "Kirkland":{},
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size


def runBaseline(groupSize):
    """Function runs TTC for the blocking groups, accepts preferences and round # as inputs, 
    outputs paired trades, updates global ledger
    """
    iteration = {"Adams": 0, "Cabot": 0, "Currier": 0, "Dunster": 0, "Eliot": 0, "Kirkland": 0, "Leverett": 0, "Lowell": 0, 
            "Mather": 0, "Pfoho": 0, "Quincy": 0, "Winthrop": 0}
    allHouses = set(["Adams", "Cabot", "Currier", "Dunster", "Eliot", "Kirkland", "Leverett", "Lowell", 
            "Mather", "Pfoho", "Quincy", "Winthrop"])
    numTrades = 0

    empty_houses = set()
    # shuffling each list, RSD mechanism implemented by each house
    # RSD mechanism for ranking within each house, if that house is chosen
    for house in allHouses: 
        try:
            random.shuffle(group_prefs[house][groupSize])
        except: 
            empty_houses.add(house)

    while len(empty_houses) < 11: 
        remainingHouses = allHouses.difference(empty_houses)

        # RSD
        chosen_house = random.sample(remainingHouses, 1)[0]

        # finding first house that can be matched with available groups
        prefs = group_prefs[chosen_house][groupSize][iteration[chosen_house]]
        house_number = house_mapping[chosen_house]
        curr_house_pref = prefs[2].index(house_number) # ranking of preference on currently assigned house
        index = 0
        target_house = ""

        # checking if target house is available before currently assigned house
        for i in range(curr_house_pref + 1):
            index += 1
            if num_mapping[prefs[2][i]] not in empty_houses:
                target_house = num_mapping[prefs[2][i]]
                break
        if curr_house_pref <= index: 
            group_prefs[chosen_house][groupSize].pop(iteration[chosen_house])
            if len(group_prefs[chosen_house][groupSize]) - 1 <= iteration[chosen_house]: # checking if iterations is greater than the number that want to trade
                empty_houses.add(chosen_house) # already in visited set, will not be visited later
            if len(group_prefs[chosen_house][groupSize]) <= 0:
                group_prefs[chosen_house].pop(groupSize)            
            continue

        available_groups = group_prefs[target_house][groupSize]
        ret_pref = []
        for index1,  group in enumerate(available_groups):
            if group[2].index(house_number) < group[2].index(house_mapping[group[1]]):
                ret_pref.append(group[2].index(house_number))
        
        if len(ret_pref) > 0:
            # finding the group in other house that most prefers this house
            best_match = ret_pref.index(min(ret_pref))

            # perform swap here
            numTrades += groupSize
            group_prefs[chosen_house][groupSize].pop(iteration[chosen_house])
            if len(group_prefs[chosen_house][groupSize]) - 1 <= iteration[chosen_house]: # checking if iterations is greater than the number that want to trade
                empty_houses.add(chosen_house) # already in visited set, will not be visited later
            if len(group_prefs[chosen_house][groupSize]) <= 0:
                group_prefs[chosen_house].pop(groupSize)

            # same, remove for target house as well
            numTrades += groupSize
            if best_match < iteration[target_house]:
                iteration[target_house] -= 1
            group_prefs[target_house][groupSize].pop(best_match)
            if len(group_prefs[target_house][groupSize]) - 1 <= iteration[target_house]: # checking if iterations is greater than the number that want to trade
                empty_houses.add(target_house) # already in visited set, will not be visited later
            if len(group_prefs[target_house][groupSize]) <= 0:
                group_prefs[target_house].pop(groupSize)
        else: 
            iteration[chosen_house] += 1
            if len(group_prefs[chosen_house][groupSize]) - 1 <= iteration[chosen_house]: # checking if iterations is greater than the number that want to trade
                empty_houses.add(chosen_house)
                if len(group_prefs[chosen_house][groupSize]) <= 0:
                    group_prefs[chosen_house].pop(groupSize)
    return numTrades


def main():
    """Main function accepts input and keeps track of total swaps
    """
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
        if len(set(pref_list[3:])) != len(pref_list[3:]):
            print("\nIncorrect preference order format")
            return False

        # consider if blocking group name is used before
        try:
            group_prefs[startingHouse][groupSize].append((blocking_name, startingHouse, (list(map(int, pref_list[3:])))))
        except:
            group_prefs[startingHouse][groupSize] = [(blocking_name, startingHouse, (list(map(int, pref_list[3:]))))]
    # running 8 rounds for all of the possible blocking group sizes
    rounds = 8

    for groupSize in range(rounds, 0, -1): 
        # preprocessing the lists in dictionary to order by the largest group size firsts
        print("Running submarket of group size " + str(groupSize))

        # how far down preferences we want to traverse, range is set to level of preferences
        totalTrades += runBaseline(groupSize)
        print("Total Swaps: " + str(totalTrades))
    return totalTrades

if __name__ == "__main__":
    main()