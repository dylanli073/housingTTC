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


test_g = [[(1, 10)], [(2, 12)], [(3, 13)], [(4, 16)], [(5, 14)],
         [(6, 16)], [(7, 15)], [(8, 14)], [(9, 13)], [(10, 16)],
         [(11, 16)], [(0, 11)]]
min_weight, cycle = findCycle(test_g)
print(executeSwaps(test_g, min_weight, cycle))