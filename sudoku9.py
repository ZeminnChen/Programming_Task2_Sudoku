import tkinter as tk
import random
from tkinter import messagebox


def generate_sudoku():
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
   
         
         
# Main       
root = tk.Tk()
root.title("Random 9x9 Sudoku")

board = generate_sudoku()
entries = []

BLOCK_PAD = 5  
NORMAL_PAD = 2  

# Create 9x9 grid
for i in range(9):
    row_entries = []
    for j in range(9):
        e = tk.Entry(root, width=3, justify='center', font=('Arial',18), fg='blue', bg='#f0f0f0')
        
        padx = BLOCK_PAD if j % 3 == 0 and j != 0 else NORMAL_PAD
        pady = BLOCK_PAD if i % 3 == 0 and i != 0 else NORMAL_PAD
        e.grid(row=i, column=j, padx=padx, pady=pady)
        
        if board[i][j] != 0:
            e.insert(0, str(board[i][j]))
            e.config(fg='black', state='readonly')  
        
        row_entries.append(e)
    entries.append(row_entries)

# New game button
new_game = tk.Button(root, text="New Game", font=('Arial',14), fg='white', bg='blue',
                     command=new_board)
new_game.grid(row=9, column=0, columnspan=9, pady=10)

# Check button
check_button = tk.Button(root, text="Check", font=('Arial',14), fg='white', bg='green',
                         command=check_sudoku)
check_button.grid(row=10, column=0, columnspan=9, pady=10)

root.mainloop()
