import tkinter as tk
import random
from tkinter import messagebox


def generate_sudoku():
    # Base 6x6 Sudoku
    base = [
        [1,2,3,4,5,6],
        [4,5,6,1,2,3],
        [2,3,1,5,6,4],
        [5,6,4,2,3,1],
        [3,1,2,6,4,5],
        [6,4,5,3,1,2]
    ]

    # rows 
    for _ in range(10):
        block = random.choice([0,2,4])
        r1, r2 = block + random.randint(0,1), block + random.randint(0,1)
        while r1 == r2:
            r2 = block + random.randint(0,1)
        base[r1], base[r2] = base[r2], base[r1]


    # cols
    for _ in range(10):
        block = random.choice([0,3])
        c1, c2 = block + random.randint(0,2), block + random.randint(0,2)
        while c1 == c2:
            c2 = block + random.randint(0,2)
        for r in range(6):
            base[r][c1], base[r][c2] = base[r][c2], base[r][c1]


    board = [row[:] for row in base]

    count = 0
    while count < 12:
        i, j = random.randint(0,5), random.randint(0,5)
        if board[i][j] != 0:
            board[i][j] = 0
            count += 1

    return board



def check_sudoku():
    # 0. Check if the board is filled
    for i in range(6):
        for j in range(6):
            if entries[i][j].get().strip() == "":
                messagebox.showinfo("Result", "The Sudoku is not complete yet.")
                return
            
    # 1. Check values
    temp_board = [[0]*6 for _ in range(6)]  
    for i in range(6):
        for j in range(6):
            val_str = entries[i][j].get()
            try:
                val = int(val_str)
                if 1 <= val <= 6:
                    temp_board[i][j] = val
                else:
                    messagebox.showwarning("Invalid", f"Number at row {i+1}, column {j+1} must be 1-6.")
                    return
            except:
                messagebox.showwarning("Invalid", f"Number at row {i+1}, column {j+1} must be 1-6.")
                return

    # 2. Check rows
    for i in range(6):
        row = temp_board[i]
        if len(row) != len(set(row)):
            messagebox.showinfo("Result", f"Error in row {i+1}. Duplicate numbers found.")
            return

    # 3. Check cols
    for col in range(6):
        col_vals = [temp_board[row][col] for row in range(6)]
        if len(col_vals) != len(set(col_vals)):
            messagebox.showinfo("Result", f"Error in column {col+1}. Duplicate numbers found.")
            return

    # 4. Check 2x3 blocks
    for r in [0, 2]:
        for c in [0, 3]:
            block = []
            for i in range(2):
                for j in range(3):
                    block.append(temp_board[r+i][c+j])
            if len(block) != len(set(block)):
                messagebox.showinfo("Result", f"Error in 2x3 block starting at row {r+1}, column {c+1}.")
                return

    global board
    board = temp_board
    messagebox.showinfo("Result", "Sudoku is correct! Well done!")



def new_board():
    global board
    board = generate_sudoku()

    # Clear and re-fill entries
    for i in range(6):
        for j in range(6):
            entries[i][j].config(state='normal')  
            entries[i][j].delete(0, tk.END)

            if board[i][j] != 0:
                entries[i][j].insert(0, str(board[i][j]))
                entries[i][j].config(fg='black', state='readonly')
            else:
                entries[i][j].config(fg='blue', state='normal')



# Main
root = tk.Tk()
root.title("Random 6x6 Sudoku")

board = generate_sudoku()
entries = []

# Create 6x6 grid
for i in range(6):
    row_entries = []
    for j in range(6):
        e = tk.Entry(root, width=3, justify='center', font=('Arial',18), fg='blue', bg='#f0f0f0')
        e.grid(row=i, column=j, padx=3, pady=3)
        
        if board[i][j] != 0:
            e.insert(0, str(board[i][j]))
            e.config(fg='black', state='readonly')  
        row_entries.append(e)
    entries.append(row_entries)

# New game button
new_game = tk.Button(root, text="New Game", font=('Arial',14), fg='white', bg='blue',
                     command=new_board)
new_game.grid(row=6, column=0, columnspan=6, pady=10)

# Check button
check_button = tk.Button(root, text="Check", font=('Arial',14), fg='white', bg='green',
                         command=check_sudoku)
check_button.grid(row=7, column=0, columnspan=6, pady=10)
root.mainloop()
