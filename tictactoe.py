import sys
import copy
import random
import pygame
import numpy as np


# Constants
WIDTH = 700
HEIGHT = 700
#colors
BACKGROUND_COLOR = (255, 128, 0) #cross is in White
LINE_COLOR = (239, 231, 200) #cross is in pink
CROSS_COLOR = (0, 153, 153) #cross is in blue
CIRCLE_COLOR = (204, 0, 102) #cross is in pink
#setting the rows and colums
ROWS = 3 #3 rows
COLS = 3 # 3 colums
LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20
SQSIZE = WIDTH // COLS #colum divide by 3
RADIUS = SQSIZE // 4
OFFSET = 50


# PYGAME SETUP
pygame.init() #start game
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # display the width anf the height of the board
pygame.display.set_caption('TIC TAC TOE') #caption of the game
screen.fill(BACKGROUND_COLOR) #the color fill of the game

# CLASSES
class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.marked_sqrs = 0

    def final_state(self, show=False):
        # Checking for a vertical wins
        for col in range(COLS): #loops over each column in the game grid
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0: # it checks that the vlaues of the element are eqal for a verticall win
                # if it's true draw me a vertical line
                if show:
                    self.draw_vertical_win_line(col)
                return self.squares[0][col]

         # Checking for a horizontal wins
        for row in range(ROWS): #loops over each row in the game grid
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0: # it checks that the vlaues of the element are eqal for a horizonatal win
                 # if it's true draw me a horizonatal line
                if show:
                    self.draw_horizontal_win_line(row)
                return self.squares[row][0]

        # Checking for a  desc diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0: # it checks that the vlaues of the element are eqal for a desc diagonal win
             # if it's true draw me a horizonatal line
            if show:
                self.draw_desc_diagonal_win_line() 
            return self.squares[1][1]

        # Checking for a asc diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0: # it checks that the vlaues of the element are eqal for a asc diagonal win
             # if it's true draw me a horizonatal line
            if show:
                self.draw_asc_diagonal_win_line()
            return self.squares[1][1]

        return 0

    # drawing a vertical line which represnt the column index
    def draw_vertical_win_line(self, col):
        color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR #color of the line
        iPos = (col * SQSIZE + SQSIZE // 2, 20) #This line defines the starting position of the line to be drawn.
        fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20) # This line defines the ending position of the line to be drawn.
        pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH) #draw the line

    # drawing a horizontal line which represnt the row index
    def draw_horizontal_win_line(self, row):
        color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR #color of the line
        iPos = (20, row * SQSIZE + SQSIZE // 2) #This line defines the starting position of the line to be drawn.
        fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2) # This line defines the ending position of the line to be drawn.
        pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH) #draw the line

    def draw_desc_diagonal_win_line(self):
        color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR #color of the line
        iPos = (20, 20) #This line defines the starting position of the line to be drawn.
        fPos = (WIDTH - 20, HEIGHT - 20) # This line defines the ending position of the line to be drawn.
        pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH) #draw the line

    def draw_asc_diagonal_win_line(self):
        color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR #color of the line
        iPos = (20, HEIGHT - 20) # This line defines the starting position of the line to be drawn.
        fPos = (WIDTH - 20, 20) # This line defines the ending position of the line to be drawn.
        pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH) #draw the line

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
        else:
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move

class Game:
    def __init__(self):
        # Initialize the game board and AI
        self.board = Board()
        self.ai = AI()
        
        # Set initial player (1 for cross, 2 for circle), game mode, and running status
        self.player = 1
        self.gamemode = 'ai'  # Options: 'pvp' for player vs. player, 'ai' for player vs. AI
        self.running = True
        
        # Display the game lines
        self.show_lines()

    # Method to draw the game lines on the screen
    def show_lines(self):
        # Draw background
        screen.fill(BACKGROUND_COLOR)

        # Draw vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Draw horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    # Method to draw player's figure (cross or circle) on the board at given row and column
    def draw_fig(self, row, col):
        if self.player == 1:
            # Calculate start and end points for the descending and ascending lines of the cross
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)

            # Draw both lines of the cross
            for pos in [(start_desc, end_desc), (start_asc, end_asc)]:
                pygame.draw.line(screen, CROSS_COLOR, pos[0], pos[1], CROSS_WIDTH)
        elif self.player == 2:
            # Calculate center point for the circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            
            # Draw circle
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    # OBJECT
    game = Game()
    board = game.board
    ai = game.ai

    #MAIN LOOP
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                 # If the user quits the game, quit pygame and exit the program
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # If a key is pressed down
                if event.key == pygame.K_g:
                    # If the 'g' key is pressed, change the game mode
                    game.change_gamemode()
    
                elif event.key == pygame.K_r:
                     # If the 'r' key is pressed, reset the game
                    game.reset()
                    board = game.board
                    ai = game.ai

                elif event.key == pygame.K_0:
                     # If the '0' key is pressed, set the AI level to 0 (random moves)
                    ai.level = 0

                elif event.key == pygame.K_1:
                    # If the '1' key is pressed, set the AI level to 1 (smart moves)
                    ai.level = 1


            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                mouse_pos = event.pos

                # Calculate the corresponding row and column on the game board
                Clicked_row = mouse_pos[1] // SQSIZE
                Clicked_col = mouse_pos[0] // SQSIZE

                  # Check if the clicked square is empty and the game is still running
                if board.empty_sqr(Clicked_row, Clicked_col) and game.running:
                     # Make a move at the clicked position
                    game.make_move(Clicked_row, Clicked_col)

                    # Check if the game is over after the move
                    if game.isover():
                        game.running = False

        # AI move if in AI mode and it's AI's turn
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #UPDATE THE SCREEN
            pygame.display.update()

            #AI METHODS
            ai_row, ai_col = ai.eval(board)
            game.make_move(ai_row, ai_col)
            
            # Check if the game is over after the AI move
            if game.isover():
                game.running = False
        
        
        pygame.display.update()
                 

main()
