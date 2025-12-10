import tkinter as tk
import random
from tkinter import messagebox

# ------------------------------
# Generate a random 9x9 Sudoku
# ------------------------------
def generate_sudoku():
    import random

    # Base 9x9 Sudoku
    base = [
        [1,2,3,4,5,6,7,8,9],
        [4,5,6,7,8,9,1,2,3],
        [7,8,9,1,2,3,4,5,6],
        [2,3,1,5,6,4,8,9,7],
        [5,6,4,8,9,7,2,3,1],
        [8,9,7,2,3,1,5,6,4],
        [3,1,2,6,4,5,9,7,8],
        [6,4,5,9,7,8,3,1,2],
        [9,7,8,3,1,2,6,4,5]
    ]

    # rows 
    for _ in range(10):
        block = random.choice([0,3,6])
        r1, r2 = block + random.randint(0,2), block + random.randint(0,2)
        while r1 == r2:
            r2 = block + random.randint(0,2)
        base[r1], base[r2] = base[r2], base[r1]


    # cols
    for _ in range(10):
        block = random.choice([0,3,6])
        c1, c2 = block + random.randint(0,2), block + random.randint(0,2)
        while c1 == c2:
            c2 = block + random.randint(0,2)
        for r in range(9):
            base[r][c1], base[r][c2] = base[r][c2], base[r][c1]


    board = [row[:] for row in base]

    count = 0
    while count < 40:
        i, j = random.randint(0,8), random.randint(0,8)
        if board[i][j] != 0:
            board[i][j] = 0
            count += 1

    return board


# -----------------------------------------
# Check if Sudoku is valid before updating
# ----------------------------------------
def check_sudoku():
    # 0. Check if the board is filled
    for i in range(9):
        for j in range(9):
            if entries[i][j].get().strip() == "":
                messagebox.showinfo("Result", "The Sudoku is not complete yet.")
                return

    # 1. Check values
    temp_board = [[0]*9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            val_str = entries[i][j].get()
            try:
                val = int(val_str)
                if 1 <= val <= 9:
                    temp_board[i][j] = val
                else:
                    messagebox.showwarning("Invalid", f"Number at row {i+1}, column {j+1} must be 1-9.")
                    return
            except:
                messagebox.showwarning("Invalid", f"Number at row {i+1}, column {j+1} must be 1-9.")
                return

    # 2. Check rows
    for i in range(9):
        row = temp_board[i]
        if len(row) != len(set(row)):
            messagebox.showinfo("Result", f"Error in row {i+1}. Duplicate numbers found.")
            return

    # 3. Check cols
    for col in range(9):
        col_vals = [temp_board[row][col] for row in range(9)]
        if len(col_vals) != len(set(col_vals)):
            messagebox.showinfo("Result", f"Error in column {col+1}. Duplicate numbers found.")
            return

    # 4. Check 3x3 blocks
    for r in [0,3,6]:
        for c in [0,3,6]:
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(temp_board[r+i][c+j])
            if len(block) != len(set(block)):
                messagebox.showinfo("Result", f"Error in 3x3 block starting at row {r+1}, column {c+1}.")
                return

    global board
    board = temp_board
    messagebox.showinfo("Result", "Sudoku is correct! Well done!")


# ------------------------------
# Tkinter setup
# ------------------------------
root = tk.Tk()
root.title("Random 9x9 Sudoku")

board = generate_sudoku()
entries = []

BLOCK_THICKNESS = 3
NORMAL_THICKNESS = 1
BORDER_COLOR = 'black'


# Create 9x9 grid
for i in range(9):
    row_entries = []
    for j in range(9):
        if j % 3 == 2 and j != 8:
            highlight_thickness_right = BLOCK_THICKNESS
        else:
            highlight_thickness_right = NORMAL_THICKNESS

        if i % 3 == 2 and i != 8:
            highlight_thickness_bottom = BLOCK_THICKNESS
        else:
            highlight_thickness_bottom = NORMAL_THICKNESS
            
        e = tk.Entry(
            root, 
            width=3, 
            justify='center', 
            font=('Arial',18), 
            fg='blue', 
            bg='#f0f0f0',
            bd=NORMAL_THICKNESS,
            relief='solid', 
            highlightthickness=NORMAL_THICKNESS, 
            highlightbackground='gray'
        )
        
        padx_val = (2, highlight_thickness_right + 1) if j % 3 == 2 and j != 8 else 2
        pady_val = (2, highlight_thickness_bottom + 1) if i % 3 == 2 and i != 8 else 2
        
        if j == 0 or j == 3 or j == 6:
             padx_val = (padx_val[0] + 1, padx_val[1]) if isinstance(padx_val, tuple) else (padx_val + 1, padx_val)
        if i == 0 or i == 3 or i == 6:
             pady_val = (pady_val[0] + 1, pady_val[1]) if isinstance(pady_val, tuple) else (pady_val + 1, pady_val)


        e.grid(row=i, column=j, padx=padx_val, pady=pady_val, sticky="nsew")
        
        
        if board[i][j] != 0:
            e.insert(0, str(board[i][j]))
            e.config(fg='black', state='readonly') 
        row_entries.append(e)
    entries.append(row_entries)


def new_board():
    global board
    board = generate_sudoku()

    # Clear and re-fill entries
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state='normal')  
            entries[i][j].delete(0, tk.END)

            if board[i][j] != 0:
                entries[i][j].insert(0, str(board[i][j]))
                entries[i][j].config(fg='black', state='readonly')
            else:
                entries[i][j].config(fg='blue', state='normal')


# New game button
new_game = tk.Button(root, text="New Game", font=('Arial',14), fg='white', bg='blue',
                     command=new_board)
new_game.grid(row=9, column=0, columnspan=9, pady=10)

# Check button
check_button = tk.Button(root, text="Check", font=('Arial',14), fg='white', bg='green',
                         command=check_sudoku)
check_button.grid(row=10, column=0, columnspan=9, pady=10)

root.mainloop()

