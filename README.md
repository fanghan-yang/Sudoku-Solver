# Sudoku-Solver
Sudoku-Solver: Improved Inference with AC-3 Algorithm 

The main purpose of the code is to completely solve sudoku games. In the game of Sudoku, player is given a partially-filled 
9 × 9 grid, grouped into a 3 × 3 grid of 3 × 3 blocks. The objective is to fill each square with a digit from 1 to 9, 
subject to the requirement that each row, column, and block must contain each digit exactly once.

13 puzzles have been made available in the folder called "sudoku_probles". In the folder, soduku9 is acknowledged as the 
hardest sudoku puzzle in the word. You are welcome to add more puzzles in the folder, as long as following the exact format 
as the 13 puzzles (9 rows, 9 columns, * stands for empty cell, number stands for given cell). After adding new puzzles, you 
can either use interface or change the path in main() to view and solve the puzzles, which will be covered later.

In this package, sudoku_solver.py contains several methods and a class serving as solvers to sudoku games. It can read the 
board specified by the file at the given path, and importantly, solve all the sudoku puzzles in an extremely efficient way.

main.py contains main() and interface() for input/output. You can either use interface or change the path in main() to find 
another puzzle. If you don't want use interface, just comment it in main(). The time of solving puzzles is also provided 
with solution.

