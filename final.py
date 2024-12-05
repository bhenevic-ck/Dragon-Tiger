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
game_history = []  

def quick_sort(arr, key=lambda x: x):
    """Quick Sort implementation with a key function."""
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if key(x) <= key(pivot)]
    greater = [x for x in arr[1:] if key(x) > key(pivot)]
    return quick_sort(less, key) + [pivot] + quick_sort(greater, key)

def bingo_sort(arr, key=lambda x: x):
    sorted_arr = arr.copy()
    max_val = max(sorted_arr, key=key)
    max_list = [x for x in sorted_arr if key(x) == key(max_val)]

    i = len(sorted_arr) - 1
    while sorted_arr:
        max_val = max(sorted_arr, key=key)
        max_list = [x for x in sorted_arr if key(x) == key(max_val)]
        for val in max_list:
            sorted_arr.remove(val)
            arr[i] = val
            i -= 1
    return arr

def cycle_sort(arr, key=lambda x: x):
    sorted_arr = arr.copy()
    for cycle_start in range(len(sorted_arr) - 1):
        item = sorted_arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, len(sorted_arr)):
            if key(sorted_arr[i]) < key(item):
                pos += 1
        if pos == cycle_start:
            continue
        while key(item) == key(sorted_arr[pos]):
            pos += 1
        sorted_arr[pos], item = item, sorted_arr[pos]
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(sorted_arr)):
                if key(sorted_arr[i]) < key(item):
                    pos += 1
            while key(item) == key(sorted_arr[pos]):
                pos += 1
            sorted_arr[pos], item = item, sorted_arr[pos]
    return sorted_arr

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

    # Create and shuffle the deck
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)

    def display_final_cards():
        """Displays the final cards and determines the winner."""
        dragon_card = deck.pop()
        tiger_card = deck.pop()

        # Update labels with final cards
        dragon_label.config(text=f"Dragon Card: {dragon_card}")
        tiger_label.config(text=f"Tiger Card: {tiger_card}")

        # Determine winner
        card_ranking = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 0, 'J': 0, 'Q': 0, 'K': 0, 'A': 1}
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

        players.clear()
        update_bets_display()

    def shuffle_animation(iterations=10):
        """Displays a shuffling animation by updating cards with random values."""
        if iterations > 0:
            random_dragon = random.choice(deck)
            random_tiger = random.choice(deck)
            dragon_label.config(text=f"Dragon Card: {random_dragon}")
            tiger_label.config(text=f"Tiger Card: {random_tiger}")

        
            root.after(100, shuffle_animation, iterations - 1)
        else:
           
            display_final_cards()

    # Start shuffling animation
    shuffle_animation()

# Function to update the bets display
def update_bets_display():
    bets_display.config(text="Bets: " + ", ".join([f"{p[0]} - ${p[1]} on {p[2]}" for p in players]))

def view_history():
    history_window = Toplevel(root)
    history_window.title("Game History")
    history_window.geometry("700x400")  

    tree = Treeview(history_window, columns=("Player", "Bet Amount", "Side"), show="headings")
    tree.heading("Player", text="Player ID")
    tree.heading("Bet Amount", text="Bet Amount")
    tree.heading("Side", text="Side")
    tree.place(x=20, y=20, width=660, height=300) 

    # Function to refresh the table with original data
    def refresh_table(data):
        tree.delete(*tree.get_children())  
        for record in data:
            tree.insert("", "end", values=record)

    # Function to reset the table to its original state
    def reset_table():
        refresh_table(game_history)  
        algorithm_var.set("Select Sorting Algorithm") 
        metrics_label.config(text="")  

    # Function to sort bets based on selected algorithm
    def sort_history():
        selected_algorithm = algorithm_var.get()
        if selected_algorithm == "Quick Sort":
            start_time = time.perf_counter()
            sorted_data = quick_sort(game_history, key=lambda x: x[1])
            end_time = time.perf_counter()
        elif selected_algorithm == "Bingo Sort":
            start_time = time.perf_counter()
            sorted_data = bingo_sort(game_history, key=lambda x: x[1])
            end_time = time.perf_counter()
        elif selected_algorithm == "Cycle Sort":
            start_time = time.perf_counter()
            sorted_data = cycle_sort(game_history, key=lambda x: x[1])
            end_time = time.perf_counter()
        else:
            messagebox.showerror("Error", "Please select a valid sorting algorithm!")
            return

        runtime_sec = end_time - start_time  # runtime to seconds
        space_usage = sys.getsizeof(sorted_data)  # Space in bytes

        refresh_table(sorted_data)

        metrics_label.config(
            text=f"Runtime: {runtime_sec:.6f} seconds | Space Used: {space_usage:,} bytes"
        )

    # Display the initial unsorted data
    refresh_table(game_history)

    # Dropdown menu for selecting sorting algorithm
    algorithm_var = tk.StringVar()
    algorithm_var.set("Select Sorting Algorithm") 
    algorithm_menu = tk.OptionMenu(history_window, algorithm_var, "Quick Sort", "Bingo Sort", "Cycle Sort")
    algorithm_menu.place(x=20, y=340)  

    # Add Sort button
    sort_button = tk.Button(history_window, text="Sort History", command=sort_history)
    sort_button.place(x=350, y=340, width=100, height=30)  

    # Add Refresh button
    refresh_button = tk.Button(history_window, text="Refresh", command=reset_table)
    refresh_button.place(x=450, y=340, width=100, height=30)  

    # Label to display runtime and space usage
    metrics_label = tk.Label(history_window, text="")
    metrics_label.place(x=20, y=375) 

    # Add a close button
    close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
    close_button.place(x=550, y=340, width=100, height=30)  
  
def set_num_players():
    global current_player_id, players, balances, max_players  
    try:
        num = int(num_players_entry.get())
        if num < 1:  
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number of players!")
        return

    # Initialize the global variables
    players.clear()
    balances.clear()  
    current_player_id = generate_player_id()  
    max_players = num  

    switch_to_main_game(current_player_id)
# Global variable for Bets Display position
bets_display_x = 400  

# Function to move the Bets Display label
def move_bets_display():
    global bets_display_x

    # Move the label to the left by decreasing x-position
    bets_display_x -= 2  
    if bets_display_x < -1200:  
        bets_display_x = root.winfo_width()

    bets_display.place(x=bets_display_x, y=20, width=4989, height=50)

    root.after(50, move_bets_display)
    
# Function to display the main game page
def switch_to_main_game(current_player_id):
    global result_label, dragon_label, tiger_label, bets_display

    clear_frame()

    # Result Label
    result_label = tk.Label(root, text="", font=("Arial", 19), fg="black")
    result_label.place(x=260, y=200, width=600, height=30)  

    # Dragon Label
    dragon_label = tk.Label(root, text="Dragon : ", font=("Arial", 24), fg="red")
    dragon_label.place(x=235, y=140, width=300, height=35)

    # TigerLabel
    tiger_label = tk.Label(root, text="Tiger : ", font=("Arial", 24), fg="orange")
    tiger_label.place(x=495, y=140, width=500, height=35)

    # Bets Display Label(Moving Text)
    bets_display = tk.Label(root, text="Bets: ", font=("Arial", 18), fg="black")
    bets_display.place(x=400, y=30, width=300, height=30)

    # Buttons with adjustable positions and dimensions
    tk.Button(root, text="Randomize Bets", font=("Arial", 16), command=randomize_bets).place(x=460, y=240, width=200, height=40)
    tk.Button(root, text="Start Game", font=("Arial", 16), command=start_game).place(x=460, y=290, width=200, height=40)
    tk.Button(root, text="View History", font=("Arial", 16), command=view_history).place(x=460, y=360, width=200, height=40)
    tk.Button(root, text="Set Numbers of Players", font=("Arial", 12), command=switch_to_set_players_page).place(x=260, y=360, width=200, height=40)
    tk.Button(root, text="Quit", font=("Arial", 12), command=root.quit).place(x=660, y=360, width=200, height=40)
    move_bets_display()

# Function to display the home page
def home_page():
    clear_frame()
    tk.Label(root, text="Dragon Tiger Game", font=("Arial", 45), fg="black").place(x=165, y=165, width=800, height=70)
    tk.Button(root, text="Start Game", font=("Arial", 24), bg="grey", fg="white", command=switch_to_set_players_page).place(x=385, y=290, width=350, height=40)
    tk.Button(root, text="Quit", font=("Arial", 24), bg="red", fg="white", command=root.quit).place(x=385, y=340, width=350, height=40)

# Function to set the number of players
def switch_to_set_players_page():
    clear_frame()
    tk.Label(root, text="Set Number of Players ", font=("Arial", 24)).place(x=165, y=165, width=800, height=70)
    global num_players_entry
    num_players_entry = tk.Entry(root, font=("Arial", 18))
    num_players_entry.place(x=460, y=250, width=200, height=40)
    tk.Button(root, text="Submit", font=("Arial", 18), bg="grey", fg="white", command=set_num_players).place(x=510, y=300, width=100, height=40)
    
# Function to clear the current frame
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Start the main page
root = tk.Tk()
root.title("Dragon Tiger Game")
root.geometry("1100x600")

home_page()

root.mainloop()
