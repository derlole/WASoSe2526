def quicksort(arr, low, high):
    if low < high:
        # Pi ist der Index des Pivot-Elements
        pi = partition(arr, low, high)

        # Rekursiv auf dem linken und rechten Teil anwenden
        quicksort(arr, low, pi-1)
        quicksort(arr, pi+1, high)

def partition(arr, low, high):
    i = (low-1)  # Index des kleineren Elements
    pivot = arr[high]  # Pivot

    for j in range(low, high):
        # Wenn das aktuelle Element kleiner oder gleich dem Pivot ist
        if arr[j] <= pivot:
            i += 1
            # Tausche arr[i] und arr[j]
            arr[i], arr[j] = arr[j], arr[i]

    # Tausche arr[i+1] und arr[high] (oder pivot)
    arr[i+1], arr[high] = arr[high], arr[i+1]

    return i + 1

# Beispielarray zum Testen
arr = [10, 7, 8, 9, 1, 5]
n = len(arr)
quicksort(arr, 0, n-1)
print("Sortiertes Array:")
print(arr)