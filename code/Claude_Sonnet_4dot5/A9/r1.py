#!/usr/bin/env python3
"""
Pathfinding-Programm mit BFS und DFS
Findet den kürzesten Weg zwischen zwei Punkten in einem 2D-Gitter mit Hindernissen
"""

from collections import deque
from typing import List, Tuple, Set, Optional


class Pathfinder:
    """Klasse für Wegfindung in einem 2D-Gitter"""
    
    def __init__(self, grid: List[List[int]]):
        """
        Initialisiert den Pathfinder
        
        Args:
            grid: 2D-Liste wo 0 = begehbar, 1 = Hindernis
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        
    def is_valid(self, row: int, col: int, visited: Set[Tuple[int, int]]) -> bool:
        """
        Überprüft, ob eine Position gültig ist
        
        Args:
            row: Zeile
            col: Spalte
            visited: Set der bereits besuchten Positionen
            
        Returns:
            True wenn die Position gültig ist, sonst False
        """
        return (0 <= row < self.rows and 
                0 <= col < self.cols and
                self.grid[row][col] == 0 and
                (row, col) not in visited)
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Gibt alle gültigen Nachbarpositionen zurück (4-Richtungen)
        
        Args:
            pos: Aktuelle Position (row, col)
            
        Returns:
            Liste der Nachbarpositionen
        """
        row, col = pos
        # 4 Richtungen: oben, rechts, unten, links
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            neighbors.append((new_row, new_col))
            
        return neighbors
    
    def bfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Breadth-First Search: Findet den kürzesten Pfad
        
        Args:
            start: Startposition (row, col)
            goal: Zielposition (row, col)
            
        Returns:
            Liste der Positionen im Pfad oder None wenn kein Pfad existiert
        """
        # Validierung der Start- und Zielposition
        if not (0 <= start[0] < self.rows and 0 <= start[1] < self.cols):
            return None
        if not (0 <= goal[0] < self.rows and 0 <= goal[1] < self.cols):
            return None
        if self.grid[start[0]][start[1]] == 1 or self.grid[goal[0]][goal[1]] == 1:
            return None
            
        # Queue für BFS: (position, pfad_bis_hierher)
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current_pos, path = queue.popleft()
            
            # Ziel erreicht?
            if current_pos == goal:
                return path
            
            # Alle Nachbarn untersuchen
            for neighbor in self.get_neighbors(current_pos):
                if self.is_valid(neighbor[0], neighbor[1], visited):
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        # Kein Pfad gefunden
        return None
    
    def dfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Depth-First Search: Findet einen gültigen Pfad (nicht notwendigerweise der kürzeste)
        
        Args:
            start: Startposition (row, col)
            goal: Zielposition (row, col)
            
        Returns:
            Liste der Positionen im Pfad oder None wenn kein Pfad existiert
        """
        # Validierung der Start- und Zielposition
        if not (0 <= start[0] < self.rows and 0 <= start[1] < self.cols):
            return None
        if not (0 <= goal[0] < self.rows and 0 <= goal[1] < self.cols):
            return None
        if self.grid[start[0]][start[1]] == 1 or self.grid[goal[0]][goal[1]] == 1:
            return None
        
        visited = set()
        path = []
        
        def dfs_recursive(pos: Tuple[int, int]) -> bool:
            """Rekursive DFS-Hilfsfunktion"""
            if pos == goal:
                path.append(pos)
                return True
            
            visited.add(pos)
            path.append(pos)
            
            # Alle Nachbarn untersuchen
            for neighbor in self.get_neighbors(pos):
                if self.is_valid(neighbor[0], neighbor[1], visited):
                    if dfs_recursive(neighbor):
                        return True
            
            # Backtracking: diese Position führt nicht zum Ziel
            path.pop()
            return False
        
        if dfs_recursive(start):
            return path
        return None


def print_grid_with_path(grid: List[List[int]], path: Optional[List[Tuple[int, int]]] = None):
    """
    Gibt das Gitter mit dem Pfad formatiert aus
    
    Args:
        grid: Das 2D-Gitter
        path: Optional der gefundene Pfad
    """
    if path is None:
        path = []
    
    path_set = set(path)
    
    print("\nGitter-Visualisierung:")
    print("  ", end="")
    for col in range(len(grid[0])):
        print(f"{col:2}", end=" ")
    print()
    
    for row in range(len(grid)):
        print(f"{row:2}", end=" ")
        for col in range(len(grid[0])):
            if (row, col) in path_set:
                if (row, col) == path[0]:
                    print(" S", end=" ")  # Start
                elif (row, col) == path[-1]:
                    print(" Z", end=" ")  # Ziel
                else:
                    print(" ·", end=" ")  # Pfad
            elif grid[row][col] == 1:
                print(" █", end=" ")  # Hindernis
            else:
                print(" .", end=" ")  # Freies Feld
        print()


def main():
    """Hauptfunktion mit Beispielen"""
    
    print("=" * 60)
    print("Pathfinding mit BFS und DFS")
    print("=" * 60)
    
    # Beispiel 1: Einfaches Gitter
    print("\n--- Beispiel 1: Einfaches Gitter ---")
    grid1 = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    pathfinder1 = Pathfinder(grid1)
    start1 = (0, 0)
    goal1 = (4, 4)
    
    print(f"\nStart: {start1}, Ziel: {goal1}")
    
    # BFS
    path_bfs1 = pathfinder1.bfs(start1, goal1)
    if path_bfs1:
        print(f"\n✓ BFS Pfad gefunden (Länge: {len(path_bfs1)})")
        print(f"Pfad: {' → '.join([f'({r},{c})' for r, c in path_bfs1])}")
        print_grid_with_path(grid1, path_bfs1)
    else:
        print("\n✗ BFS: Kein Pfad gefunden")
    
    # DFS
    path_dfs1 = pathfinder1.dfs(start1, goal1)
    if path_dfs1:
        print(f"\n✓ DFS Pfad gefunden (Länge: {len(path_dfs1)})")
        print(f"Pfad: {' → '.join([f'({r},{c})' for r, c in path_dfs1])}")
        print_grid_with_path(grid1, path_dfs1)
    else:
        print("\n✗ DFS: Kein Pfad gefunden")
    
    # Beispiel 2: Komplexeres Labyrinth
    print("\n\n--- Beispiel 2: Komplexes Labyrinth ---")
    grid2 = [
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    
    pathfinder2 = Pathfinder(grid2)
    start2 = (0, 0)
    goal2 = (4, 6)
    
    print(f"\nStart: {start2}, Ziel: {goal2}")
    
    # BFS
    path_bfs2 = pathfinder2.bfs(start2, goal2)
    if path_bfs2:
        print(f"\n✓ BFS Pfad gefunden (Länge: {len(path_bfs2)})")
        print_grid_with_path(grid2, path_bfs2)
    else:
        print("\n✗ BFS: Kein Pfad gefunden")
    
    # DFS
    path_dfs2 = pathfinder2.dfs(start2, goal2)
    if path_dfs2:
        print(f"\n✓ DFS Pfad gefunden (Länge: {len(path_dfs2)})")
        print_grid_with_path(grid2, path_dfs2)
    else:
        print("\n✗ DFS: Kein Pfad gefunden")
    
    # Beispiel 3: Kein Pfad möglich
    print("\n\n--- Beispiel 3: Blockierter Pfad ---")
    grid3 = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    pathfinder3 = Pathfinder(grid3)
    start3 = (0, 0)
    goal3 = (0, 4)
    
    print(f"\nStart: {start3}, Ziel: {goal3}")
    print_grid_with_path(grid3)
    
    # BFS
    path_bfs3 = pathfinder3.bfs(start3, goal3)
    if path_bfs3:
        print(f"\n✓ BFS Pfad gefunden (Länge: {len(path_bfs3)})")
    else:
        print("\n✗ BFS: Kein Pfad gefunden (blockiert durch Hindernisse)")
    
    # DFS
    path_dfs3 = pathfinder3.dfs(start3, goal3)
    if path_dfs3:
        print(f"\n✓ DFS Pfad gefunden (Länge: {len(path_dfs3)})")
    else:
        print("\n✗ DFS: Kein Pfad gefunden (blockiert durch Hindernisse)")
    
    print("\n" + "=" * 60)
    print("Vergleich BFS vs DFS:")
    print("- BFS findet immer den KÜRZESTEN Pfad")
    print("- DFS findet EINEN gültigen Pfad (kann länger sein)")
    print("- Beide behandeln Hindernisse korrekt")
    print("=" * 60)


if __name__ == "__main__":
    main()
