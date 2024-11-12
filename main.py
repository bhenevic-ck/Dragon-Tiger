import sqlite3
import random

# Connect to SQLite Database
conn = sqlite3.connect('dragon_tiger_game.db')
cursor = conn.cursor()

# Database Setup
def setup_database():
    cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      wins INTEGER DEFAULT 0,
                      losses INTEGER DEFAULT 0,
                      balance INTEGER DEFAULT 10000)''')  # Players start with 10,000 balance
    cursor.execute('''CREATE TABLE IF NOT EXISTS game_results (
                      game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      player_id INTEGER,
                      result TEXT,
                      bet_side TEXT,
                      bet_amount INTEGER,
                      payout INTEGER,
                      FOREIGN KEY(player_id) REFERENCES players(id))''')
    conn.commit()

# Sorting Algorithms

# Quick Sort
def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high][1]
    i = low - 1
    for j in range(low, high):
        if arr[j][1] >= pivot:  # Descending order
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Cycle Sort
def cycle_sort(arr):
    for cycle_start in range(0, len(arr) - 1):
        item = arr[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, len(arr)):
            if arr[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(arr)):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
    return arr

# Bingo Sort (Bucket Sort approach)
def bingo_sort(arr):
    min_val = min(arr)
    max_val = max(arr)
    range_of_elements = max_val - min_val + 1
    count = [0] * range_of_elements

    for num in arr:
        count[num - min_val] += 1

    idx = 0
    for i in range(range_of_elements):
        while count[i] > 0:
            arr[idx] = i + min_val
            idx += 1
            count[i] -= 1
    return arr

# Draw a random card (1 to 13, representing Ace to King)
def draw_card():
    return random.randint(1, 13)

# Function to play the Dragon Tiger game
def play_game(player_id):
    # Ask player for their bet
    bet_side = input("Place your bet (Dragon/Tiger/Tie): ").lower()
    if bet_side not in ['dragon', 'tiger', 'tie']:
        print("Invalid bet. Please choose 'Dragon', 'Tiger', or 'Tie'.")
        return

    bet_amount = int(input("Enter your bet amount: "))
    
    # Get player balance
    cursor.execute("SELECT balance FROM players WHERE id = ?", (player_id,))
    balance = cursor.fetchone()[0]

    # Check if player has enough balance
    if bet_amount > balance:
        print("You do not have enough balance to place this bet.")
        return

    # Draw cards for Dragon and Tiger
    dragon_card = draw_card()
    tiger_card = draw_card()
    
    print(f"Dragon's card: {dragon_card}, Tiger's card: {tiger_card}")

    # Determine the result
    if dragon_card > tiger_card:
        result = "dragon"
    elif tiger_card > dragon_card:
        result = "tiger"
    else:
        result = "tie"

    print(f"The result is: {result.capitalize()}!")

    # Calculate payout based on the player's bet
    payout = 0
    if bet_side == result:
        if result == "tie":
            payout = bet_amount * 10  # If Tie, 10x payout
        else:
            payout = bet_amount * 10  # If Dragon or Tiger, 10x payout
    elif bet_side == "tie" and result != "tie":
        payout = bet_amount // 2  # If Dragon or Tiger and result is Tie, you lose half the bet
    elif bet_side != result and bet_side != "tie":
        payout = -bet_amount  # If you lost, deduct your bet

    # Update player's balance
    new_balance = balance + payout
    cursor.execute("UPDATE players SET balance = ? WHERE id = ?", (new_balance, player_id))
    conn.commit()

    # Record the game result in the database
    cursor.execute("INSERT INTO game_results (player_id, result, bet_side, bet_amount, payout) VALUES (?, ?, ?, ?, ?)", 
                   (player_id, result, bet_side, bet_amount, payout))
    conn.commit()

    print(f"Your payout: {payout}. Your new balance: {new_balance}")

# Display Top Players using Quick Sort
def display_top_players():
    cursor.execute("SELECT id, (wins * 100.0) / (wins + losses) as win_rate FROM players WHERE (wins + losses) > 0")
    players = cursor.fetchall()
    quick_sort(players, 0, len(players) - 1)
    print("Top Players by Win Rate:")
    for player in players:
        print(f"Player ID: {player[0]}, Win Rate: {player[1]:.2f}%")

# Register or Get Player
def register_player(name):
    cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Player {name} registered successfully.")

def get_player_id(name):
    cursor.execute("SELECT id FROM players WHERE name=?", (name,))
    player = cursor.fetchone()
    if player:
        return player[0]
    else:
        register_player(name)
        return cursor.lastrowid

# Main Game Loop
def main():
    setup_database()
    print("Welcome to Dragon Tiger Game!")
    player_name = input("Enter player name: ")
    player_id = get_player_id(player_name)

    while True:
        action = input("Enter 'play' to play, 'top' to see top players, 'quit' to exit: ").lower()
        if action == 'play':
            play_game(player_id)
        elif action == 'top':
            display_top_players()
        elif action == 'quit':
            break
        else:
            print("Invalid input, please try again.")

    print("Thank you for playing!")
    conn.close()

if __name__ == "__main__":
    main()
