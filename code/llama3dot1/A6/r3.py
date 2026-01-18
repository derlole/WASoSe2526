def quicksort(arr):
    """
    Sortiert ein Array von Zahlen nach dem QuickSort-Algorithmus.
    
    :param arr: Das zu sortierende Array
    :type arr: list
    :return: Das geordnete Array
    :rtype: list
    """
    _quicksort_helper(arr, 0, len(arr) - 1)


def _quicksort_helper(arr, low, high):
    """
    Hilfsfunktion für die QuickSort. Wählt ein Pivot-Element aus und tauscht alle Elemente kleiner als das Pivot mit denjenigen, 
    die größer sind.
    
    :param arr: Das zu sortierende Array
    :type arr: list
    :param low: Der unterste Index des zu sortierenden Bereichs
    :type low: int
    :param high: Der obere Index des zu sortierenden Bereichs
    :type high: int
    """
    if low < high:
        pivot_index = _partition(arr, low, high)
        _quicksort_helper(arr, low, pivot_index - 1)
        _quicksort_helper(arr, pivot_index + 1, high)


def _partition(arr, low, high):
    """
    Partitioniert das Array um das Pivot-Element richtig zu positionieren.
    
    :param arr: Das zu sortierende Array
    :type arr: list
    :param low: Der unterste Index des zu partitionierenden Bereichs
    :type low: int
    :param high: Der obere Index des zu partitionierenden Bereichs
    :type high: int
    :return: Der neue Index des Pivot-Elements
    :rtype: int
    """
    pivot = arr[high]
    i = (low - 1)

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Beispiel für die Verwendung der Funktion
arr_unsortiert = [5, 2, 8, 3, 1, 6, 4]
quicksort(arr_unsortiert)
print("Sortiertes Array:", arr_unsortiert)
