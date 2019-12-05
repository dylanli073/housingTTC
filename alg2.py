def findCycle(g, s_house):
    unvisited = set(range(len(g)))
    visited = {}
    explored = {}
    parents = [None] * len(g)
    unvisited.remove(s_house)
    visited.add(s_house)
    for (next, w) in g[s_house]:


test_g = [[(1, 2)], [(2, 1)], [(3, 1)], [(4, 1)], [(5, 1)],
         [(6, 1)], [(7, 1)], [(8, 1)], [(9, 1)], [(10, 1)],
         [(11, 1)], [(0, 1)]]
print(1)
