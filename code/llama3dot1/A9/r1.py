from collections import deque

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

def is_valid(point, grid_size):
    """Überprüft, ob ein Punkt innerhalb eines 2D-Grids liegt"""
    return 0 <= point.x < grid_size and 0 <= point.y < grid_size

def bfs(start, target, obstacles):
    """
    Implementiert einen Breadth-First Search (BFS)-Algorithmus,
    um den schnellsten Weg zwischen zwei Punkten zu finden.

    Args:
        start (Point): Der Startpunkt.
        target (Point): Das Ziel.
        obstacles (List[Point]): Eine Liste von Hindernissen.

    Returns:
        List[Point] oder None: Ein Pfad, wenn ein Pfad gefunden wurde,
        sonst None.
    """
    queue = deque([(start, [start])])
    visited = set((start.x, start.y))

    while queue:
        (point, path) = queue.popleft()

        if point == target:
            return path

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = Point(point.x + dx, point.y + dy)

            if is_valid(neighbor, max(grid_size, grid_size)):
                if (neighbor.x, neighbor.y) not in visited and \
                   neighbor not in obstacles:
                    queue.append((neighbor, path + [neighbor]))
                    visited.add((neighbor.x, neighbor.y))

    return None

grid_size = 10
obstacles = [
    Point(1, 1),
    Point(2, 2),
]

start_point = Point(0, 0)
target_point = Point(grid_size - 1, grid_size - 1)

path = bfs(start_point, target_point, obstacles)

if path:
    print("Der schnellste Weg besteht aus den folgenden Punkten:")
    for point in path:
        print(point)
else:
    print("Kein Pfad gefunden.")