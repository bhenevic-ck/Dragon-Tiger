import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter.ttk import Treeview
import random
import time
import sys

# Global variables
players = []  # List to store players' bet data (ID, bet amount, side)
balances = {}  # Dictionary to store players' balance by ID
current_player_id = None  # The current player ID
max_players = 0  # Maximum number of players
game_history = []  # Store the history of past games
sorted_history = []  # To store the sorted history

def quick_sort(arr, key=lambda x: x):
    """Quick Sort implementation with a key function."""
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if key(x) <= key(pivot)]
    greater = [x for x in arr[1:] if key(x) > key(pivot)]
    return quick_sort(greater, key) + [pivot] + quick_sort(less, key)

# Function to set the number of players
def set_num_players():
    global current_player_id, players, balances, max_players  # Make sure current_player_id and players are global
    try:
        num = int(num_players_entry.get())
        if num < 1 or num > 1000:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of players (1-1000)!")
        return

    # Initialize the global variables
    players.clear()
    balances.clear()  # Initialize the balances dictionary
    current_player_id = generate_player_id()  # Start with first player ID
    max_players = num  # Set the number of maximum players

    switch_to_main_game(current_player_id)

# Function to generate a random Player ID
def generate_player_id():
    return f"Player-{random.randint(1000, 9999)}"

# Function to place a bet
def place_bet(side):
    global current_player_id, players, balances, max_players, bet_entry

    try:
        bet_amount = int(bet_entry.get())
        if bet_amount <= 0:
            raise ValueError
    except ValueError:
        result_label.config(text="Enter a valid bet amount!", fg="red")
        return

    # Deduct bet amount from player's balance
    if current_player_id not in balances:
        balances[current_player_id] = 10000  # Initialize new player balance with 10,000
    if balances[current_player_id] < bet_amount:
        result_label.config(text="Insufficient balance!", fg="red")
        return

    if len(players) >= max_players:
        result_label.config(text="Maximum players reached!", fg="red")
        return

    balances[current_player_id] -= bet_amount
    players.append((current_player_id, bet_amount, side))  # Add the bet to the list
    result_label.config(text=f"Bet placed on {side} by {current_player_id} (${bet_amount})", fg="green")

    # Move player ID and bet amount to the center
    center_label.config(text=f"{current_player_id} placed ${bet_amount} on {side}")
    update_balance_display()
    update_players_display()
    update_bets_display()

    # If all players have placed their bets, start the game
    if len(players) >= max_players:
        start_game_button.config(state=tk.NORMAL)  # Enable the start game button
    else:
        # Generate a new Player ID for next player
        current_player_id = generate_player_id()
        player_id_label.config(text=f"Current Player ID: {current_player_id}")

# Function to start the game
def start_game():
    global players, game_history
    if not players:
        result_label.config(text="No bets placed yet!", fg="red")
        return

    # Create and shuffle the deck
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)

    # Draw cards
    dragon_card = deck.pop()
    tiger_card = deck.pop()

    # Display drawn cards
    dragon_label.config(text=f"Dragon Card: {dragon_card}")
    tiger_label.config(text=f"Tiger Card: {tiger_card}")

    # Determine winner
    card_ranking = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    dragon_value = card_ranking[dragon_card]
    tiger_value = card_ranking[tiger_card]

    if dragon_value > tiger_value:
        winner = "Dragon"
    elif tiger_value > dragon_value:
        winner = "Tiger"
    else:
        winner = "Tie"

    # Process bets
    for player in players:
        player_id, bet_amount, side = player
        if side == winner:
            balances[player_id] += bet_amount * 2

    # Save game results and players' bets
    for player in players:
        player_id, bet_amount, side = player
        game_history.append((player_id, bet_amount, side))

    # Display winner result
    result_label.config(text=f"{winner} Wins!", fg="green")

    # Reset game for next round
    start_game_button.config(state=tk.DISABLED)
    players.clear()
    update_balance_display()
    update_players_display()
    update_bets_display()


    players.clear()  # Clear the players' list for the next round

# Function to update the balance display
def update_balance_display():
    balance = balances.get(current_player_id, 10000)  # Default balance is 10,000 if not found
    balances_display.config(text=f"Balance: ${balance}")

# Function to update the players display
def update_players_display():
    players_display.config(text="Players: " + ", ".join([p[0] for p in players]))

# Function to update the bets display
def update_bets_display():
    bets_display.config(text="Bets: " + ", ".join([f"${p[1]} on {p[2]}" for p in players]))

# Function to view history and show the table
def view_history():
    # Call function to show the history table
    show_history_table()

def show_history_table():
    # Create a new top-level window for the history table
    history_window = Toplevel(root)
    history_window.title("Game History")
    history_window.geometry("700x500")

    # Create a Treeview widget
    tree = Treeview(history_window, columns=("Player", "Bet Amount", "Side"), show="headings")
    tree.heading("Player", text="Player ID")
    tree.heading("Bet Amount", text="Bet Amount")
    tree.heading("Side", text="Side")
    tree.pack(fill=tk.BOTH, expand=True)

    # Function to refresh the table with new data
    def refresh_table(data):
        tree.delete(*tree.get_children())  # Clear the table
        for record in data:
            tree.insert("", "end", values=record)

    # Function to sort bets using Quick Sort
    def sort_bets():
        start_time = time.time()
        sorted_data = quick_sort(game_history, key=lambda x: x[1])  # Sort by Bet Amount
        runtime = time.time() - start_time
        space_usage = sys.getsizeof(sorted_data) / (1024 * 1024)  # Space in MiB

        # Update the table with sorted data
        refresh_table(sorted_data)

        # Display runtime and space usage
        metrics_label.config(
            text=f"Sorting Runtime: {runtime:.6f} seconds | Space Used: {space_usage:.6f} MiB"
        )

    # Display the initial unsorted data
    refresh_table(game_history)

    # Add Sort button
    sort_button = tk.Button(history_window, text="Sort Bets", command=sort_bets)
    sort_button.pack(pady=10)

    # Label to display runtime and space usage
    metrics_label = tk.Label(history_window, text="")
    metrics_label.pack(pady=5)

    # Add a close button
    close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
    close_button.pack(pady=10)

# Function to sort and display bets
def sort_bets():
    global sorted_bets_runtime
    sorted_bets, runtime = quick_sort_runtime(players) # type: ignore
    space_usage = calculate_space_usage(sorted_bets) # type: ignore

    sorted_text = "Sorted Bets (Descending):\n"
    for name, bet, side in sorted_bets:
        sorted_text += f"{name}: ${bet} on {side}\n"

    sorted_label.config(text=sorted_text, justify="left")
    runtime_label.config(text=f"Runtime: {runtime:.6f} seconds", fg="black")
    space_label.config(text=f"Memory Usage: {space_usage:.6f} MB", fg="black")

# Main page UI setup
def home_page():
    clear_frame()
    tk.Label(root, text="Dragon Tiger Game", font=("Arial", 50), fg="black").pack(pady=20)
    tk.Button(root, text="Start Game", font=("Arial", 24), bg="grey", fg="white", command=switch_to_set_players_page).pack(pady=10)
    tk.Button(root, text="Quit", font=("Arial", 24), bg="red", fg="white", command=root.quit).pack(pady=10)

# Function to set the number of players
def switch_to_set_players_page():
    clear_frame()
    tk.Label(root, text="Set Number of Players (1-1000)", font=("Arial", 24)).pack(pady=10)
    global num_players_entry
    num_players_entry = tk.Entry(root, font=("Arial", 18))
    num_players_entry.pack(pady=10)
    tk.Button(root, text="Submit", font=("Arial", 18), bg="grey", fg="white", command=set_num_players).pack(pady=10)

# Function to display the main game page
def switch_to_main_game(current_player_id):
    global result_label, center_label, balances_display, players_display, bets_display, sorted_label, runtime_label, space_label, sorted_bets_runtime, bet_entry, start_game_button, player_id_label, dragon_label, tiger_label

    # Initialize the main game page elements
    clear_frame()

    # Display main game components
    result_label = tk.Label(root, text="", font=("Arial", 18), fg="black")
    result_label.pack(pady=10)

    center_label = tk.Label(root, text="", font=("Arial", 24), fg="black")
    center_label.pack(pady=20)

    dragon_label = tk.Label(root, text="Dragon Card: ", font=("Arial", 18), fg="black")
    dragon_label.pack(pady=10)

    tiger_label = tk.Label(root, text="Tiger Card: ", font=("Arial", 18), fg="black")
    tiger_label.pack(pady=10)

    balances_display = tk.Label(root, text="Balance: $1,000,000", font=("Arial", 18), fg="black")
    balances_display.pack(pady=10)

    players_display = tk.Label(root, text="Players: ", font=("Arial", 18), fg="black")
    players_display.pack(pady=10)

    bets_display = tk.Label(root, text="Bets: ", font=("Arial", 18), fg="black")
    bets_display.pack(pady=10)

    sorted_label = tk.Label(root, text="", font=("Arial", 16), fg="black")
    sorted_label.pack(pady=10)

    runtime_label = tk.Label(root, text="", font=("Arial", 16), fg="black")
    runtime_label.pack(pady=10)

    space_label = tk.Label(root, text="", font=("Arial", 16), fg="black")
    space_label.pack(pady=10)

    bet_entry = tk.Entry(root, font=("Arial", 24))
    bet_entry.pack(pady=10)

    start_game_button = tk.Button(root, text="Start Game", font=("Arial", 24), command=start_game)
    player_id_label = tk.Label(root, text=f"Current Player ID: {current_player_id}", font=("Arial", 18), fg="black")
    start_game_button.pack(pady=10)

    tk.Button(root, text="Place Bet on Dragon", font=("Arial", 24), command=lambda: place_bet("Dragon")).pack(pady=10)
    tk.Button(root, text="Place Bet on Tiger", font=("Arial", 24), command=lambda: place_bet("Tiger")).pack(pady=10)

    # Moved the "View History" button to the main page
    tk.Button(root, text="View History", font=("Arial", 24), command=view_history).pack(pady=10)

# Function to clear the current frame (all widgets in the window)
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Start the main page
root = tk.Tk()
root.title("Dragon Tiger Game")
root.geometry("1400x900")

home_page()  # Start with the home page

root.mainloop()
