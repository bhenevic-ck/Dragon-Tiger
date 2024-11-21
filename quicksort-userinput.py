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

# Taking user input
try:
    # User inputs numbers separated by spaces
    user_input = input("Enter numbers separated by spaces: ")
    # Convert the input string into a list of integers
    numbers = list(map(int, user_input.split()))
    
    print("Original List:", numbers)
    sorted_numbers = quick_sort(numbers)  # Call the quick_sort function
    print("Sorted List:", sorted_numbers)
except ValueError:
    print("Please enter valid integers.")
