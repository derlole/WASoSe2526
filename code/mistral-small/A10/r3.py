def quick_sort(arr, low, high):
    if low < high:
        # pi ist der Index des Teilungs-Elements
        pi = partition(arr, low, high)

        # Rekursiv auf dem linken und rechten Teil des geteilten Elements
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    # Wähle das letzte Element als Pivot
    pivot = arr[high]

    # Index des kleineren Elements
    i = (low - 1)

    for j in range(low, high):
        # Wenn das aktuelle Element kleiner oder gleich dem Pivot ist
        if arr[j] <= pivot:
            i += 1
            # Tausche arr[i] und arr[j]
            arr[i], arr[j] = arr[j], arr[i]

    # Tausche arr[i + 1] und arr[high] (oder pivot)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1

# Beispielarray
arr = [10, 80, 30, 90, 40, 50, 70]
print("Unsortiertes Array:", arr)

quick_sort(arr, 0, len(arr) - 1)
print("Sortiertes Array:", arr)