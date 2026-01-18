from collections import deque

# Define the grid size and start/goal positions
grid_size = 10
start = (0, 0)
goal = (9, 9)

# Define the grid with obstacles (0 represents free space, 1 represents an obstacle)
grid = [
    [0][0][0][0][0][0][0][0][0][0],
    [0][0][0][0][0][0][0][0][1][0],
    [0][1][1][0][0][0][0][0][1][0],
    [0][0][0][0][0][0][0][0][1][0],
    [0][0][0][0][0][0][0][0][1][0],
    [0][0][0][0][0][0][0][0][1][0],
    [0][0][0][0][0][0][0][0][1][0],
    [0][0][0][0][0][0][0][0][1][0],
    [0][0][0][0][0][0][0][0][1][0],
    [0][0][0][0][0][0][0][0][0][0]
]

def bfs(grid, start, goal):
    # Directions for moving up, down, left, right
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Initialize the queue with the starting position and path
    queue = deque([(start, [start])])
    
    # Keep track of visited positions to avoid cycles
    visited = set()
    visited.add(start)
    
    while queue:
        current, path = queue.popleft()
        
        # Check if we have reached the goal
        if current == goal:
            return path
        
        # Explore neighbors
        for direction in directions:
            new_position = (current[0] + direction[0], current[1] + direction[1])
            
            # Check if the new position is within bounds and not an obstacle
            if 0 <= new_position[0] < grid_size and 0 <= new_position[1] < grid_size and grid[new_position[0]][new_position[1]] == 0:
                # If the position hasn't been visited, add it to the queue
                if new_position not in visited:
                    visited.add(new_position)
                    queue.append((new_position, path + [new_position]))
    
    # Return None if no path is found
    return None

# Find the shortest path using BFS
path = bfs(grid, start, goal)

if path:
    print("Shortest path found:", path)
else:
    print("No path found")