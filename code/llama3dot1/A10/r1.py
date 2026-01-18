def quick_sort(arr):
    """
    Sortiert ein Array von Zahlen mit dem Quick-Sort-Algorithmus.

    Args:
        arr (list): Das zu sortierende Array.

    Returns:
        list: Das sortierte Array.
    """

    # Wenn das Array kleiner als 2 ist, ist es bereits sortiert
    if len(arr) <= 1:
        return arr

    # Wähle einen Pivot-Element aus dem Array
    pivot = arr[0]

    # Teile das Array in drei Teile auf: untere Partition, Pivot und obere Partition
    lower_partition = [x for x in arr[1:] if x <= pivot]
    middle_partition = [pivot] * (len(arr) - len(lower_partition) - 1)
    upper_partition = [x for x in arr[1:] if x > pivot]

    # Rekursive Sortierung der Partitionen
    lower_sorted = quick_sort(lower_partition)
    upper_sorted = quick_sort(upper_partition)

    return lower_sorted + middle_partition + upper_sorted

# Beispielverwendung:
arr_unsortiert = [5, 2, 8, 3, 1, 4]
arr_sortiert = quick_sort(arr_unsortiert)
print(arr_sortiert)  # Ausgabe: [1, 2, 3, 4, 5, 8]