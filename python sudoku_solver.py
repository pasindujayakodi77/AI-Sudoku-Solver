import random
import tkinter as tk
from tkinter import messagebox

# Sudoku Solver
def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def sudoku_solver(board):
    empty_cell = find_empty_location(board)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if sudoku_solver(board):
                return True
            board[row][col] = 0

    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# Sudoku Puzzle Generator
def generate_board():
    board = [[0] * 9 for _ in range(9)]
    fill_board(board)
    return board

def fill_board(board):
    for _ in range(9):  # Try to fill 9 random numbers to start
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        while not is_valid(board, row, col, num) or board[row][col] != 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
        board[row][col] = num
    return board

# Reset the board to the initial puzzle
def reset_board(board, original_board):
    for i in range(9):
        for j in range(9):
            board[i][j] = original_board[i][j]
    
# GUI Setup with Tkinter
class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver Game")

        self.board = [[0] * 9 for _ in range(9)]
        self.original_board = [[0] * 9 for _ in range(9)]
        self.cells = {}
        self.create_ui()

        self.new_game()

    def create_ui(self):
        for row in range(9):
            for col in range(9):
                cell = tk.Entry(self.root, width=5, font=('Arial', 18), justify='center', bd=2, relief="solid")
                cell.grid(row=row, column=col, padx=5, pady=5)
                self.cells[(row, col)] = cell

        # Buttons for interacting with the game
        self.solve_button = tk.Button(self.root, text="Solve", width=10, command=self.solve_game)
        self.solve_button.grid(row=9, column=0, columnspan=3)

        self.reset_button = tk.Button(self.root, text="Reset", width=10, command=self.reset_game)
        self.reset_button.grid(row=9, column=3, columnspan=3)

        self.new_game_button = tk.Button(self.root, text="New Game", width=10, command=self.new_game)
        self.new_game_button.grid(row=9, column=6, columnspan=3)

    def display_board(self):
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                self.cells[(row, col)].delete(0, tk.END)
                if value != 0:
                    self.cells[(row, col)].insert(0, str(value))

    def get_user_input(self):
        for row in range(9):
            for col in range(9):
                value = self.cells[(row, col)].get()
                if value.isdigit() and int(value) in range(1, 10):
                    self.board[row][col] = int(value)
                else:
                    self.board[row][col] = 0

    def solve_game(self):
        self.get_user_input()
        if sudoku_solver(self.board):
            self.display_board()
        else:
            messagebox.showinfo("No Solution", "No solution exists for this Sudoku puzzle.")

    def reset_game(self):
        self.board = [[0] * 9 for _ in range(9)]
        reset_board(self.board, self.original_board)
        self.display_board()

    def new_game(self):
        self.board = generate_board()
        self.original_board = [row[:] for row in self.board]
        self.display_board()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
