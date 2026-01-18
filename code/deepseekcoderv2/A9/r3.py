from collections import deque

def is_valid(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def bfs(start, end, grid):
    if not is_valid(*start, grid) or not is_valid(*end, grid):
        return None

    queue = deque([(start[0], start[1], [])])
    visited = set((start[0], start[1]))
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        x, y, path = queue.popleft()
        if (x, y) == end:
            return path + [(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, grid) and (nx, ny) not in visited:
                queue.append((nx, ny, path + [(x, y)]))
                visited.add((nx, ny))
    return None

# Beispiel-Grid mit Hindernissen (1 für Hindernis, 0 für freien Platz)
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
end = (4, 4)

path = bfs(start, end, grid)
if path:
    print("Der kürzeste Pfad von", start, "nach", end, "ist:", path)
else:
    print("Es gibt keinen Pfad zwischen", start, "und", end)