def process(g, n, p, u, v, e, mw):
    data = ([], mw)
    u.remove(n)
    v.add(n)
    if g[n]:
        for (next, w) in g[n]:
            if w < mw:
                mw = w
            if next not in v and next not in e:
                p[next] = n
                process(g, next, p, u, v, e, mw)
            elif next in v:
                p[next] = n
                cycle = [next]
                pointer = p[next]
                while pointer != next:
                    cycle.append(pointer)
                    pointer = p[pointer]
                data = (cycle, mw)
    else:
        v.remove(n)
        e.add(n)
    return data
def findCycle(g):
    unvisited = set(range(len(g)))
    visited = set()
    explored = set()
    parents = [None] * len(g)
    min_weight = g[0][0][1]

    for i in range(len(g)):
        if i in unvisited:
            unvisited.remove(i)
            visited.add(i)
        if g[i]:
            for (next, w) in g[i]:
                if w < min_weight:
                    min_weight = w
                if next not in visited and next not in explored:
                    parents[next] = i
                    my_data = process(g, next, parents, unvisited, visited, explored, min_weight)
        else:
            visited.remove(i)
            explored.add(i)
    return my_data




test_g = [[(1, 2)], [(2, 1)], [(3, 1)], [(4, 1)], [(5, 1)],
         [(6, 1)], [(7, 1)], [(8, 1)], [(9, 1)], [(10, 1)],
         [(11, 1)], [(0, 1)]]
print(findCycle(test_g))
