import pygame
from random import sample, randint, random
from tabulate import tabulate

config  =   {
                "cell_width"            :   50,
                "cell_height"           :   50,
                "cell_color"            :   (235,235,235),
                "cell_color_hover"      :   (220,220,255),
                "cell_color_locked"     :   (255,220,220),
                "cell_color_editing"    :   (220,255,220),
                "cell_color_wrong"      :   (255,120,120),
                "cell_padding"          :   3,
                "background"            :   (0,0,0),
                "color_number"          :   (0,0,0),
                "window_name"           :   "Soduko!",
                "difficulty"            :   0.5,
            }

class Game(object):
    def __init__(self, config):
        self.config         =   config    
        
        #Initiate pygame
        pygame.init()
        pygame.display.set_caption(config['window_name'])
        
        #Set up pygame parameters
        self.view   =   pygame.display.set_mode((9*(config['cell_width' ]+config['cell_padding'])+3*config['cell_padding'],
                                                 9*(config['cell_height']+config['cell_padding'])+3*config['cell_padding']))
        self.font           =   pygame.font.SysFont('comicsansms', int(config['cell_height']*0.8))
        self.font_initial   =   pygame.font.SysFont('comicsansms', int(config['cell_height']*0.8), True)
        self.font_predicted =   pygame.font.SysFont('comicsansms', int(config['cell_height']*0.4))

        #Set up some variables
        self.solution       =   self.generate_board()
        self.cell_board     =   self.gamify(self.solution)
        self.running        =   True 
        self.check_mouse()
        self.clock = pygame.time.Clock()
        self.win            =   False
        self.pressed        =   False
        

    def check_mouse(self):
        self.pos        =   pygame.mouse.get_pos()
        self.pressed,_,_=  pygame.mouse.get_pressed()

    def draw_board(self):
        for row in self.cell_board:
            for cell in row:
                cell.draw()
                
    def draw_background(self):
        self.view.fill(self.config['background'])
        
    def gamify(self, solution):
        #Generate cell structure:
        cell_board   =   [[0 for _ in range(9)] for _ in range(9)]
        for i,row in enumerate(solution):
            for j,number in enumerate(row):
                if random() > self.config['difficulty']:
                    value   =   0
                else:
                    value   =   number
                cell_board[i][j]    =   Cell(self,i,j,value)
        return cell_board

    def generate_board(self):
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
    
    def check_keyboard(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_c]:
            for i,row in enumerate(self.cell_board):
                for j,cell in enumerate(row):
                    if cell.value != self.solution[i][j] and cell.value != 0:
                        cell.correct    =   False 
                    elif cell.value == self.solution[i][j]:
                        cell.correct    =   True
                    else:
                        cell.correct    =   None 
        if pressed[pygame.K_SPACE]:
            self.solve(self.cell_board)
            self.check_for_win()
            
    
    def check_for_win(self):      
        validity    =   self.check_validity(self.cell_board)
        all_entry   =   True
        for row in self.cell_board:
            for cell in row:
                if cell.value ==0: all_entry   =   False
        self.win = validity*all_entry


        
    def check_validity(self, board):
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
                value       =   board[row][col].value
                if value !=0:
                    counter[value-1]  += 1
            for count in counter:
                if count >1:
                    valid=False
        return valid
            

    def solve(self, board, position=0):
        self.draw_background()
        self.draw_board()
        pygame.display.update()
        self.clock.tick(10000)
        row, col    =   position//9, position%9
        sol_found  =   False
        #Check the if we are at the end
        if position>=81:
            return True, board

        #Skip if it is an initial value
        if board[row][col].initial_value  != 0:
            sol_found, board    =   self.solve(board, position+1)
            if sol_found:
                return True, board
            else:
                return False, board

        #Try all different values:
        for value in range(1,10):
            board[row][col].value =   value
            valid_solution          =   self.check_validity(board)
            if valid_solution:
                sol_found, board    =   self.solve(board, position+1)
                if sol_found:
                    return True, board
        
        board[row][col].value =   0
        return False, board


class Cell(object):
    def __init__(self, parent, row, col, value):
        self.value          =   value
        self.row            =   row
        self.col            =   col
        self.initial_value  =   value
        self.parent         =   parent
        self.clicked        =   False
        self.hover          =   False
        self.predicted      =   []
        self.correct        =   None
    
    def draw(self):
        #Plot the square. Fix the formatting after
        square  =   self.draw_cell(self.parent.config['cell_color'])

        color   =   self.pick_color(square)        
        square  =   self.draw_cell(self.parent.config[color])
        self.add_text(square)
    
    def pick_color(self, square):
        color   =   'cell_color'

        #Check if it's correct
        if self.correct==False:
            color   =   'cell_color_wrong'
        
        #Check hover
        if square.collidepoint(self.parent.pos):
            self.hover  =   True
            color   = 'cell_color_hover'
        else:
            self.hover  =   False
            self.clicked=   False
        
        #Check click
        if self.hover and self.parent.pressed:
            self.clicked    =   True
        
        #Update value if clicked
        if self.clicked and self.hover:
            if self.initial_value!=0:
                color   =   'cell_color_locked'
            else:
                color   =   'cell_color_editing'
                self.listen_for_number()
        return color

    def add_text(self, square):
        
        #Stringify the value. Don't show a number
        if self.value != 0: 
            cell_data = str(self.value)
        else:
            cell_data = ''
            for digit in self.predicted:
                cell_data += str(digit)
        
        if self.initial_value!=0:
            text            =   self.parent.font_initial.render(cell_data, True, self.parent.config['color_number'])
        elif len(self.predicted)>0:
            text            =   self.parent.font_predicted.render(cell_data, True, self.parent.config['color_number'])
        else:
            text            =   self.parent.font.render(cell_data, True, self.parent.config['color_number'])
        
        #Add text to the square
        textRect        =   text.get_rect()
        textRect.center =   square.center
        self.parent.view.blit(text, textRect)

    def draw_cell(self, color):
        #Compute position of the square
        x_pos  = self.col*(self.parent.config['cell_width']+self.parent.config['cell_padding'])+(1+self.col//3)*self.parent.config['cell_padding']
        y_pos  = self.row*(self.parent.config['cell_height']+self.parent.config['cell_padding'])+(1+self.row//3)*self.parent.config['cell_padding']
        return pygame.draw.rect(self.parent.view, color, (x_pos, y_pos, self.parent.config['cell_width'], self.parent.config['cell_height']))

    def listen_for_number(self):
        for event in pygame.event.get():#pygame.time.get_ticks-self.parent.last_pressed>1000:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1 or event.key==pygame.K_KP1:    self.predict(1)
                if event.key==pygame.K_2 or event.key==pygame.K_KP2:    self.predict(2)
                if event.key==pygame.K_3 or event.key==pygame.K_KP3:    self.predict(3)
                if event.key==pygame.K_4 or event.key==pygame.K_KP4:    self.predict(4)
                if event.key==pygame.K_5 or event.key==pygame.K_KP5:    self.predict(5)
                if event.key==pygame.K_6 or event.key==pygame.K_KP6:    self.predict(6)
                if event.key==pygame.K_7 or event.key==pygame.K_KP7:    self.predict(7)
                if event.key==pygame.K_8 or event.key==pygame.K_KP8:    self.predict(8)
                if event.key==pygame.K_9 or event.key==pygame.K_KP9:    self.predict(9)
                if event.key==pygame.K_DELETE or event.key==pygame.K_BACKSPACE:
                    try:
                        self.predicted.remove(self.predicted[-1])
                    except:
                        pass
                    self.set_number(0)
                if event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                    if len(self.predicted)  ==  1:
                        self.set_number(self.predicted[0])
                        self.predicted=[]

        self.parent.check_for_win()

    def set_number(self, number):
        self.parent.pressed     =   True
        self.correct    =   None
        valid_input     =   self.parent.check_validity(self.parent.cell_board)
        if not valid_input:
            self.correct    =   False
        self.value      =   number

    def predict(self, number):
        self.parent.pressed     =   True
        if self.value == 0:
            if number not in self.predicted:
                self.predicted.append(number)
            else:
                self.predicted.remove(number)

# Draw Once
game            =   Game(config)

while game.running:
    #Get input
    game.check_mouse()
    game.check_keyboard()

    if not game.win:
        #Draw the board
        game.draw_background()
        game.draw_board()
    else:
        print("WIN")
        print(game.win)
        exit()
    
    #Update view
    pygame.display.update()

    #Limit framerate to 30 fps.
    game.clock.tick(30)

    #Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
    