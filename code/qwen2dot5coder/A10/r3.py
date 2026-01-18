def quicksort(arr):
    """
    Sorts an array of numbers using the Quick-Sort algorithm.
    :param arr: The array to be sorted.
    :return: The sorted array.
    """
    # Helper function to partition the array around a pivot element
    def partition(low, high):
        """
        Partitions the array around a pivot element and returns the index of the pivot element after partitioning.
        :param low: The lower bound of the subarray to be partitioned.
        :param high: The upper bound of the subarray to be partitioned.
        :return: The index of the pivot element after partitioning.
        """
        # Select the pivot element as the last element in the subarray
        pivot = arr[high]
        
        # Initialize the left pointer to the first element in the subarray
        i = low - 1
        
        # Traverse the subarray from low to high-1
        for j in range(low, high):
            # If the current element is less than or equal to the pivot element,
            # swap it with the element at the left pointer and increment the left pointer
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        # Swap the pivot element with the element at the left pointer + 1
        arr[i+1], arr[high] = arr[high], arr[i+1]
        
        # Return the index of the pivot element after partitioning
        return i+1
    
    # Helper function to perform quicksort on a subarray
    def quicksort_recursive(low, high):
        """
        Sorts a subarray using the Quick-Sort algorithm.
        :param low: The lower bound of the subarray to be sorted.
        :param high: The upper bound of the subarray to be sorted.
        """
        # Base case: if the subarray has 0 or 1 elements, it is already sorted
        if low < high:
            # Partition the subarray around a pivot element and get the index of the pivot element after partitioning
            pi = partition(low, high)
            
            # Recursively sort the subarray to the left of the pivot element
            quicksort_recursive(low, pi-1)
            
            # Recursively sort the subarray to the right of the pivot element
            quicksort_recursive(pi+1, high)
    
    # Call the recursive quicksort function on the entire array
    quicksort_recursive(0, len(arr)-1)
    
    # Return the sorted array
    return arr