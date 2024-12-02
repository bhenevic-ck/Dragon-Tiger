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

def quick_sort(arr, key=lambda x: x):
    """Quick Sort implementation with a key function."""
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if key(x) <= key(pivot)]
    greater = [x for x in arr[1:] if key(x) > key(pivot)]
    return quick_sort(less, key) + [pivot] + quick_sort(greater, key)

# Function to set the number of players
def set_num_players():
    global current_player_id, players, balances, max_players
    try:
        num = int(num_players_entry.get())
        if num < 1 or num > 1000:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of players (1-1000)!")
        return

    players.clear()
    balances.clear()
    current_player_id = generate_player_id()  # Start with first player ID
    max_players = num
    switch_to_main_game(current_player_id)

# Function to generate a random Player ID
def generate_player_id():
    return f"Player-{random.randint(1000, 9999)}"

# Function to place randomized bets
def randomize_bets():
    global players, balances
    players.clear()
    sides = ["Dragon", "Tiger"]
    for _ in range(max_players):
        player_id = generate_player_id()
        bet_amount = random.randint(1, 1000)
        side = random.choice(sides)
        balances[player_id] = balances.get(player_id, 10000) - bet_amount
        players.append((player_id, bet_amount, side))
    result_label.config(text="Bets randomized successfully!", fg="green")
    update_bets_display()

# Function to start the game
def start_game():
    global players, game_history
    if not players:
        result_label.config(text="No bets placed yet!", fg="red")
        return

    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)

    dragon_card = deck.pop()
    tiger_card = deck.pop()

    dragon_label.config(text=f"Dragon Card: {dragon_card}")
    tiger_label.config(text=f"Tiger Card: {tiger_card}")

    card_ranking = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    dragon_value = card_ranking[dragon_card]
    tiger_value = card_ranking[tiger_card]

    winner = "Dragon" if dragon_value > tiger_value else "Tiger" if tiger_value > dragon_value else "Tie"

    for player in players:
        player_id, bet_amount, side = player
        if side == winner:
            balances[player_id] += bet_amount * 2

    game_history.extend(players)
    result_label.config(text=f"{winner} Wins!", fg="green")
    players.clear()
    update_bets_display()

# Function to update the bets display
def update_bets_display():
    bets_display.config(text="Bets: " + ", ".join([f"{p[0]} - ${p[1]} on {p[2]}" for p in players]))

def view_history():
    history_window = Toplevel(root)
    history_window.title("Game History")
    history_window.geometry("700x500")

    tree = Treeview(history_window, columns=("Player", "Bet Amount", "Side"), show="headings")
    tree.heading("Player", text="Player ID")
    tree.heading("Bet Amount", text="Bet Amount")
    tree.heading("Side", text="Side")
    tree.pack(fill=tk.BOTH, expand=True)

    def refresh_table(data):
        tree.delete(*tree.get_children())
        for record in data:
            tree.insert("", "end", values=record)

    def sort_history():
        start_time = time.perf_counter_ns()  # Start time in nanoseconds
        sorted_data = quick_sort(game_history, key=lambda x: x[1])  # Sort by Bet Amount
        end_time = time.perf_counter_ns()  # End time in nanoseconds
        runtime_ns = end_time - start_time
        space_usage = sys.getsizeof(sorted_data) / (1024 * 1024)  # Memory in MiB

        refresh_table(sorted_data)
        metrics_label.config(
            text=f"Runtime: {runtime_ns:,} nanoseconds | Space Used: {space_usage:.6f} MiB"
        )

    refresh_table(game_history)

    sort_button = tk.Button(history_window, text="Sort History", command=sort_history)
    sort_button.pack(pady=10)

    metrics_label = tk.Label(history_window, text="")
    metrics_label.pack()

    close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
    close_button.pack()


# Function to display the main game page
def switch_to_main_game(current_player_id):
    global result_label, dragon_label, tiger_label, bets_display

    clear_frame()

    tk.Label(root, text=f"Player ID: {current_player_id}", font=("Arial", 24)).pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 18), fg="black")
    result_label.pack(pady=10)

    dragon_label = tk.Label(root, text="Dragon Card: ", font=("Arial", 18), fg="black")
    dragon_label.pack(pady=10)

    tiger_label = tk.Label(root, text="Tiger Card: ", font=("Arial", 18), fg="black")
    tiger_label.pack(pady=10)

    bets_display = tk.Label(root, text="Bets: ", font=("Arial", 18), fg="black")
    bets_display.pack(pady=10)

    tk.Button(root, text="Randomize Bets", font=("Arial", 18), command=randomize_bets).pack(pady=10)
    tk.Button(root, text="Start Game", font=("Arial", 18), command=start_game).pack(pady=10)
    tk.Button(root, text="View History", font=("Arial", 18), command=view_history).pack(pady=10)

# Function to display the home page
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

# Function to clear the current frame
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Start the main page
root = tk.Tk()
root.title("Dragon Tiger Game")
root.geometry("1400x900")

home_page()

root.mainloop()
