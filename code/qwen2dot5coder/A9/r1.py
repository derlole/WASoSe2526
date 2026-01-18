from collections import deque

def bfs_shortest_path(grid, start, end):
    # Directions for moving up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Initialize queue with the starting point and a path containing only the start point
    queue = deque([(start, [start])])
    
    # Set to keep track of visited nodes
    visited = set()
    visited.add(start)
    
    while queue:
        current, path = queue.popleft()
        
        # If we reach the end, return the path
        if current == end:
            return path
        
        # Explore neighbors
        for direction in directions:
            next_x, next_y = current[0] + direction[0], current[1] + direction[1]
            neighbor = (next_x, next_y)
            
            # Check if the neighbor is within bounds and not an obstacle or visited
            if 0 <= next_x < len(grid) and 0 <= next_y < len(grid[0]) and grid[next_x][next_y] == 0 and neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)
    
    # If no path is found
    return None

# Example usage
grid = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]

start = (0, 0)
end = (3, 2)

path = bfs_shortest_path(grid, start, end)
print("Shortest Path:", path)