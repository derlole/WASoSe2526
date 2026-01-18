def quicksort(arr, low, high):
    if low < high:
        # Partition index
        pi = partition(arr, low, high)

        # Recursively sort elements before partition and after partition
        quicksort(arr, low, pi-1)
        quicksort(arr, pi+1, high)

def partition(arr, low, high):
    pivot = arr[high]  # Pivot
    i = (low - 1)      # Index of smaller element

    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1
            # Swap arr[i] and arr[j]
            arr[i], arr[j] = arr[j], arr[i]

    # Swap arr[i+1] and arr[high] (or pivot)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1

# Test the function
arr = [10, 7, 8, 9, 1, 5]
n = len(arr)
quicksort(arr, 0, n-1)
print("Sorted array is:", arr)