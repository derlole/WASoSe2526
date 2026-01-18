from collections import deque

def bfs_shortest_path(grid, start, goal):
    """
    Findet den kürzesten Pfad von start nach goal in einem 2D-Gitter unter Verwendung von BFS.
    
    grid: 2D-Liste von 0 (frei) und 1 (Hindernis)
    start: Tuple (x, y)
    goal: Tuple (x, y)
    
    Rückgabe: Liste von Punkten, die den Pfad darstellen, oder None, wenn kein Pfad existiert
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]
    
    # Richtungen: rechts, links, unten, oben
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    
    queue = deque([start])
    visited[start[0]][start[1]] = True
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == goal:
            # Pfad zurückverfolgen
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = parent[x][y] if parent[x][y] is not None else (None, None)
            return path[::-1]  # umkehren, damit Start -> Ziel
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == 0:
                visited[nx][ny] = True
                parent[nx][ny] = (x, y)
                queue.append((nx, ny))
    
    return None  # Kein Pfad gefunden

# Beispiel-Gitter
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
]

start = (0, 0)
goal = (3, 4)

path = bfs_shortest_path(grid, start, goal)
if path:
    print("Gefundener Pfad:", path)
else:
    print("Kein Pfad möglich.")
