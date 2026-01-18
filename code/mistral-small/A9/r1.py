from collections import deque

def is_valid(grid, x, y):
    # Überprüft, ob der Punkt (x, y) gültig ist (innerhalb des Gitters und kein Hindernis)
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 1

def bfs(start, end):
    # Initialisiere das Gitter
    rows = len(start)
    cols = len(start[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # BFS-Queue initialisieren
    queue = deque([start])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    visited[start[0]][start[1]] = True

    while queue:
        current_x, current_y = queue.popleft()

        # Wenn der Endpunkt erreicht ist, den Pfad zurückverfolgen und speichern
        if (current_x, current_y) == end:
            path = []
            while (current_x, current_y) != start:
                path.append((current_x, current_y))
                # Bestimme die Richtung des vorherigen Schritts
                if (current_x, current_y) in directions:
                    dir = directions[current_x][current_y]
                    next_x = current_x - dir[0]
                    next_y = current_y - dir[1]
                else:
                    # Falls kein vorheriger Schritt gefunden wird, ist der Pfad ungültig
                    return []
                current_x, current_y = next_x, next_y
            path.append(start)
            return path[::-1]  # Rückwärts aufgelistet, also umkehren

        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy
            if is_valid(grid, new_x, new_y) and not visited[new_x][new_y]:
                queue.append((new_x, new_y))
                visited[new_x][new_y] = True

    return []  # Kein Pfad gefunden

# Beispielgitter mit Hindernissen (1 für frei, 0 für Hindernis)
grid = [
    [1, 0, 1, 1],
    [1, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 1, 1, 1]
]

start = (0, 0)
end = (3, 3)

path = bfs(start, end)
print("Kürzester Pfad:", path)