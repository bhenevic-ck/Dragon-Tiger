import time
import tracemalloc

# Quick Sort implementation (in-place)
def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] >= pivot:  # Sort in descending order
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Function to run the game
def dragon_tiger_game():
    while True:
        try:
            # Get the number of players
            num_players = int(input("Enter the number of players (max 300): "))
            if num_players > 300 or num_players < 1:
                print("Invalid input. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Try again.")

    # Get bet amounts for each player
    players = []
    for i in range(num_players):
        while True:
            try:
                bet_amount = float(input(f"Enter the bet amount for player {i + 1}: "))
                players.append((i + 1, bet_amount))  # Store player number and bet amount
                break
            except ValueError:
                print("Invalid input. Please enter a valid bet amount.")

    # Extract only the bet amounts for sorting
    bet_amounts = [bet for _, bet in players]

    # Start memory tracking
    tracemalloc.start()

    # Sort bet amounts with Quick Sort and measure time in nanoseconds
    start_time = time.time_ns()
    quick_sort(bet_amounts, 0, len(bet_amounts) - 1)
    end_time = time.time_ns()

    # Stop memory tracking
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Arrange sorted players based on sorted bet amounts
    sorted_players = sorted(players, key=lambda x: x[1], reverse=True)
    print("\nSorted Players by Bet Amount:")
    for player, bet in sorted_players:
        print(f"Player {player} - Bet Amount: {bet}")

    # Display runtime in nanoseconds with decimal precision
    runtime = end_time - start_time
    print(f"\nQuick Sort Runtime: {runtime:.2f} nanoseconds")

    # Display memory usage in MiB
    print(f"Memory Usage: Current = {current / 1024 / 1024:.2f} MiB, Peak = {peak / 1024 / 1024:.2f} MiB")

# Run the game
dragon_tiger_game()
