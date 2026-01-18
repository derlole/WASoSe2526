from collections import deque

def is_valid(x, y, grid):
    # Prüfen, ob der Punkt innerhalb des Gitters liegt und nicht ein Hindernis darstellt
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 1

def bfs(start, end):
    # Initialisieren der Breite-Erst-Suche
    queue = deque([start])
    visited = set()
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Umgekehrte Reihenfolge des Pfads zurückgeben

        visited.add(current)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_point = (current[0] + dx, current[1] + dy)
            if is_valid(next_point[0], next_point[1], grid):
                if next_point not in visited:
                    parent[next_point] = current
                    queue.append(next_point)
                    visited.add(next_point)

    return []  # Kein Pfad gefunden

def find_shortest_path(start, end, grid):
    start = (start[0], start[1])
    end = (end[0], end[1])

    if not is_valid(start[0], start[1], grid) or not is_valid(end[0], end[1], grid):
        return []  # Start- oder Zielpunkt ist ungültig

    path = bfs(start, end)
    return path

# Beispiel
grid = [
    [1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1]
]
start = (0, 0)
end = (3, 4)

path = find_shortest_path(start, end, grid)
print("Gefundener Pfad:", path)