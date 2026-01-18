def quick_sort(arr, low, high):
    """
    Sortiert ein Array in-place mit dem Quick-Sort-Algorithmus.
    
    Parameters:
    arr (list): Liste von Zahlen
    low (int): Startindex
    high (int): Endindex
    """
    if low < high:
        # Partitioniere das Array und erhalte den Pivot-Index
        pi = partition(arr, low, high)
        
        # Rekursiv die beiden Hälften sortieren
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    """
    Partitioniert das Array und setzt alle kleineren Elemente links,
    größere rechts vom Pivot (Lomuto-Partitionierung).
    
    Returns:
    int: Index des Pivots nach Partitionierung
    """
    pivot = arr[high]  # Pivot ist das letzte Element
    i = low - 1  # Index des kleineren Elements
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Tausche
    # Setze Pivot an die richtige Stelle
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Beispielnutzung:
if __name__ == "__main__":
    arr = [10, 7, 8, 9, 1, 5]
    print("Ursprüngliches Array:", arr)
    quick_sort(arr, 0, len(arr) - 1)
    print("Sortiertes Array:   ", arr)
