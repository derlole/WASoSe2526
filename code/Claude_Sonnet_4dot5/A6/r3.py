def quicksort(arr, low=0, high=None):
    """
    Sortiert einen Array in aufsteigender Reihenfolge mit Quicksort.
    
    Args:
        arr: Liste von Zahlen, die sortiert werden soll
        low: Startindex (Standard: 0)
        high: Endindex (Standard: len(arr) - 1)
    
    Returns:
        Der sortierte Array (in-place modifiziert)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partitioniere den Array und erhalte den Pivot-Index
        pivot_index = partition(arr, low, high)
        
        # Rekursiv die beiden Hälften sortieren
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)
    
    return arr


def partition(arr, low, high):
    """
    Partitioniert den Array um einen Pivot-Wert.
    
    Args:
        arr: Der Array
        low: Startindex der Partition
        high: Endindex der Partition
    
    Returns:
        Der finale Index des Pivot-Elements
    """
    # Wähle das letzte Element als Pivot
    pivot = arr[high]
    
    # Index des kleineren Elements
    i = low - 1
    
    # Durchlaufe alle Elemente und verschiebe kleinere nach links
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Setze Pivot an die richtige Position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1


# Test-Beispiele
if __name__ == "__main__":
    # Test 1: Unsortierter Array
    test1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {test1}")
    quicksort(test1)
    print(f"Sortiert: {test1}")
    
    # Test 2: Bereits sortiert
    test2 = [1, 2, 3, 4, 5]
    quicksort(test2)
    print(f"Bereits sortiert: {test2}")
    
    # Test 3: Rückwärts sortiert
    test3 = [9, 7, 5, 3, 1]
    quicksort(test3)
    print(f"Rückwärts sortiert: {test3}")
    
    # Test 4: Mit Duplikaten
    test4 = [5, 2, 8, 2, 9, 1, 5, 5]
    quicksort(test4)
    print(f"Mit Duplikaten: {test4}")
    
    # Test 5: Negative Zahlen
    test5 = [-5, 3, -1, 7, -8, 2]
    quicksort(test5)
    print(f"Mit negativen Zahlen: {test5}")
