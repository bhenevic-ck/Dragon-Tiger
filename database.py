import sqlite3

# Connect to SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect('dragon_tiger_game.db')
cursor = conn.cursor()

# Create the players table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        balance INTEGER DEFAULT 10000)  # Players start with 10,000 balance
''')

# Create the game_results table to store game history
cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_results (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        result TEXT,
        bet_side TEXT,
        bet_amount INTEGER,
        payout INTEGER,
        FOREIGN KEY(player_id) REFERENCES players(id))
''')

# Commit changes and close the connection
conn.commit()

print("Database and tables created successfully!")

# Close the connection
conn.close()
