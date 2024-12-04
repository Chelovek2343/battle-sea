import random, os

def clear(): os.system("cls")

# Function to display the game board
def print_board(board):
    print("  " + " ".join(map(str, range(1, len(board[0]) + 1))))  # Print column numbers
    for i, row in enumerate(board):  # Print each row with row labels (A, B, C...)
        print(f"{chr(65 + i)} " + " ".join(row))

# Function to check if a ship can be placed at a certain location
def is_empty(hidden, row, col, size, direction):
    for i in range(size):
        new_row = row + direction[0] * i
        new_col = col + direction[1] * i
        if not (0 <= new_row < len(hidden) and 0 <= new_col < len(hidden[0])) or hidden[new_row][new_col] != ".":
            return False
    return True

# Function to place ships on the hidden board
def ships_location(hidden, ships):
    for size, count in ships:
        for _ in range(count):  # Place each ship
            while True:
                direction = random.choice([(0, 1), (1, 0)])  # Horizontal or vertical
                row = random.randint(0, len(hidden) - 1)
                col = random.randint(0, len(hidden[0]) - 1)
                if is_empty(hidden, row, col, size, direction):
                    for i in range(size):  # Place the ship
                        hidden[row + direction[0] * i][col + direction[1] * i] = "#"
                    break

# Function to take a turn (player's shot)
def take_turn(board, hidden):
    while True:
        shot = input("Enter your shot (e.g., B5): ").upper()
        if len(shot) >= 2 and shot[0].isalpha() and shot[1:].isdigit():
            row = ord(shot[0]) - 65  # Convert letter to row index
            col = int(shot[1:]) - 1  # Convert number to column index
            if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == ".":
                break
        print("Invalid input. Try again.")

    if hidden[row][col] == "#":  # Check if the shot is a hit or miss
        board[row][col] = "X"
        hidden[row][col] = "!"  # Mark as hit on hidden board
        print("Hit!")
        return not any("#" in row for row in hidden)  # Check if all ships are sunk
    else:
        board[row][col] = "O"
        print("Miss!")
        return False

# Main function to play the game
def play_game(name):
    size = 7  # Board size (7x7 grid)
    ships = [(3, 1), (2, 2), (1, 4)]  # List of ships (size, count)
    board = [["."] * size for _ in range(size)]  # Player's board
    hidden = [["."] * size for _ in range(size)]  # Hidden board with ships

    ships_location(hidden, ships)

    shots = 0  # Count the number of shots taken
    while True:
        clear()
        print_board(board)
        shots += 1
        if take_turn(board, hidden):  # Player's turn
            break

    clear()
    print_board(board)
    print(f"Congratulations! You won in {shots} shots!")
    return shots

def end():
    leaderboard = []

    while True:
        clear()
        player_name = input("Enter your name: ")
        shots_taken = play_game(player_name)
        leaderboard.append((player_name, shots_taken))

        if input("Do you want to play again? (yes/no): ").strip().lower() == "no":
            print("\nLeaderboard:")
            for rank, (name, shots) in enumerate(sorted(leaderboard, key=lambda x: x[1]), start=1):
                print(f"{rank}. {name} - {shots} shots")
            break

end()
