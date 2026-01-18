def quicksort(arr):
    # Helper function to partition the array
    def partition(low, high):
        pivot = arr[high]  # Choosing the rightmost element as pivot
        i = low - 1  # Index of smaller element

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i + 1

    # Helper function for the quicksort algorithm
    def _quicksort(arr, low, high):
        if low < high:
            pi = partition(low, high)
            _quicksort(arr, low, pi - 1)
            _quicksort(arr, pi + 1, high)

    _quicksort(arr, 0, len(arr) - 1)
    return arr

# Example usage:
numbers = [34, 7, 23, 32, 5, 62]
sorted_numbers = quicksort(numbers)
print("Sorted array:", sorted_numbers)