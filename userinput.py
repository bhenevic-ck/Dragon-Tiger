# Iterative version of Quick Sort
def iterative_quick_sort(arr):
    # Stack to hold sublists to be processed
    stack = [(0, len(arr) - 1)]  # We push the first and last indices of the array to the stack
    
    while stack:
        low, high = stack.pop()  # Pop the current low and high indices from the stack
        if low < high:
            # Partition the array and get the pivot index
            pivot_index = partition(arr, low, high)
            
            # Push the left side (low to pivot_index-1) and right side (pivot_index+1 to high) to the stack
            stack.append((low, pivot_index - 1))  # Left partition
            stack.append((pivot_index + 1, high))  # Right partition
    
    return arr

# Partition function
def partition(arr, low, high):
    pivot = arr[high]  # Pivot is the last element in the current sublist
    i = low - 1  # Pointer for the smaller element
    
    # Rearrange elements in the array
    for j in range(low, high):
        if arr[j] <= pivot:  # If current element is less than or equal to pivot
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap elements
    
    # Place the pivot element in the correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1  # Return the pivot index

# Predefined list of numbers
numbers = [8, 3, 1, 7, 0, 10, 2]

# Display original list
print("Original List:", numbers)

# Sorting the list using Iterative Quick Sort
sorted_numbers = iterative_quick_sort(numbers)

# Display sorted list
print("Sorted List:", sorted_numbers)
