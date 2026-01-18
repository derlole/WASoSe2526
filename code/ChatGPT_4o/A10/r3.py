def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    def partition(arr, low, high):
        # Pivot als letztes Element wählen
        pivot = arr[high]
        i = low - 1  # Index für das kleinere Element
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]  # Elemente tauschen
        # Pivot an die richtige Position setzen
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    if low < high:
        pi = partition(arr, low, high)
        # Rekursiv die linke und rechte Partition sortieren
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

# Beispielnutzung:
arr = [10, 7, 8, 9, 1, 5]
quicksort(arr)
print("Sortiertes Array:", arr)
