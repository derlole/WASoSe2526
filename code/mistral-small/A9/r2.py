from collections import deque

# Definition der Richtungen für die Bewegung im 2D-Raum
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(x, y, grid):
    """Überprüft, ob der Punkt (x, y) gültig ist und keine Hindernisse darstellt."""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def bfs_shortest_path(start, end):
    """Findet den kürzesten Pfad zwischen 'start' und 'end' in einem 2D-Raum mit Hindernissen."""
    x1, y1 = start
    x2, y2 = end

    # Erstellen Sie die 2D-Grid-Matrix
    grid_size = max(x1, x2) + 1
    grid = [[0] * grid_size for _ in range(grid_size)]

    # Setzen Sie die Start- und Endpunkte im Grid
    start_point = (x1, y1)
    end_point = (x2, y2)
    if is_valid(start_point[0], start_point[1], grid):
        grid[start_point[0]][start_point[1]] = 1  # Hindernis setzen
    if is_valid(end_point[0], end_point[1], grid):
        grid[end_point[0]][end_point[1]] = 1  # Hindernis setzen

    # Initialisiere die Warteschlange für BFS und besuche das Startfeld
    queue = deque([start])
    visited = set()
    visited.add(start)
    steps = 0

    while queue:
        for _ in range(len(queue)):
            x, y = queue.popleft()

            if (x, y) == end:
                return steps

            # Überprüfen Sie alle möglichen Richtungen
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny, grid):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        steps += 1

    return -1  # Kein Pfad gefunden

# Beispiel: Verbinden Sie (0, 0) mit (2, 2) in einem 3x3-Grid
start = (0, 0)
end = (2, 2)
print(bfs_shortest_path(start, end))  # Ausgabe: 4