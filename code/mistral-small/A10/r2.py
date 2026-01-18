def quick_sort(arr):
    """
    Sorts an array in place using the Quick Sort algorithm.
    :param arr: List of integers to be sorted.
    """
    def partition(low, high):
        # Choose the rightmost element as pivot
        pivot = arr[high]
        i = low - 1  # index of smaller element

        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1
                # Swap arr[i] and arr[j]
                arr[i], arr[j] = arr[j], arr[i]

        # Swap arr[i+1] and arr[high] (or pivot)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]

        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            # Partition the array and get the pivot index
            pi = partition(low, high)

            # Recursively sort elements before and after partition
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    # Call the recursive function with initial low and high indices
    quick_sort_recursive(0, len(arr) - 1)

# Example usage:
array = [10, 7, 8, 9, 1, 5]
quick_sort(array)
print("Sorted array:", array)