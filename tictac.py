import tkinter
import random
import winsound

# Define colors
color_blue = "#4584b6"
color_yellow = "#ffde57"
color_gray = "#343434"
color_light_gray = "#646464"

# Game state variables
playerX = "X"
playerO = "O"
curr_player = playerX
turns = 0
game_over = False
ai_mode = False

# Initialize tkinter window
window = tkinter.Tk()
window.title("Tic Tac Toe")
window.resizable(False, False)

# Define frames for different pages
home_frame = tkinter.Frame(window)
game_frame = tkinter.Frame(window)
credits_frame = tkinter.Frame(window)

# Initialize board
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

def play_sound(sound_file):
    try:
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(f"Error playing sound: {e}")

def switch_to_game(ai=False):
    global ai_mode, curr_player, turns, game_over
    ai_mode = ai
    curr_player = playerX
    turns = 0
    game_over = False

    for row in range(3):
        for column in range(3):
            board[row][column].config(text="", foreground=color_blue, background=color_gray)

    label.config(text=curr_player + "'s turn", foreground="white")
    home_frame.pack_forget()
    credits_frame.pack_forget()
    game_frame.pack()

def switch_to_home():
    global ai_mode, curr_player, turns, game_over
    ai_mode = False
    curr_player = playerX
    turns = 0
    game_over = False

    game_frame.pack_forget()
    credits_frame.pack_forget()
    home_frame.pack()

def switch_to_credits():
    game_frame.pack_forget()
    home_frame.pack_forget()
    credits_frame.pack()

def set_tile(row, column):
    global curr_player, game_over, turns

    if game_over or board[row][column]["text"] != "":
        return

    play_sound("click.wav")

    board[row][column]["text"] = curr_player

    if curr_player == playerO:
        curr_player = playerX
    else:
        curr_player = playerO

    label["text"] = curr_player + "'s turn"
    check_winner()

    if ai_mode and not game_over and curr_player == playerO:
        ai_move()

def ai_move():
    global curr_player

    empty_tiles = [(row, col) for row in range(3) for col in range(3) if board[row][col]["text"] == ""]

    if empty_tiles:
        row, column = random.choice(empty_tiles)
        set_tile(row, column)

def check_winner():
    global turns, game_over
    turns += 1

    # Check horizontally
    for row in range(3):
        if (board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"]
                and board[row][0]["text"] != ""):
            declare_winner(row=row)
            return

    # Check vertically
    for column in range(3):
        if (board[0][column]["text"] == board[1][column]["text"] == board[2][column]["text"]
                and board[0][column]["text"] != ""):
            declare_winner(column=column)
            return

    # Check diagonally
    if (board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"]
            and board[0][0]["text"] != ""):
        declare_winner(diagonal="main")
        return

    if (board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"]
            and board[0][2]["text"] != ""):
        declare_winner(diagonal="anti")
        return

    # Check tie
    if turns == 9:
        label.config(text="Tie!", foreground=color_yellow)
        game_over = True

def declare_winner(row=None, column=None, diagonal=None):
    global game_over
    game_over = True

    play_sound("win.wav")

    if diagonal == "main":
        for i in range(3):
            board[i][i].config(foreground=color_yellow, background=color_light_gray)
    elif diagonal == "anti":
        for i in range(3):
            board[i][2 - i].config(foreground=color_yellow, background=color_light_gray)
    elif row is not None:
        for col in range(3):
            board[row][col].config(foreground=color_yellow, background=color_light_gray)
    elif column is not None:
        for row in range(3):
            board[row][column].config(foreground=color_yellow, background=color_light_gray)

    label.config(text=board[row][0]["text"] + " is the winner!", foreground=color_yellow)

def new_game():
    switch_to_game(ai_mode)

# Create home interface
tkinter.Label(home_frame, text="Tic Tac Toe", font=("Consolas", 30, "bold"), fg="white", bg=color_gray).pack(pady=20)

play_1p_button = tkinter.Button(home_frame, text="1 Player", font=("Consolas", 20), bg=color_gray, fg="white",
                                command=lambda: switch_to_game(ai=True))
play_1p_button.pack(pady=10)

play_2p_button = tkinter.Button(home_frame, text="2 Players", font=("Consolas", 20), bg=color_gray, fg="white",
                                command=lambda: switch_to_game(ai=False))
play_2p_button.pack(pady=10)

credits_button = tkinter.Button(home_frame, text="Credits", font=("Consolas", 20), bg=color_gray, fg="white",
                                 command=switch_to_credits)
credits_button.pack(pady=10)

quit_button = tkinter.Button(home_frame, text="Quit", font=("Consolas", 20), bg=color_gray, fg="white",
                              command=window.destroy)
quit_button.pack(pady=10)

# Create credits interface
tkinter.Label(credits_frame, text="Credits", font=("Consolas", 30, "bold"), fg="white", bg=color_gray).pack(pady=20)

credits_text = tkinter.Label(credits_frame, text="Shemsu Siraj\nBeimnet Guta", font=("Consolas", 20), fg="white",
                              bg=color_gray, justify="center")
credits_text.pack(pady=10)

back_button = tkinter.Button(credits_frame, text="Back", font=("Consolas", 20), bg=color_gray, fg="white",
                              command=switch_to_home)
back_button.pack(pady=10)

# Create game interface
label = tkinter.Label(game_frame, text="", font=("Consolas", 20), bg=color_gray, fg="white")
label.grid(row=0, column=0, columnspan=3, sticky="we")

for row in range(3):
    for column in range(3):
        board[row][column] = tkinter.Button(game_frame, text="", font=("Consolas", 50, "bold"),
                                            bg=color_gray, fg=color_blue, width=4, height=1,
                                            command=lambda row=row, column=column: set_tile(row, column))
        board[row][column].grid(row=row + 1, column=column)

restart_button = tkinter.Button(game_frame, text="Restart", font=("Consolas", 20), bg=color_gray, fg="white",
                                 command=new_game)
restart_button.grid(row=4, column=0, columnspan=2, sticky="we")

home_button = tkinter.Button(game_frame, text="Home", font=("Consolas", 20), bg=color_gray, fg="white",
                              command=switch_to_home)
home_button.grid(row=4, column=2, sticky="we")

# Show home frame
home_frame.pack()

# Start tkinter main loop
window.mainloop()
