"""
Pathfinding-Algorithmen: BFS und DFS
Findet Pfade in einem 2D-Raum mit Hindernissen
"""

from collections import deque
from typing import List, Tuple, Optional, Set


class Grid:
    """Repräsentiert ein 2D-Gitter für Pfadfindung"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.obstacles: Set[Tuple[int, int]] = set()
    
    def add_obstacle(self, x: int, y: int):
        """Fügt ein Hindernis hinzu"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.obstacles.add((x, y))
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Prüft, ob eine Position begehbar ist"""
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                (x, y) not in self.obstacles)
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Gibt alle begehbaren Nachbarn einer Position zurück"""
        x, y = pos
        # 4-Richtungen: oben, rechts, unten, links
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def visualize(self, path: Optional[List[Tuple[int, int]]] = None):
        """Visualisiert das Gitter mit optionalem Pfad"""
        path_set = set(path) if path else set()
        start = path[0] if path else None
        goal = path[-1] if path else None
        
        print("\n" + "─" * (self.width * 2 + 1))
        for y in range(self.height):
            row = "│"
            for x in range(self.width):
                pos = (x, y)
                if pos == start:
                    row += "S "  # Start
                elif pos == goal:
                    row += "G "  # Goal/Ziel
                elif pos in path_set:
                    row += "• "  # Pfad
                elif pos in self.obstacles:
                    row += "█ "  # Hindernis
                else:
                    row += "  "  # Leer
            row += "│"
            print(row)
        print("─" * (self.width * 2 + 1))


def bfs_pathfinding(grid: Grid, start: Tuple[int, int], 
                    goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Breadth-First Search - Findet den KÜRZESTEN Pfad
    
    Args:
        grid: Das 2D-Gitter
        start: Startposition (x, y)
        goal: Zielposition (x, y)
    
    Returns:
        Liste von Positionen vom Start zum Ziel, oder None wenn kein Pfad existiert
    """
    if not grid.is_walkable(*start) or not grid.is_walkable(*goal):
        return None
    
    if start == goal:
        return [start]
    
    # Queue für BFS: (position, pfad_bis_hierher)
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        # Prüfe alle Nachbarn
        for neighbor in grid.get_neighbors(current):
            if neighbor == goal:
                # Ziel gefunden!
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    # Kein Pfad gefunden
    return None


def dfs_pathfinding(grid: Grid, start: Tuple[int, int], 
                    goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Depth-First Search - Findet einen GÜLTIGEN Pfad (nicht unbedingt den kürzesten)
    
    Args:
        grid: Das 2D-Gitter
        start: Startposition (x, y)
        goal: Zielposition (x, y)
    
    Returns:
        Liste von Positionen vom Start zum Ziel, oder None wenn kein Pfad existiert
    """
    if not grid.is_walkable(*start) or not grid.is_walkable(*goal):
        return None
    
    if start == goal:
        return [start]
    
    visited = set()
    
    def dfs_recursive(current: Tuple[int, int], path: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
        """Rekursive DFS-Hilfsfunktion"""
        if current == goal:
            return path
        
        visited.add(current)
        
        # Durchsuche alle Nachbarn
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                result = dfs_recursive(neighbor, path + [neighbor])
                if result is not None:
                    return result
        
        return None
    
    return dfs_recursive(start, [start])


def dfs_pathfinding_iterative(grid: Grid, start: Tuple[int, int], 
                               goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Depth-First Search (iterativ mit Stack)
    Alternative iterative Implementierung von DFS
    
    Args:
        grid: Das 2D-Gitter
        start: Startposition (x, y)
        goal: Zielposition (x, y)
    
    Returns:
        Liste von Positionen vom Start zum Ziel, oder None wenn kein Pfad existiert
    """
    if not grid.is_walkable(*start) or not grid.is_walkable(*goal):
        return None
    
    if start == goal:
        return [start]
    
    # Stack für DFS: (position, pfad_bis_hierher)
    stack = [(start, [start])]
    visited = {start}
    
    while stack:
        current, path = stack.pop()
        
        # Prüfe alle Nachbarn
        for neighbor in grid.get_neighbors(current):
            if neighbor == goal:
                # Ziel gefunden!
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    
    # Kein Pfad gefunden
    return None


def compare_algorithms(grid: Grid, start: Tuple[int, int], goal: Tuple[int, int]):
    """Vergleicht BFS und DFS für denselben Pfad"""
    print(f"\n{'='*50}")
    print(f"Pfadfindung von {start} nach {goal}")
    print(f"{'='*50}")
    
    # BFS
    print("\n🔵 BFS (Breadth-First Search):")
    bfs_path = bfs_pathfinding(grid, start, goal)
    if bfs_path:
        print(f"   ✓ Pfad gefunden! Länge: {len(bfs_path)} Schritte")
        print(f"   Pfad: {' → '.join(map(str, bfs_path))}")
    else:
        print("   ✗ Kein Pfad gefunden")
    
    # DFS (rekursiv)
    print("\n🔴 DFS (Depth-First Search - Rekursiv):")
    dfs_path = dfs_pathfinding(grid, start, goal)
    if dfs_path:
        print(f"   ✓ Pfad gefunden! Länge: {len(dfs_path)} Schritte")
        print(f"   Pfad: {' → '.join(map(str, dfs_path))}")
    else:
        print("   ✗ Kein Pfad gefunden")
    
    # DFS (iterativ)
    print("\n🟣 DFS (Depth-First Search - Iterativ):")
    dfs_iter_path = dfs_pathfinding_iterative(grid, start, goal)
    if dfs_iter_path:
        print(f"   ✓ Pfad gefunden! Länge: {len(dfs_iter_path)} Schritte")
        print(f"   Pfad: {' → '.join(map(str, dfs_iter_path))}")
    else:
        print("   ✗ Kein Pfad gefunden")
    
    # Visualisierung
    if bfs_path:
        print("\n📍 Visualisierung mit BFS-Pfad (kürzester Pfad):")
        grid.visualize(bfs_path)
    
    if dfs_path and bfs_path and len(dfs_path) != len(bfs_path):
        print("\n📍 Visualisierung mit DFS-Pfad (zum Vergleich):")
        grid.visualize(dfs_path)


def main():
    """Hauptprogramm mit verschiedenen Testszenarien"""
    
    # Szenario 1: Einfaches Gitter ohne Hindernisse
    print("\n" + "="*60)
    print("SZENARIO 1: Einfaches Gitter (10x10)")
    print("="*60)
    grid1 = Grid(10, 10)
    compare_algorithms(grid1, (0, 0), (9, 9))
    
    # Szenario 2: Gitter mit Hindernissen
    print("\n" + "="*60)
    print("SZENARIO 2: Gitter mit Hindernissen (15x10)")
    print("="*60)
    grid2 = Grid(15, 10)
    
    # Vertikale Wand mit Lücke
    for y in range(8):
        if y != 4:  # Lücke bei y=4
            grid2.add_obstacle(7, y)
    
    # Horizontale Hindernisse
    for x in range(3, 12):
        if x not in [6, 7, 8]:
            grid2.add_obstacle(x, 5)
    
    compare_algorithms(grid2, (1, 1), (13, 8))
    
    # Szenario 3: Unmöglicher Pfad
    print("\n" + "="*60)
    print("SZENARIO 3: Unmöglicher Pfad (blockiert)")
    print("="*60)
    grid3 = Grid(10, 10)
    
    # Komplette vertikale Wand
    for y in range(10):
        grid3.add_obstacle(5, y)
    
    compare_algorithms(grid3, (2, 5), (8, 5))
    
    print("\n" + "="*60)
    print("Legende:")
    print("  S = Start")
    print("  G = Goal/Ziel")
    print("  • = Pfad")
    print("  █ = Hindernis")
    print("="*60)
    
    print("\n📊 Zusammenfassung:")
    print("   • BFS findet immer den KÜRZESTEN Pfad")
    print("   • DFS findet einen GÜLTIGEN Pfad (möglicherweise nicht der kürzeste)")
    print("   • Beide Algorithmen garantieren, dass sie einen Pfad finden, wenn einer existiert")
    print("   • BFS verwendet eine Queue (FIFO), DFS einen Stack (LIFO)")


if __name__ == "__main__":
    main()