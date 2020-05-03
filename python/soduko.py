from random import sample, randint, seed
from tabulate import tabulate

DIFFICULTY  =   5   #From 1 to 10

def main():    
    #Build a board
    solution    =   generate_board()
    
    #Remove x amount of pieces randomly (based on DIFFICULTY)
    board       =   gamify(solution)

    #Build a solver
    #guess       =   solve(board)
    
    #show(guess)
    print(board)
    

def check_validity(board):
    combinations    =   []
    squares         =   [[0,1,2], [3,4,5], [6,7,8]]
    valid           =   True

    #Add columns and rows
    for i in range(9):
        combinations.append([ 9*i+k for k in range(9)])
        combinations.append([ i+k*9 for k in range(9)])

    #Add squares
    for row in squares:
        for col in squares:
            combination     =   []
            for a in row:
                for b in col:
                    combination.append(a*9+b)
            combinations.append(combination)
    
    #Check combinations
    for combination in combinations:
        counter =   [0 for _ in range(9)]
        for position in combination:
            row, col    =   position//9, position%9
            value       =   board[row][col]
            if value !=0:
                counter[value-1]  += 1
        for count in counter:
            if count >1:
                valid=False
    return valid
        

def testing(current_board, initial_board, position):
    row, col    =   position//9, position%9
    sol_found  =   False
    #Check the if we are at the end
    if position>=81:
        return True, current_board

    #Skip if it is an initial value
    if initial_board[row][col]  != 0:
        
        sol_found, board    =   testing(current_board, initial_board, position+1)
        if sol_found:
            return True, board
        else:
            return False, board

    #Try all different values:
    for value in range(1,10):
        
        current_board[row][col] =   value
        valid_solution          =   check_validity(current_board)
        if valid_solution:
            sol_found, board    =   testing(current_board, initial_board, position+1)
            if sol_found:
                return True, board
    
    current_board[row][col] =   0
    return False, current_board


def solve(current_board):
    print("Looking for solution")
    _, board   =   testing(current_board, current_board, 0)
    return board


def gamify(board):
    #Choose the amount of tiles to remove
    n  =   int(6.3*DIFFICULTY)

    #Remove n tiles from the board
    while n>0:
        removee     =   randint(0,80)
        row, col    =   removee//9 , removee%9
        if board[row][col] != 0:
            board[row][col] = 0
            n  -=  1
    
    return board

def show(board):
    print(tabulate(board))

def generate_board():
    base  = 3

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%(base**2)

    # randomize rows, columns and numbers (of valid base pattern)
    def shuffle(s): return sample(s,len(s)) 
    rBase = range(base)
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    return board

if __name__=='__main__':
    main()