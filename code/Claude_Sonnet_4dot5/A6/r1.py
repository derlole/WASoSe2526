def quicksort(arr, left=None, right=None):
    """
    Sortiert einen Array in aufsteigender Reihenfolge mit Quicksort.
    
    Args:
        arr: Liste von Zahlen
        left: Startindex (default: 0)
        right: Endindex (default: len(arr)-1)
    
    Returns:
        Sortierter Array (in-place Modifikation)
    """
    # Initialisierung beim ersten Aufruf
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    # Basisfall: Array mit 0 oder 1 Element
    if left >= right:
        return arr
    
    # Partition durchführen
    pivot_index = partition(arr, left, right)
    
    # Rekursiv linke und rechte Teilarrays sortieren
    quicksort(arr, left, pivot_index - 1)
    quicksort(arr, pivot_index + 1, right)
    
    return arr


def partition(arr, left, right):
    """
    Partitioniert den Array um ein Pivot-Element.
    Elemente kleiner als Pivot kommen nach links, größere nach rechts.
    
    Args:
        arr: Array zum Partitionieren
        left: Startindex
        right: Endindex
        
    Returns:
        Index der finalen Pivot-Position
    """
    # Pivot-Element (mittleres Element für bessere Performance)
    mid = (left + right) // 2
    pivot = arr[mid]
    
    # Pivot ans Ende verschieben
    arr[mid], arr[right] = arr[right], arr[mid]
    
    # Partitionierung
    store_index = left
    for i in range(left, right):
        if arr[i] < pivot:
            arr[i], arr[store_index] = arr[store_index], arr[i]
            store_index += 1
    
    # Pivot an finale Position bringen
    arr[store_index], arr[right] = arr[right], arr[store_index]
    
    return store_index


# Test-Beispiele
if __name__ == "__main__":
    # Testfall 1: Unsortierter Array
    test1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {test1}")
    quicksort(test1)
    print(f"Sortiert: {test1}")
    
    # Testfall 2: Bereits sortiert
    test2 = [1, 2, 3, 4, 5]
    print(f"\nOriginal: {test2}")
    quicksort(test2)
    print(f"Sortiert: {test2}")
    
    # Testfall 3: Umgekehrt sortiert
    test3 = [9, 7, 5, 3, 1]
    print(f"\nOriginal: {test3}")
    quicksort(test3)
    print(f"Sortiert: {test3}")
    
    # Testfall 4: Negative Zahlen
    test4 = [-5, 3, -1, 7, 0, -8, 2]
    print(f"\nOriginal: {test4}")
    quicksort(test4)
    print(f"Sortiert: {test4}")
    
    # Testfall 5: Duplikate
    test5 = [5, 2, 8, 2, 9, 1, 5, 5]
    print(f"\nOriginal: {test5}")
    quicksort(test5)
    print(f"Sortiert: {test5}")
    
    # Testfall 6: Einzelnes Element
    test6 = [42]
    print(f"\nOriginal: {test6}")
    quicksort(test6)
    print(f"Sortiert: {test6}")
    
    # Testfall 7: Leerer Array
    test7 = []
    print(f"\nOriginal: {test7}")
    quicksort(test7)
    print(f"Sortiert: {test7}")