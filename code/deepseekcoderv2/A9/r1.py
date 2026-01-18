from collections import deque

def bfs(graph, start, goal):
    queue = deque([start])
    visited = set()
    path = {start: []}
    
    while queue:
        current = queue.popleft()
        if current == goal:
            return build_path(path, current)
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path[neighbor] = path[current] + [current]
    
    return None  # If no path is found

def dfs(graph, start, goal):
    stack = [start]
    visited = set()
    path = {start: []}
    
    while stack:
        current = stack.pop()
        if current == goal:
            return build_path(path, current)
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                path[neighbor] = path[current] + [current]
    
    return None  # If no path is found

def build_path(path, goal):
    result = []
    current = goal
    while current:
        result.append(current)
        current = path.get(current)
    return result[::-1]

# Example usage with a grid and obstacles
def is_valid(x, y, grid):
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0:
        return True
    return False

def get_neighbors(node, grid):
    (x, y) = node
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, grid):
            neighbors.append((nx, ny))
    return neighbors

def create_graph(grid):
    graph = {}
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                node = (i, j)
                neighbors = get_neighbors(node, grid)
                graph[node] = neighbors
    return graph

# Example grid with obstacles
grid = [
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]

start_point = (0, 0)
goal_point = (3, 3)
graph = create_graph(grid)

print("BFS Path:", bfs(graph, start_point, goal_point))
print("DFS Path:", dfs(graph, start_point, goal_point))