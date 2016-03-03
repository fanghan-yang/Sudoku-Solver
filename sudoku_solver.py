###############################################################################
#################################### Import ###################################
###############################################################################

import copy

###############################################################################
################################ Sudoku Solver ################################
###############################################################################

def sudoku_cells():
    '''return all cells in sudoku problem, used as a constant in Sudoku class'''
    all_cell = []
    for i in xrange(9):
        for j in xrange(9):
            all_cell.append((i, j))
    return all_cell

def sudoku_arcs():
    '''return a pair of cells corresponding to inequality constraints;
    each arc should be a pair of cells whose values cannot be equal in
    a solved puzzle'''
    all_arcs = []
    all_cell = sudoku_cells()
    for cell_1 in all_cell:
        for cell_2 in all_cell:
            # same cell
            if cell_1 == cell_2:
                continue
            # same row
            if cell_1[0] == cell_2[0]:
                all_arcs.append((cell_1, cell_2))
                continue
            # smae col
            if cell_1[1] == cell_2[1]:
                all_arcs.append((cell_1, cell_2))
                continue
            # same block
            if cell_1[0]/3 == cell_2[0]/3 and cell_1[1]/3 == cell_2[1]/3:
                all_arcs.append((cell_1, cell_2))
    return all_arcs

def read_board(path):
    '''read the input txt file, return the board which is used by
    Sudoku class'''
    board = {}                      # board represented as a dictionary
    row = 0
    f = open(path)
    for line in f:                  # read each line
        for col in xrange(9):       # read each char
            if line[col] == '*':
                board[(row, col)] = set(xrange(1, 10))
            else:
                board[(row, col)] = set([int(line[col])])
        row += 1
    return board

class Sudoku(object):

    CELLS = sudoku_cells()          # constant, all cells
    ARCS = sudoku_arcs()            # constant, all arcs

    def __init__(self, board):
        '''initialization'''
        self.board = board

    def get_values(self, cell):
        '''get possible values of a certain cell'''
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        '''remove any value in cell1 set for which there are no values in
        cell2 set satisfying the corresponding inequality constraint;
        i.o.w., remove any value in cell1 set if it violates cell2 set;
        i.o.w., if
            1. cell1 and cell2 are a ARCS pair
            2. cell2 set contains only one value
            3. cell2 set is a subset of cell1 set
        remove that value in cell1 set'''
        if (cell1, cell2) in self.ARCS:             # cell1 and cell2 are a ARCS pair
            if self.is_certain(cell2):              # cell2 set contains only one value
                if self.board[cell2].issubset(self.board[cell1]):   # cell2 set is a subset of cell1 set
                    self.board[cell1].difference_update(self.board[cell2])
                    return True
        return False

    def print_board(self):
        '''print the current board, used to checking completeness'''
        board = [[0] * 9 for i in xrange(9)]
        for cell in self.CELLS:
            if self.is_certain(cell):
                board[cell[0]][cell[1]] = list(self.board[cell])[0]
            elif len(self.board[cell]) == 0:
                board[cell[0]][cell[1]] = ''
        for row in xrange(9):
            print board[row]            # print each row

    def is_certain(self, cell):
        '''check if a cell is solved (has only a possible value)'''
        if len(self.board[cell]) == 1:
            return True
        return False
    
    def infer_ac3(self):
        '''inference with arc consistent algorithm'''
        queue = set()
        for arcs in self.ARCS:
            if not self.is_certain(arcs[0]) and self.is_certain(arcs[1]):
                queue.add(arcs)                             # only add useful arcs to queue
        while queue:
            first_arcs = queue.pop()                        # pop the first arcs in queue
            if self.remove_inconsistent_values(first_arcs[0], first_arcs[1]):
                if self.is_certain(first_arcs[0]):          # efficient
                    for arcs in self.ARCS:
                        if arcs[1] == first_arcs[0] and \
                           not self.is_certain(arcs[0]):    # efficient
                            queue.add(arcs)                 # only add useful arcs to queue

    def infer_improved_helper(self):
        '''solve a specific cell by examining the possible values for
        other cells in the same row, column, or block'''
        is_changed = False
        if not self.is_consistent():
            return is_changed
        for cell in self.CELLS:
            if len(self.board[cell]) > 1:
                for value in self.board[cell]:
                    
                    # exam possible values for other cells in the same row
                    make_change = True              # initialize flag
                    for col in xrange(9):
                        cell_temp = (cell[0], col)  # go over cells
                        if cell_temp == cell:       # skip itself
                            continue
                        if value in self.board[cell_temp]:
                            make_change = False     # terminate if the value is not unique
                            break
                    if make_change:
                        self.board[cell] = set([value])
                        is_changed = True
                        break

                    # exam possible values for other cells in the same column
                    make_change = True              # initialize flag
                    for row in xrange(9):
                        cell_temp = (row, cell[1])  # go over cells
                        if cell_temp == cell:       # skip itself
                            continue
                        if value in self.board[cell_temp]:
                            make_change = False     # terminate if the value is not unique
                            break
                    if make_change:
                        self.board[cell] = set([value])
                        is_changed = True
                        break

                    # exam possible values for other cells in the same block
                    make_change = True              # initialize flag
                    block_row = cell[0] / 3 * 3
                    block_col = cell[1] / 3 * 3
                    for delta_row in xrange(3):
                        for delta_col in xrange(3):
                            cell_temp = (block_row + delta_row, block_col + delta_col)
                            if cell_temp == cell:   # skip itself
                                continue
                            if value in self.board[cell_temp]:
                                make_change = False # terminate if the value is not unique
                                break
                    if make_change:
                        self.board[cell] = set([value])
                        is_changed = True
                        break
        return is_changed
        
    def infer_improved(self):
        '''improved inference version of AC-3'''
        self.infer_ac3()
        while self.infer_improved_helper():
            self.infer_ac3()

    def is_solved(self):
        '''check if the sudoku problem is solved'''
        for cell in self.CELLS:
            if self.is_certain(cell) is False:
                return False
        return True

    def is_consistent(self):
        '''check if the current assignment is consistent'''
        for cell in self.CELLS:
            if len(self.board[cell]) == 0:
                return False
        return True

    def heuristics(self):
        '''choose a reasonable cell according to heuristics (most constrained
        variable / most constraining variable), self must be unsolved object'''
        uncertain_cells = set()

        # heuristic 1: most constrained variable (least possible values)
        min_length = float('inf')
        for cell in self.CELLS:
            length = len(self.board[cell])
            if length > 1:
                uncertain_cells.add(cell)   # build set for heuristic 2, for efficiency
                if length < min_length:     # find a most constrained variable
                    most_constrained_cells = set([cell])
                elif length == min_length:  # find a tie of most constrained variables
                    most_constrained_cells.add(cell)

        # heuristic 2: most constraining variable (most adjacent cells)
        max_length = 0
        if len(most_constrained_cells) > 1: # tie in heuristic 1
            for cell in most_constrained_cells:
                count = 0
                for another_cell in uncertain_cells.difference(set(cell)):
                    if (cell, another_cell) in self.ARCS:
                        count += 1
                if count > max_length:      # find a most constraining variable
                    most_constraining_cell = cell
            return most_constraining_cell
        else:
            return most_constrained_cells.pop()
        
    def infer_with_guessing_helper(self):
        '''recursive-backtracking with heuristics 1&2'''
        if self.is_solved():                # solution found
            return self.board               # board as solution
        cell = self.heuristics()            # choose a cell with heuristics 1&2
        for value in self.board[cell]:      # guessing
            sudoku = copy.deepcopy(self)
            sudoku.board[cell] = set([value])
            sudoku.infer_improved()
            if sudoku.is_consistent():      # still solvable after guessing
                solution = sudoku.infer_with_guessing_helper()  # recursion
                if solution is not None:    # pass solution back to root
                    return solution
    
    def infer_with_guessing(self):
        '''full solution to sudoku problem'''
        self.infer_improved()
        self.board = self.infer_with_guessing_helper()
