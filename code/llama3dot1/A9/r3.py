from collections import deque

class Graph:
    def __init__(self):
        self.nodes = set()
        self.graph = {}

    def add_node(self, node):
        self.nodes.add(node)
        self.graph[node] = []

    def add_edge(self, node1, node2):
        self.graph[node1].append(node2)
        self.graph[node2].append(node1)

def bfs(graph, start, end, obstacles):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in obstacles and node == end:
            return path

        for neighbor in graph.graph[node]:
            if neighbor not in visited and neighbor not in obstacles:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                visited.add(neighbor)

    return None

# Beispiel-Verwendung
graph = Graph()

# Hinzufügen von Knoten
graph.add_node('A')
graph.add_node('B')
graph.add_node('C')
graph.add_node('D')

# Hinzufügen von Kanten
graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('B', 'D')
graph.add_edge('C', 'D')

obstacles = {'C'}  # Knoten C ist ein Hindernis

start_node = 'A'
end_node = 'D'

path = bfs(graph, start_node, end_node, obstacles)
if path:
    print("Der schnellste Weg von {} zu {} ist: {}".format(start_node, end_node, " -> ".join(path)))
else:
    print("Kein Pfad gefunden")