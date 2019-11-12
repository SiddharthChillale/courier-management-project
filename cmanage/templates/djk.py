def findMin(graph, visited, d):
    minNode = -1
    min = float('inf')
    for i in range(len(graph)):
        if visited[i] == 0 and d[i] < min:
            min = d[i]
            minNode = i
    return minNode

def checkConnection(graph, u, v):
    # print('u is',u,'and v is',v)
    for i,j in enumerate(graph[u]):
        # print('i is', i, 'and j is', j)
        if j[0] == v:
            # print('yes connection is there and cost is', j[1])
            return True, j[1] # returns whether there is an edge in graph and the weight of it

    # print('No connection')
    return False, float('inf')

def dijkstra(graph, root):
    d = [float('inf')]*len(graph)
    visited = [0]*len(graph)
    d[root] = 0
    queue = []
    for k in range(len(graph)):
        u = findMin(graph, visited, d)
        visited[u] = 1
        # print('Min node is ', u)
        for i in range(len(graph)):
            x = checkConnection(graph, u, i)
            # print("x is ", x)
            if visited[i] == 0 and  x[0] and d[u] != float('inf') and d[u] + x[1] < d[i]:
                d[i] = d[u] + x[1]
    return d

graph = dict({
    0: [(1,10),(5,5)],
    1: [(0,10),(2,15),(4,16)],
    2: [(1, 10),(3,5),(4,17)],
    3: [(2,5),(4,5)],
    4: [(1,16),(2,17),(3,5)],
    5: [(0,5), (4,7)]
})

d = dijkstra(graph, 0)
print('Distances from node 0 are:')

for i in range(6):
        print(i,' : ', d[i])





Class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph(defaultdict(list))

    # funciton to add an edge
    def addEdge (self, u, v, w):
        if w== 1:
            self.graph[u].append(v,w)   