house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8,
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}
num_mapping = {1:"Adams", 2:"Cabot", 3:"Currier", 4:"Dunster", 5:"Eliot", 6:"Kirkland", 7:"Leverett", 8:"Lowell",
    9:"Mather", 10:"Pfoho", 11:"Quincy", 12:"Winthrop"}
group_prefs = {"Adams":{}, "Cabot": {}, "Currier": {}, "Dunster": {}, "Eliot": {}, "Kirkland":{}, "Leverett": {}, "Lowell": {},
    "Mather": {}, "Pfoho": {}, "Quincy": {}, "Winthrop": {}} # organized by house, then by group size


def process(g, n, p, u, v, e, mw, c_i, data):
    u.remove(n)
    v.add(n)
    if g[n]:
        for (next, w) in g[n]:
            if w < mw:
                mw = w
            if next not in v and next not in e:
                p[next] = n
                c_i, data = process(g, next, p, u, v, e, mw, c_i, data)
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
    data = (None, None)
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
                    c_i, my_data = process(g, next, parents, unvisited, visited, explored, min_weight, c_i, data)
        else:
            visited.remove(i)
            explored.add(i)
    return my_data

test_g = [[(5, 1), (2, 1), (10, 1), (6, 1), (7, 2)], [(4, 1), (7, 1), (6, 1), (11, 2)],
          [(1, 1), (5, 1), (0, 1), (7, 1)], [(2, 1), (9, 1), (10, 1)], [(1, 1), (9, 1), (0, 1), (10, 1), (3, 1)],
          [(7, 1), (11, 1), (2, 1)], [(2, 1), (9, 1)], [(0, 1), (6, 1), (8, 1), (2, 1), (9, 1)],
          [(5, 1), (6, 1), (4, 1)], [(4, 1), (3, 1), (0, 1)], [(1, 1), (7, 2), (11, 1), (3, 1)],
          [(9, 1), (0, 1), (7, 1)]]

print(findCycle(test_g))