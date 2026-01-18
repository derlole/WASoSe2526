from collections import deque

def bfs_shortest_path(grid, start, goal):
    """
    Findet den kürzesten Pfad in einem 2D-Grid von start zu goal.
    grid: 2D-Liste mit 0 = frei, 1 = Hindernis
    start, goal: (x, y) Koordinaten
    Rückgabe: Liste von Koordinaten des Pfades oder None, wenn kein Pfad existiert
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False]*cols for _ in range(rows)]
    prev = [[None]*cols for _ in range(rows)]
    
    queue = deque([start])
    visited[start[0]][start[1]] = True

    # Bewegungen: oben, unten, links, rechts
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while queue:
        x, y = queue.popleft()

        if (x, y) == goal:
            # Pfad rekonstruiere
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = prev[x][y] if prev[x][y] is not None else (None, None)
            return path[::-1]  # umkehren

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny] and grid[nx][ny] == 0:
                    queue.append((nx, ny))
                    visited[nx][ny] = True
                    prev[nx][ny] = (x, y)

    return None  # kein Pfad gefunden

# Beispiel
grid = [
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

path = bfs_shortest_path(grid, start, goal)

if path:
    print("Pfad gefunden:")
    print(path)
else:
    print("Kein Pfad verfügbar")
