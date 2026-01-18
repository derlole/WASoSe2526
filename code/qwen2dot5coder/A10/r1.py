def quick_sort(arr):
    def partition(low, high):
        # Choose the rightmost element as pivot
        pivot = arr[high]
        i = low - 1  # Pointer for the smaller element

        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1
                # Swap arr[i] and arr[j]
                arr[i], arr[j] = arr[j], arr[i]

        # Swap the pivot element with the element at i+1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            # pi is partitioning index, arr[pi] is now at right place
            pi = partition(low, high)

            # Recursively sort elements before partition and after partition
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    # Initial call to the recursive quick_sort function
    quick_sort_recursive(0, len(arr) - 1)

# Example usage:
arr = [10, 7, 8, 9, 1, 5]
quick_sort(arr)
print("Sorted array is:", arr)