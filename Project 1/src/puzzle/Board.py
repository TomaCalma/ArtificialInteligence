import pygame
import numpy as np
from .constants import BLACK,WHITE,GREY,RED,GREEN,BLUE,WIDTH,HEIGHT,SHAPE_RATIO

class Board:
    def __init__(self, size): #Constructor for the board
        self.size = size#Width/Height of the board
        self.board_matrix = np.reshape(np.zeros(size*size),(size,size)) #initializes the board as a matrix of 0s
        self.score = 0 #Score of the board
        self.depth = 0 #Depth for tree porpuses

    def update_depth(self,board): #Board depth updates
        board.depth+=1
    
    def draw_background(self,win,size): #Draws the square background for the board
        win.fill(BLACK)
        square_size = WIDTH/size
        for row in range (size):
            for col in range(row % 2, size, 2):
                pygame.draw.rect(win,GREY,(row*square_size,col*square_size,square_size,square_size))
    
    def get_current_square(self,board,pos): #Used to get the square located in the given position
        shape_size = WIDTH/board.size
        x,y = pos
        c1 = int(y / shape_size)
        c2 = int(x / shape_size)
        #print("I'm in square ","[",c1,"]","[",c2,"]")
        return c1,c2

    def update_display(self,win,board): #Updates all the visual shapes present in the board
        shape_size = WIDTH/board.size
        for x in range (board.size):
            for y in range (board.size):
                if (board.board_matrix[x][y]=="Q" or board.board_matrix[x][y]=="q"):
                    rect = pygame.Rect(y*shape_size,x*shape_size,shape_size*SHAPE_RATIO,shape_size*SHAPE_RATIO)
                    rect.center = (y*shape_size+shape_size/2,x*shape_size+shape_size/2)
                    pygame.draw.rect(win,RED,rect)
                elif (board.board_matrix[x][y]=="C" or board.board_matrix[x][y]=="c"):
                    pygame.draw.circle(win,BLUE,(y*shape_size+shape_size/2,x*shape_size+shape_size/2),shape_size-shape_size*0.6)
                elif(board.board_matrix[x][y]=="T" or board.board_matrix[x][y]=="t"):
                    pygame.draw.polygon(win, GREEN, ((y*shape_size+shape_size/2,x*shape_size+20),(y*shape_size+20,x*shape_size+shape_size-20),(y*shape_size+shape_size-20,x*shape_size+shape_size-20)))

    def update_shape(self,board,x,y,shape): #Used for AI, can update to any desired shape
        if(shape=="q"):
            board.board_matrix[x][y] = "q"
        elif(shape=="c"):
            board.board_matrix[x][y] = "c"
        elif(shape=="t"):
            board.board_matrix[x][y] = "t"
        elif(shape==" "):
            board.board_matrix[x][y] = " "
        else:
            print("Invalid shape")
    
    def update_next_shape(self,board,pos):   # Used for singleplayer, iterates over the different shapes available for the current square
        x,y = board.get_current_square(board,pos)
        string = board.board_matrix[x][y]
        #print("Mouse position: ",pos)
        if(string==" "):
            board.board_matrix[x][y] = "q"
        elif(string == "q" and string.islower()):
            board.board_matrix[x][y] = "c"
        elif(string == "c" and string.islower()):
            board.board_matrix[x][y] = "t"
        elif(string == "t" and string.islower()):
            board.board_matrix[x][y] = " "

    def get_updated_score(self,board): #Gets an updated value of the score, +1 if a row/column is a palyndrome
        score = 0
        rows = board.size
        cols = board.size
        #is_palindrome = False

        # Check rows
        for i in range(rows):
            row = [elem.upper() for elem in board.board_matrix[i] if elem.upper() != " "]
            reverse_row = row[::-1]
            #print(row)
            if(row == reverse_row):
                score+=1

        # Check columns
        for j in range(cols):
            column = [board.board_matrix[i][j].upper() for i in range(rows) if board.board_matrix[i][j].upper() != " "]
            reverse_column = column[::-1]
            #print(column)
            if(column == reverse_column):
                score+=1

        return score

    def update_score(self,board): #Basic call to the update score function
        board.score = board.get_updated_score(board)
    