import random

house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7,
                 "Lowell": 8, "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1: "Adams", 2: "Cabot", 3: "Currier", 4: "Dunster", 5: "Eliot", 6: "Kirkland", 7: "Leverett",
               8: "Lowell", 9: "Mather", 10: "Pfoho", 11: "Quincy", 12: "Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Kirkland":{}, "Leverett": {}, "Lowell": {},
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size


def process(g, n, p, u, v, e, mw, c_i, data):
    u.remove(n)
    v.add(n)
    if g[n]:
        for (next, w) in g[n]:
            if w < mw:
                mw = w
            if next in u:
                p[next] = n
                c_i, data, e, u, v = process(g, next, p, u, v, e, mw, c_i, data)
            elif next in v and not c_i:
                c_i = 1
                seen_neighbors = 1
                for a, _ in g[next]:
                    if a in u:
                        seen_neighbors = seen_neighbors * 0
                c_i = c_i - seen_neighbors
                if c_i:
                    p[next] = n
                    cycle = [next]
                    pointer = p[next]
                    while pointer != next and p[pointer] is not None:
                        cycle.append(pointer)
                        pointer = p[pointer]
                    return (c_i, (mw, cycle), e, u, v)

    else:
        if n in v:
            v.remove(n)
            e.add(n)
    return (c_i, data, e, u, v)


def findCycle(g):
    unvisited = set(range(len(g)))
    visited = set()
    explored = set()
    parents = [None] * len(g)
    min_weight = 1
    min_weight_set = False
    for i in range(len(g)):
        if g[i] and not min_weight_set:
            min_weight_set = True
            min_weight = g[i][0][1]
    data = (False, None)
    c_i = False
    k = -1

    while (not c_i) and k < len(g) - 1:
        k += 1
        if g[k] and k in unvisited:
            unvisited.remove(k)
            visited.add(k)
            for (next, w) in g[k]:
                if w < min_weight:
                    min_weight = w
                if next not in visited and next not in explored:
                    parents[next] = k
                    c_i, data, explored, unvisited, visited = process(g, next, parents, unvisited, visited, explored,
                                                                         min_weight, c_i, data)
        else:
            if k in visited:
                visited.remove(k)
                explored.add(k)
    return data


def executeSwaps(g, block_size, round, min_weight, cycle, group_list):
    new_list = group_list
    for house in range(len(cycle)):
        try:
            parent = cycle[house + 1]
        except:
            parent = cycle[0]
        edge_found = False
        edge = -1
        while not edge_found:
            edge += 1
            v, w = g[parent][edge]
            if v == cycle[house] and w - min_weight > 0:
                edge_found = True
                g[parent][edge] = (v, w - min_weight)
            elif v == cycle[house] and w - min_weight == 0:
                g[parent].pop(edge)
                edge_found = True

            if edge_found:
                p_i = False
                iter = -1
                while not p_i and iter < len(new_list):
                    iter += 1
                    gs, sh, plist = new_list[iter]
                    if block_size == gs and sh == num_mapping[parent+1] and plist[round]-1 == v:
                        p_i = True
                        new_list.pop(iter)
    return g, new_list


def multiGraphMaker(block_size, gl, round):
    house_graph = [[] for i in range(12)]
    house_prefs = {"Adams":[0 for i in range(12)], "Cabot": [0 for i in range(12)], "Currier": [0 for i in range(12)],
                   "Dunster": [0 for i in range(12)], "Eliot": [0 for i in range(12)], "Kirkland":[0 for i in range(12)],
                   "Leverett": [0 for i in range(12)], "Lowell": [0 for i in range(12)], "Mather": [0 for i in range(12)],
                   "Pfoho": [0 for i in range(12)], "Quincy": [0 for i in range(12)], "Winthrop": [0 for i in range(12)]}
    edge_list = []
    for groupSize, s_house, prefs in gl:
        if groupSize == block_size:
            house_prefs[s_house][prefs[round]-1] += 1
    for groupSize, s_house, prefs in gl:
        if groupSize == block_size and (s_house, prefs[round]-1) not in edge_list and num_mapping[prefs[round]] != s_house:
            edge_list.append((s_house, prefs[round]-1))
            house_graph[house_mapping[s_house]-1].append((prefs[round]-1, house_prefs[s_house][prefs[round]-1]))

    return house_graph


def runRound(round, group_list):
    new_list = group_list
    multigraph = []
    for i in range(1, 9):
        multigraph.append(multiGraphMaker(i, group_list, round))
    total_swaps = 0
    for j in range(len(multigraph)):
        cycle_found = True
        while cycle_found:
            graph = multigraph[j]
            my_cycle = findCycle(graph)
            cycle_found = my_cycle[1] is not None
            if cycle_found:
                multigraph[j], new_list = executeSwaps(graph, j+1, round, my_cycle[0], my_cycle[1], group_list)
            try:
                total_swaps += (j + 1) * my_cycle[0] * len(my_cycle[1])
            except:
                total_swaps += 0
    return total_swaps, new_list


def main():
    total_groups = int(input("Input # of groups: "))
    group_list = []
    # accept groups in the format: [groupname, groupsize, starting house name, rankings] rep. in number values
    # adding each individual into the system, with group name and preference ordering
    for group in range(total_groups):
        specs = list(input().split())
        blocking_name = str(specs[0])
        groupSize = int(specs[1])
        startingHouse = specs[2]

        if groupSize < 0 or groupSize > 8:
            print("\nInput group size between 1 and 8 inclusive")
            return False
        group_list.append((groupSize, startingHouse, list((map(int, specs[3:])))))
        try:
            group_prefs[startingHouse][groupSize].append((blocking_name, list((map(int, specs[3:])))))
        except:
            group_prefs[startingHouse][groupSize] = [(blocking_name, list(map(int, specs[3:])))]
    total_swaps = 0
    for r in range(1, 9):
        swaps, my_list = runRound(r, group_list)
        total_swaps += swaps
        group_list = my_list
    return total_swaps

if __name__ == "__main__":
    print(main())