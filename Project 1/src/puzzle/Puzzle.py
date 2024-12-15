import pygame
import numpy as np
import math

class Puzzle:
    def __init__(self,initial_puzzle,puzzle_solution):
        self.size = len(initial_puzzle) #Length of the array representing the initial puzzle
        self.initial_puzzle = initial_puzzle #Array with the initial puzzle
        self.puzzle_solution = np.reshape(puzzle_solution,(int(math.sqrt(len(initial_puzzle))),int(math.sqrt(len(initial_puzzle))))) #Matrix of the puzzle solution