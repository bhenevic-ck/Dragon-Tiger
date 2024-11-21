# Function for Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:  # Base case: An array with 1 or no elements is already sorted
        return arr
    else:
        # Choose a pivot (in this case, the last element)
        pivot = arr[-1]
        # Partitioning step
        left = [x for x in arr[:-1] if x <= pivot]  # Elements less than or equal to pivot
        right = [x for x in arr[:-1] if x > pivot]  # Elements greater than pivot
        
        # Recursively sort the left and right partitions
        return quick_sort(left) + [pivot] + quick_sort(right)

# Predefined list of numbers
numbers = [8, 3, 1, 7, 0, 10, 2]

# Display original list
print("Original List:", numbers)

# Sorting the list using Quick Sort
sorted_numbers = quick_sort(numbers)

# Display sorted list
print("Sorted List:", sorted_numbers)
