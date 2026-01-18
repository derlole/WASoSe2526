"""
Pathfinding in 2D Space using BFS and DFS
==========================================
Dieses Programm implementiert Breitensuche (BFS) und Tiefensuche (DFS)
um Pfade in einem 2D-Gitter mit Hindernissen zu finden.

BFS findet immer den kuerzesten Pfad.
DFS findet einen Pfad, aber nicht notwendigerweise den kuerzesten.
"""

from collections import deque
from typing import List, Tuple, Optional, Set


class Pathfinder:
    """Klasse fuer Pfadfindung in einem 2D-Gitter"""
    
    def __init__(self, grid: List[List[int]]):
        """
        Initialisiert den Pathfinder mit einem Gitter.
        
        Args:
            grid: 2D-Liste, wobei 0 = frei, 1 = Hindernis
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        
        # Moegliche Bewegungsrichtungen (oben, unten, links, rechts)
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def is_valid(self, row: int, col: int, visited: Set[Tuple[int, int]]) -> bool:
        """Prueft, ob eine Position gueltig ist."""
        return (0 <= row < self.rows and 
                0 <= col < self.cols and 
                self.grid[row][col] == 0 and 
                (row, col) not in visited)
    
    def bfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Breadth-First Search (BFS) - findet den kuerzesten Pfad.
        """
        if not (0 <= start[0] < self.rows and 0 <= start[1] < self.cols):
            print("Fehler: Startposition ausserhalb des Gitters")
            return None
        if not (0 <= goal[0] < self.rows and 0 <= goal[1] < self.cols):
            print("Fehler: Zielposition ausserhalb des Gitters")
            return None
        if self.grid[start[0]][start[1]] == 1:
            print("Fehler: Startposition ist ein Hindernis")
            return None
        if self.grid[goal[0]][goal[1]] == 1:
            print("Fehler: Zielposition ist ein Hindernis")
            return None
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            (current_row, current_col), path = queue.popleft()
            
            if (current_row, current_col) == goal:
                return path
            
            for dr, dc in self.directions:
                new_row, new_col = current_row + dr, current_col + dc
                
                if self.is_valid(new_row, new_col, visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append(((new_row, new_col), new_path))
        
        return None
    
    def dfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Depth-First Search (DFS) - findet einen Pfad.
        """
        if not (0 <= start[0] < self.rows and 0 <= start[1] < self.cols):
            print("Fehler: Startposition ausserhalb des Gitters")
            return None
        if not (0 <= goal[0] < self.rows and 0 <= goal[1] < self.cols):
            print("Fehler: Zielposition ausserhalb des Gitters")
            return None
        if self.grid[start[0]][start[1]] == 1:
            print("Fehler: Startposition ist ein Hindernis")
            return None
        if self.grid[goal[0]][goal[1]] == 1:
            print("Fehler: Zielposition ist ein Hindernis")
            return None
        
        stack = [(start, [start])]
        visited = {start}
        
        while stack:
            (current_row, current_col), path = stack.pop()
            
            if (current_row, current_col) == goal:
                return path
            
            for dr, dc in self.directions:
                new_row, new_col = current_row + dr, current_col + dc
                
                if self.is_valid(new_row, new_col, visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    stack.append(((new_row, new_col), new_path))
        
        return None
    
    def visualize_path(self, path: Optional[List[Tuple[int, int]]], 
                       start: Tuple[int, int], goal: Tuple[int, int]) -> None:
        """Visualisiert das Gitter mit dem gefundenen Pfad."""
        if path is None:
            print("\nKein Pfad gefunden!")
            return
        
        visual = [row[:] for row in self.grid]
        
        for row, col in path:
            if (row, col) != start and (row, col) != goal:
                visual[row][col] = 2
        
        visual[start[0]][start[1]] = 3
        visual[goal[0]][goal[1]] = 4
        
        symbols = {0: '.', 1: '#', 2: 'o', 3: 'S', 4: 'Z'}
        
        print("\nGitter-Visualisierung:")
        print("  " + "".join(f"{i%10}" for i in range(self.cols)))
        for i, row in enumerate(visual):
            print(f"{i%10} " + "".join(symbols[cell] for cell in row))
        
        print(f"\nLegende: S=Start, Z=Ziel, o=Pfad, #=Hindernis, .=Frei")
        print(f"Pfadlaenge: {len(path)} Schritte")


def create_sample_grid() -> List[List[int]]:
    """Erstellt ein Beispiel-Gitter mit Hindernissen"""
    return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


def main():
    """Hauptfunktion mit Beispielen"""
    print("=" * 60)
    print("Pathfinding mit BFS und DFS")
    print("=" * 60)
    
    grid = create_sample_grid()
    pathfinder = Pathfinder(grid)
    
    start = (0, 0)
    goal = (9, 9)
    
    print(f"\nSuche Pfad von {start} nach {goal}")
    
    print("\n" + "=" * 60)
    print("BFS (Breadth-First Search) - findet kuerzesten Pfad")
    print("=" * 60)
    bfs_path = pathfinder.bfs(start, goal)
    pathfinder.visualize_path(bfs_path, start, goal)
    
    print("\n" + "=" * 60)
    print("DFS (Depth-First Search) - findet einen Pfad")
    print("=" * 60)
    dfs_path = pathfinder.dfs(start, goal)
    pathfinder.visualize_path(dfs_path, start, goal)
    
    if bfs_path and dfs_path:
        print("\n" + "=" * 60)
        print("Vergleich:")
        print("=" * 60)
        print(f"BFS-Pfadlaenge: {len(bfs_path)} Schritte (kuerzester Pfad)")
        print(f"DFS-Pfadlaenge: {len(dfs_path)} Schritte")
        if len(bfs_path) < len(dfs_path):
            print(f"BFS ist {len(dfs_path) - len(bfs_path)} Schritte kuerzer")
        elif len(bfs_path) == len(dfs_path):
            print("Beide Algorithmen fanden gleich lange Pfade")
    
    print("\n" + "=" * 60)
    print("Beispiel: Unmoeglicher Pfad")
    print("=" * 60)
    blocked_grid = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0]
    ]
    blocked_pathfinder = Pathfinder(blocked_grid)
    blocked_start = (0, 0)
    blocked_goal = (0, 4)
    blocked_path = blocked_pathfinder.bfs(blocked_start, blocked_goal)
    blocked_pathfinder.visualize_path(blocked_path, blocked_start, blocked_goal)


if __name__ == "__main__":
    main()
