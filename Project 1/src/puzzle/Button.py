import pygame
import numpy as np
import sys

class Button:
    def __init__(self,text,pos,font,color,feedback):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color
        self.feedback = feedback
