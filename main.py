############################################################
########################## Import ##########################
############################################################

import os
import time
from sudoku_solver import *

############################################################
###################### Main Function #######################
############################################################

def main():

    # you may want to change the default path here
    path = "sudoku1.txt"

    # this in interface, if you don't want it, just comment it
    path = interface(path)
        
    # create puzzle
    try:
        sudoku = Sudoku(read_board(path))
    except:
        print
        print "This is not a readable sudoku puzzle."
        return
    print
    print "Original Sudoku Puzzle:"
    sudoku.print_board()                # print unsolved board

    # timing and solving
    start = time.time()                 # tic
    sudoku.infer_with_guessing()        # solve it
    end = time.time()                   # toc

    # output
    print
    print "Solution:"
    sudoku.print_board()                # print solved board
    
    print
    print "Timing:", str(end - start) + 's'   # print timing
    print

def interface(path):
    print
    print "############################## File Uploading ##############################"
    print
    print "The path of puzzle to be solved is default to '" + path + "'."
    print
    print "Enter 1 to keep it, or enter a path (eg. enter 'sudoku_problems/sudoku9.txt'"
    print "without qutation) to change it."
    while True:
        print
        user_input = raw_input('>>> ')
        if user_input == '1':
            user_input = path
        if os.path.exists(user_input):
            try:
                sudoku = Sudoku(read_board(user_input))
            except:
                print "This is not a readable sudoku puzzle. Please enter another one."
                continue
            path = user_input
            print
            print "File uploading ... Done!"
            break
        print "File '" + user_input + "' does not exist. Please enter another one."
    return path

if __name__ == "__main__":
    main()
