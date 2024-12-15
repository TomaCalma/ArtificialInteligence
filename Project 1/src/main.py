import numpy as np
import pygame
import sys
import math
import time
from dataclasses import dataclass
from puzzle.constants import WIDTH,HEIGHT,X3_PUZZLE,X3_PUZZLE_SOL,X4_PUZZLE,X4_PUZZLE_SOL,PUZZLE1,PUZZLE1_SOL,PUZZLE2,PUZZLE2_SOL,PUZZLE3,PUZZLE3_SOL,PUZZLE4,PUZZLE4_SOL,PUZZLE5,PUZZLE5_SOL,PUZZLE6,PUZZLE6_SOL,PUZZLE7,PUZZLE7_SOL,PUZZLE8,PUZZLE8_SOL,PUZZLE9,PUZZLE9_SOL,BLACK,WHITE,RED
from puzzle.Board import Board
from puzzle.Puzzle import Puzzle
from collections import deque
import copy


pygame.init() #Initializing pygame
FPS = 60 #Available frame rate for the game
font = pygame.font.SysFont('Arial',60) #Sets the default font for the text
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #Creates the game window
pygame.display.set_caption("Symmetry Puzzle") #Name of the game window



#
# This function slots the given puzzle into the target board, mostly for starting a puzzle
#
def slot_in_matrix(puzzle,board):
        board.board_matrix = np.reshape(puzzle.initial_puzzle,(board.size,board.size))
    
#
# This function creates the initial board aswell as updates the display when a puzzle is started
#
def start_puzzle(board,puzzle):
    board = Board(int(math.sqrt(puzzle.size)))
    slot_in_matrix(puzzle, board)
    update_board_display(board)
    return board

#
# This function calls the entirety of the drawing elements needed in the screen for the board in play
#
def update_board_display(board):
    board.draw_background(WIN,board.size)
    board.update_display(WIN,board)
    pygame.display.update()

#
# This function checks if we have reached the solution of the initial puzzle
#
def check_win(board,puzzle):
    for x in range (board.size):
        for y in range (board.size):
            if(board.board_matrix[x][y].upper() != puzzle.puzzle_solution[x][y].upper()):
                return False
    return True

#
# Calls the prompt for the user to select an algorythm when in AI player
#
def algorythm_selection():
    create_text_rect("Please select an algorythm [1-9]:",WIDTH/2,50)
    create_text_rect("1.BFS",WIDTH/2,150)
    create_text_rect("2.DFS",WIDTH/2,250)
    create_text_rect("3.Iterative Deepening",WIDTH/2,350)
    create_text_rect("4.Greedy",WIDTH/2,450)
    create_text_rect("Press ""S"" to start the algorithm!",WIDTH/2,650)

#
# Base function to create any rectangle with a certain text at position x,y
#
def create_text_rect(text,x,y):
    text = font.render(text,True,WHITE,BLACK)
    textRect= text.get_rect()
    textRect.center = (x,y)
    WIN.blit(text,textRect)
    pygame.display.update()

#
# Prints the current game mode
#
def print_mode(mode):
    if(mode==1):
        create_text_rect("Current mode: Human player",WIDTH/2,HEIGHT-40)
    elif(mode==2):
        create_text_rect("Current mode: AI player",WIDTH/2,HEIGHT-40)

#
# When called this function return the player to the main menu of the game
#
def main_screen():
    img = pygame.image.load("SymmetryPuzzleMenu.png").convert()
    WIN.blit(img,(0,0))
    #WIN.fill(BLACK)
    pygame.display.update()

#
# Generates all the possible boards we can reach using operations of cost 1 for a given board
#
def one_step_expansion(board):
    next_generation = []

    for i in range (board.size):
        for j in range (board.size):
            if(board.board_matrix[i][j] == " "):
                BoardQ = copy.deepcopy(board)
                BoardQ.update_shape(BoardQ,i,j,"q")
                BoardQ.update_depth(BoardQ)
                next_generation.append(BoardQ)

                BoardC = copy.deepcopy(board)
                BoardC.update_shape(BoardC,i,j,"c")
                BoardC.update_depth(BoardC)
                next_generation.append(BoardC)

                BoardT = copy.deepcopy(board)
                BoardT.update_shape(BoardT,i,j,"t")
                BoardT.update_depth(BoardT)
                next_generation.append(BoardT)
    
    return next_generation

#
# Breadth First Search Algorithm
#
def BFS(puzzle,board):
    visited = []
    queue = deque()
    queue.append(board)

    while(len(queue)>0):
        cur_board = queue.popleft()
        visited.append(cur_board)
        #print(cur_board.depth)

        next_generation = one_step_expansion(cur_board)

        #update_board_display(cur_board)
        #time.sleep(0.05)

        for i in next_generation:
            if(not(i in visited)):
                if(check_win(cur_board,puzzle)):
                    print("Solution Found")
                    update_board_display(cur_board)
                    return True
                queue.append(i)

    return False

#
# Depth First Search Algorithm
#
def DFS(puzzle,board):
    visited = []
    stack = deque()
    stack.append(board)

    while(len(stack)>0):
        cur_board = stack.pop()
        visited.append(cur_board)
        #print(cur_board.depth)

        next_generation = one_step_expansion(cur_board)

        #update_board_display(cur_board)
        #time.sleep(0.05)

        for i in next_generation:
            if(not(i in visited)):
                if(check_win(cur_board,puzzle)):
                    print("Solution Found")
                    update_board_display(cur_board)
                    return True
                stack.append(i)

    return False

#
# Iterative Deepening Algorithm
#
def Iterative(puzzle,board,max_depth):
    for depth in range(max_depth+1):
        result = depth_limited_search(puzzle,board,depth)
        if result is not None:
            update_board_display(result)
            return True
    return False

#
# Auxiliary function for the iterative deepening function
#
def depth_limited_search(puzzle,board,depth_limit):
    next_generation = one_step_expansion(board)
    #update_board_display(board)
    #time.sleep(0.05)

    if (check_win(board,puzzle)):
        return board
    if(depth_limit == 0):
        return None
    for i in next_generation:
        #update_board_display(i)
        #time.sleep(0.05)
        result = depth_limited_search(puzzle,i,depth_limit-1)
        if result is not None:
            return result
    return None

#
# Greedy Approach to the search problem using the selected heuristic
#
def Greedy(puzzle,board,heuristic):
    cur_board = board
    while(not(check_win(cur_board,puzzle))):
        next_generation = one_step_expansion(cur_board)
        best_board = None
        best_score = float('inf')
        for i in next_generation:
            score = heuristic(i)
            if(score < best_score):
                best_score = score
                best_board = i
                update_board_display(i)
                time.sleep(0.05)
        cur_board = best_board
        if(cur_board==None):
            return False
    update_board_display(cur_board)
    return True

#
# An heuristic function that gives us how far away from the winning score are we
#
def score_heuristic(board):
    max_score = 2*board.size
    current_score = board.get_updated_score(board)
    return max_score-current_score

#
# The main function of the game
#
def main():
    run = True
    clock = pygame.time.Clock()
    board = Board(0)
    mode_select = 1 #Initializes the game as a single player game
    started_game = False #Marks if we are currently in a game or not
    game_won = False #Marks if we have finished the game currently going on (if any)
    main_screen() #Calls the main screen
    create_text_rect("Current mode: Human player",WIDTH/2,HEIGHT-40) #Prints the initial mode

    while(run):   #Main loop for the game
        clock.tick(FPS)

        for event in pygame.event.get(): #Check if the user has quit the game using the normal window close button
            if event.type == pygame.QUIT:
                run = False

            
            if (event.type == pygame.KEYDOWN and (started_game==False)): #Level and gamemode selection
                if event.key == pygame.K_m:  #The "M" key switches between the mod (gamemode=1 for player or gamemode=2 for AI)
                    if(mode_select==1):
                        mode_select = 2
                    else:
                        mode_select = 1
                    main_screen()
                    print_mode(mode_select)
                else: #We use numbers from 1-9 to select possible puzzles
                    if event.key == pygame.K_1:
                        current_puzzle = Puzzle(X3_PUZZLE,X3_PUZZLE_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_2:
                        current_puzzle = Puzzle(X4_PUZZLE,X4_PUZZLE_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_3:
                        current_puzzle = Puzzle(PUZZLE3,PUZZLE3_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_4:
                        current_puzzle = Puzzle(PUZZLE4,PUZZLE4_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_5:
                        current_puzzle = Puzzle(PUZZLE5,PUZZLE5_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_6:
                        current_puzzle = Puzzle(PUZZLE6,PUZZLE6_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_7:
                        current_puzzle = Puzzle(PUZZLE7,PUZZLE7_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_8:
                        current_puzzle = Puzzle(PUZZLE8,PUZZLE8_SOL)
                        board = start_puzzle(board,current_puzzle)
                    if event.key == pygame.K_9:
                        current_puzzle = Puzzle(PUZZLE9,PUZZLE9_SOL)
                        board = start_puzzle(board,current_puzzle)
                    started_game = True

            if (event.type == pygame.MOUSEBUTTONDOWN and mode_select==1 and started_game==True): #Handler of the ingame moves for the player
                board.update_next_shape(board,pygame.mouse.get_pos())
                update_board_display(board)
                board.update_score(board)
                #print(board.score)
                #print(board.board_matrix)
                #print(current_puzzle.puzzle_solution)
                if(check_win(board,current_puzzle)): #Checks if the puzzle has been completed
                    print("Puzzle completed!")
                    game_won = True
                if(game_won==True): #Acts when we have completed the puzzle
                    create_text_rect("Puzzle completed!",WIDTH/2,HEIGHT/2)
                    time.sleep(3)
                    main_screen()
                    print_mode(mode_select)
                    game_won=False
                    started_game=False

            if (event.type == pygame.KEYDOWN and mode_select==2 and started_game==True): #and (event.key == pygame.K_s)): #Handler of the AI algorithm selection and moves
                #print("Im here")
                ai_found_sol = False
                algorythm_selection()
                if(event.key == pygame.K_1):
                    alg_select = 1
                    create_text_rect("Currently selected: 1",WIDTH/2,750)
                elif(event.key == pygame.K_2):
                    alg_select = 2   
                    create_text_rect("Currently selected: 2",WIDTH/2,750)
                elif(event.key == pygame.K_3):
                    alg_select = 3 
                    create_text_rect("Currently selected: 3",WIDTH/2,750)
                elif(event.key == pygame.K_4):
                    alg_select = 4  
                    create_text_rect("Currently selected: 4",WIDTH/2,750)
                elif(event.key == pygame.K_s):
                    pass
                else:
                    alg_select = 1

                if(alg_select != 0 and event.key == pygame.K_s):
                    st = time.time()
                    if(alg_select==1):#BFS
                        if(BFS(current_puzzle,board)):
                            ai_found_sol = True
                    if(alg_select==2):#DFS
                        if(DFS(current_puzzle,board)):
                            ai_found_sol = True
                    if(alg_select==3):#Iterative
                        if(Iterative(current_puzzle,board,4)):
                            ai_found_sol = True
                    if(alg_select==4):#Greedy
                        if(Greedy(current_puzzle,board,score_heuristic)):
                            ai_found_sol = True
                    if(ai_found_sol):
                        create_text_rect("Puzzle completed!",WIDTH/2,HEIGHT/2)
                        time.sleep(3)
                        alg_select = 0
                    else:
                        create_text_rect("Failed!",WIDTH/2,HEIGHT/2)
                        time.sleep(3)
                        alg_select = 0
                    et = time.time()
                    print("Elapsed time: ",et-st,"s")
                    main_screen()
                    print_mode(mode_select)
                    started_game=False
                    ai_found_sol = False
                print(alg_select)
                    
                   

            if (event.type == pygame.KEYDOWN and started_game and (event.key == pygame.K_ESCAPE)): #Already in a game it will back out to the main menu if ESC is pressed
                board = Board(0)
                main_screen()
                print_mode(mode_select)
                started_game=False 

            if (event.type == pygame.KEYDOWN and not(started_game) and (event.key == pygame.K_ESCAPE)): # When in the menu the "ESC" key, quits the game
                pygame.quit()

        pygame.display.update()

    pygame.quit()

main()