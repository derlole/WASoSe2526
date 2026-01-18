from collections import deque

def bfs_shortest_path(grid, start, goal):
    """
    Findet den kürzesten Pfad in einem 2D-Raster von start zu goal unter Verwendung von BFS.
    
    grid: 2D-Liste, 0 = frei, 1 = Hindernis
    start: Tuple (x, y)
    goal: Tuple (x, y)
    
    Rückgabe: Liste von Punkten, die den Pfad darstellen, oder None, wenn kein Pfad existiert.
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]
    
    # Queue für BFS initialisieren
    queue = deque([start])
    visited[start[0]][start[1]] = True
    
    # Bewegungen: oben, unten, links, rechts
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    while queue:
        current = queue.popleft()
        if current == goal:
            # Pfad rekonstruiert
            path = []
            while current:
                path.append(current)
                current = parent[current[0]][current[1]]
            return path[::-1]  # umkehren
        
        for d in directions:
            nr, nc = current[0] + d[0], current[1] + d[1]
            if 0 <= nr < rows and 0 <= nc < cols:
                if not visited[nr][nc] and grid[nr][nc] == 0:
                    queue.append((nr, nc))
                    visited[nr][nc] = True
                    parent[nr][nc] = current
    return None

# Beispielnutzung
if __name__ == "__main__":
    # 0 = frei, 1 = Hindernis
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
        print("Kürzester Pfad gefunden:")
        print(path)
    else:
        print("Kein Pfad möglich.")
