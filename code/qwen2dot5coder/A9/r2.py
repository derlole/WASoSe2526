from collections import deque

def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = set(start)
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = current[0] + dx, current[1] + dy
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0 and (x, y) not in visited:
                visited.add((x, y))
                parent[(x, y)] = current
                queue.append((x, y))
    
    return None

# Example usage:
grid = [
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
end = (4, 4)

path = bfs(grid, start, end)

if path:
    print("Path found:", path)
else:
    print("No path found")