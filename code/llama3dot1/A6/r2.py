def quicksort(arr):
    """
    Sortiert ein Array von Zahlen in aufsteigender Reihenfolge.

    :param arr: Das Array zu sortieren
    :return: Das sortierte Array
    """
    _quicksort_helper(arr, 0, len(arr) - 1)
    return arr

def _quicksort_helper(arr, low, high):
    if low < high:
        pivot_index = _partition(arr, low, high)
        _quicksort_helper(arr, low, pivot_index - 1)
        _quicksort_helper(arr, pivot_index + 1, high)

def _partition(arr, low, high):
    """
    Teilte das Array in zwei Teile auf.

    :param arr: Das Array
    :param low: Der untere Index des Bereichs
    :param high: Der obere Index des Bereichs
    :return: Der Index des Pivot-Elements
    """
    pivot = arr[high]
    i = (low - 1)

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Beispiel-Verwendung
arr = [5, 2, 8, 3, 1, 6, 4]
print("Unsortiert:", arr)
quicksort(arr)
print("Sortiert:", arr)