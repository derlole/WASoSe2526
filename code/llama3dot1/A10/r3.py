def quick_sort(arr):
    """
    Sortiert ein Array von Zahlen mit dem Quick-Sort-Algorithmus.

    :param arr: Das Array, das sortiert werden soll.
    :type arr: list[int]
    :return: Das sortierte Array.
    :rtype: list[int]
    """
    if len(arr) <= 1:
        # Wenn das Array kleiner als 2 Elemente hat, ist es bereits sortiert
        return arr

    pivot = partition(arr)
    left = [x for x in arr if x < pivot]
    middle = [pivot] * (arr.count(pivot))
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def partition(arr):
    """
    Partitions das Array um den Median als Pivot zu finden.

    :param arr: Das Array, das geteilt werden soll.
    :type arr: list[int]
    :return: Der Median des Arrays.
    :rtype: int
    """
    n = len(arr)
    pivot = arr[n // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Wenn der Median nicht im Mittelfeld ist, muss das Array neu geteilt werden
    while len(left) != n // 2 or len(right) != n - (n // 2):
        left.append(arr.pop())
        right.insert(0, arr.pop())

    return partition(left + middle + right)


# Beispieldaten
arr = [5, 2, 8, 3, 1, 6, 4]
print("Unsortiert:", arr)
print("Sortiert:", quick_sort(arr))