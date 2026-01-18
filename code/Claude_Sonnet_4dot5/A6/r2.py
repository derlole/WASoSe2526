def quicksort(arr, low=None, high=None):
    """
    Sortiert einen Array in aufsteigender Reihenfolge mit Quicksort.
    
    Args:
        arr: Liste von Zahlen
        low: Startindex (optional, Standard: 0)
        high: Endindex (optional, Standard: len(arr)-1)
    
    Returns:
        Der sortierte Array (in-place modifiziert)
    """
    # Initialisierung beim ersten Aufruf
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1
    
    # Basisfall: Wenn der Bereich nur 0 oder 1 Element hat
    if low < high:
        # Partitioniere den Array und erhalte Pivot-Index
        pivot_index = partition(arr, low, high)
        
        # Rekursiv die beiden Teilbereiche sortieren
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)
    
    return arr


def partition(arr, low, high):
    """
    Partitioniert den Array um ein Pivot-Element.
    
    Args:
        arr: Liste von Zahlen
        low: Startindex des zu partitionierenden Bereichs
        high: Endindex des zu partitionierenden Bereichs
    
    Returns:
        Index der finalen Pivot-Position
    """
    # Wähle das letzte Element als Pivot
    pivot = arr[high]
    
    # Index des kleineren Elements
    i = low - 1
    
    # Durchlaufe den Array
    for j in range(low, high):
        # Wenn aktuelles Element kleiner oder gleich dem Pivot ist
        if arr[j] <= pivot:
            i += 1
            # Tausche arr[i] und arr[j]
            arr[i], arr[j] = arr[j], arr[i]
    
    # Setze das Pivot an die richtige Position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1


# Testfälle
if __name__ == "__main__":
    # Test 1: Normaler unsortierter Array
    arr1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr1}")
    quicksort(arr1)
    print(f"Sortiert: {arr1}")
    print()
    
    # Test 2: Bereits sortierter Array
    arr2 = [1, 2, 3, 4, 5]
    print(f"Original: {arr2}")
    quicksort(arr2)
    print(f"Sortiert: {arr2}")
    print()
    
    # Test 3: Rückwärts sortiert
    arr3 = [5, 4, 3, 2, 1]
    print(f"Original: {arr3}")
    quicksort(arr3)
    print(f"Sortiert: {arr3}")
    print()
    
    # Test 4: Array mit Duplikaten
    arr4 = [3, 7, 3, 1, 9, 3, 5]
    print(f"Original: {arr4}")
    quicksort(arr4)
    print(f"Sortiert: {arr4}")
    print()
    
    # Test 5: Einzelnes Element
    arr5 = [42]
    print(f"Original: {arr5}")
    quicksort(arr5)
    print(f"Sortiert: {arr5}")
    print()
    
    # Test 6: Leerer Array
    arr6 = []
    print(f"Original: {arr6}")
    quicksort(arr6)
    print(f"Sortiert: {arr6}")
    print()
    
    # Test 7: Negative Zahlen
    arr7 = [-5, 3, -1, 7, -9, 2]
    print(f"Original: {arr7}")
    quicksort(arr7)
    print(f"Sortiert: {arr7}")