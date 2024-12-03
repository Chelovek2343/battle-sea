import random, os

def clear(): os.system("cls" if os.name == "nt" else "clear")

def print_board(board):
    print("  " + " ".join(map(str, range(1, len(board[0]) + 1))))
    print("\n".join(f"{chr(65 + i)} " + " ".join(row) for i, row in enumerate(board)))

def is_empty(hidden, r, c, size, o):
    return all(0 <= r + o[0] * i < len(hidden) and 0 <= c + o[1] * i < len(hidden[0]) 
               and all(hidden[r + o[0] * i + dr][c + o[1] * i + dc] == "." 
                       for dr in range(-1, 2) for dc in range(-1, 2) 
                       if 0 <= r + o[0] * i + dr < len(hidden) and 0 <= c + o[1] * i + dc < len(hidden[0]))
               for i in range(size))

def place_ships(hidden, ships):
    for size, count in ships:
        for _ in range(count):
            while True:
                o = random.choice([(0, 1), (1, 0)])
                r, c = random.randint(0, len(hidden) - 1), random.randint(0, len(hidden[0]) - 1)
                if is_empty(hidden, r, c, size, o):
                    for i in range(size): hidden[r + o[0] * i][c + o[1] * i] = "#"
                    break

def take_turn(board, hidden):
    while True:
        shot = input("Enter shot (e.g., B5): ").upper()
        if len(shot) >= 2 and shot[0].isalpha() and shot[1:].isdigit():
            r, c = ord(shot[0]) - 65, int(shot[1:]) - 1
            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == ".": break
        print("Invalid input, try again.")
    if hidden[r][c] == "#": 
        board[r][c], hidden[r][c] = "X", "!"
        print("Hit!" if any("#" in row for row in hidden) else "You sunk the last ship!")
    else: board[r][c] = "O"; print("Miss!")
    return all("#" not in row for row in hidden)

def play():
    size, ships = 7, [(3, 1), (2, 2), (1, 4)]
    board = [["."] * size for _ in range(size)]
    hidden = [["."] * size for _ in range(size)]
    input("Enter your name: ")
    place_ships(hidden, ships)
    shots = 0
    while True:
        clear(); print_board(board)
        shots += 1
        if take_turn(board, hidden): break
    clear(); print_board(board)
    print(f"Victory in {shots} shots!")

if name == "main":
    play()
