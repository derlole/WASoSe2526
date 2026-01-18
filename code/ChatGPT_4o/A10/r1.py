def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Partitioniere das Array und finde den Pivot-Index
        pivot_index = partition(arr, low, high)
        # Rekursiv die linke und rechte Seite sortieren
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

def partition(arr, low, high):
    # Wähle den Pivot als letztes Element
    pivot = arr[high]
    i = low - 1  # Index für das "kleiner als Pivot"-Segment

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Tausche Elemente
    # Setze den Pivot an die richtige Position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Beispiel:
numbers = [33, 10, 55, 71, 29, 3, 18]
print("Vorher:", numbers)
quicksort(numbers)
print("Nachher:", numbers)
