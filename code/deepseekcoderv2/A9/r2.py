from collections import deque

def is_valid(x, y):
    # Hier können Sie Ihre eigene Logik für Hindernisse hinzufügen
    return 0 <= x < 10 and 0 <= y < 10

def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set()
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == goal:
            return path
        
        if (x, y) not in visited:
            visited.add((x, y))
            
            # Hier können Sie die Nachbarn von (x, y) hinzufügen
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny) and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
    
    return None

# Beispiel zur Verwendung der Funktion
start = (0, 0)
goal = (9, 9)
path = bfs(start, goal)
if path:
    print("Der kürzeste Pfad von", start, "nach", goal, "ist:", path)
else:
    print("Es gibt keinen Pfad von", start, "nach", goal)