import random

house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8,
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1:"Adams", 2:"Cabot", 3:"Currier", 4:"Dunster", 5:"Eliot", 6:"Kirkland", 7:"Leverett", 8:"Lowell",
    9:"Mather", 10:"Pfoho", 11:"Quincy", 12:"Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Kirkland":{}, "Leverett": {}, "Lowell": {},
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size


def process(g, n, p, u, v, e, mw, c_i):
    u.remove(n)
    v.add(n)
    if g[n]:
        for (next, w) in g[n]:
            if w < mw:
                mw = w
            if next not in v and next not in e:
                p[next] = n
                c_i, data = process(g, next, p, u, v, e, mw, c_i)
            elif next in v and not c_i:
                c_i = True
                p[next] = n
                cycle = [next]
                pointer = p[next]
                while pointer != next and p[pointer] is not None:
                    cycle.append(pointer)
                    pointer = p[pointer]
                return (c_i, (mw, cycle))

    else:
        v.remove(n)
        e.add(n)
    return (c_i, data)

def findCycle(g):
    unvisited = set(range(len(g)))
    visited = set()
    explored = set()
    parents = [None] * len(g)
    min_weight = g[0][0][1]
    c_i = False
    i = -1

    while not c_i and i < len(g):
        i += 1
        if g[i] and i in unvisited:
            unvisited.remove(i)
            visited.add(i)
            for (next, w) in g[i]:
                if w < min_weight:
                    min_weight = w
                if next not in visited and next not in explored:
                    parents[next] = i
                    c_i, my_data = process(g, next, parents, unvisited, visited, explored, min_weight,c_i)
        else:
            visited.remove(i)
            explored.add(i)
    return my_data

def executeSwaps(g, min_weight, cycle):
    for house in range(len(cycle)):
        try:
            parent = cycle[house + 1]
        except:
            parent = cycle[0]
        for edge in range(len(g[cycle[parent]])):
            v, w = g[parent][edge]
            if v == cycle[house]:
                g[parent][edge] = (v, w-min_weight)
    return g

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

def main():
    total_groups = int(input("Input # of groups: "))

    # accept groups in the format: [groupname, groupsize, starting house name, rankings] rep. in number values
    # adding each individual into the system, with group name and preference ordering
    for group in range(total_groups):
        specs = list(input().split())
        groupSize = int(specs[0])
        startingHouse = specs[1]
        blocking_name = specs[2]

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

if __name__ == "__main__":
    main()