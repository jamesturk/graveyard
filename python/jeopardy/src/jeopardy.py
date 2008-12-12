#!/usr/bin/env python

import os, sys
import pygame
from pygame.locals import *
           
class Question:
    def __init__(self, q, a):
        self.q = q
        self.a = a
        
    def __str__(self):
        return "Q: %s\nA: %s" % (self.q, self.a)

BLACK = (0,0,0)
WHITE = (255,255,255)

GAMEBOARD = 'gameboard'
QUESTION = 'question'
ANSWER = 'answer'

class Jeopardy:
    qm = {}
    board = []
    mode = GAMEBOARD
    curQ = None
    
    def __init__(self, screen, questionFile, round=1):
        self.screen = screen
    
        # load fonts
        self.smallFont = pygame.font.Font(None, 48)
        self.bigFont = pygame.font.Font(None, 80)
        
        # load the questions
        self.loadQuestions(questionFile)
        
        # create gameboard
        self.board.append(self.qm.keys())
        for p in range(100, 501, 100):
            self.board.append([p*round]*6)

    def loadQuestions(self, filename):
        f = open(filename)
        lines = f.readlines()
        for line in lines:
             data = line.strip().split(':')
             self.addQuestion(*data)

    def addQuestion(self, category, points, q, a):
        if not category in self.qm.keys():
            self.qm[category] = {}
        self.qm[category][points] = Question(q,a)
        
    def mouseClick(self, pos):
        if self.mode == GAMEBOARD:
            self.askQuestion(pos[0]/133, pos[1]/100)
        elif self.mode == QUESTION:
            self.mode = ANSWER
        elif self.mode == ANSWER:
            self.mode = GAMEBOARD

    def askQuestion(self, col, row):
        q = None
        if row != 0:
            cat = self.board[0][col]
            points = str(self.board[row][col])
            if points != '':
                self.curQ = self.qm[cat][points]
                self.board[row][col] = ''
                self.mode = QUESTION
                
    def drawTextCentered(self, str, skiperoo=-75):
        choperoo = len(str)
        
        font = self.smallFont
        
        # draw string and see if it is too long
        text = font.render(str, 1, WHITE)
        
        # if string is too long, choperoo!
        while text.get_rect().width > self.screen.get_rect().width:
            for c in range(choperoo/2 , choperoo):
                if str[c] == ' ':
                    choperoo = c
                    break
            # redraw string
            text = font.render(str[:choperoo], 1, WHITE)
            
        # find the centered rect for the drawing
        cr = text.get_rect()
        cr.center = self.screen.get_rect().center
        cr.y += skiperoo
        # draw
        self.screen.blit(text, cr)
        
        if choperoo != len(str):
            self.drawTextCentered(str[choperoo:], skiperoo+cr.height)

    def draw(self):
        if self.mode == GAMEBOARD:
            self.drawBoard()
        elif self.mode == QUESTION:
            self.drawTextCentered(self.curQ.q)
        elif self.mode == ANSWER:
            self.drawTextCentered(self.curQ.a)

    def drawBoard(self):
        xStart,xEnd = 0, 800
        yStart,yEnd = 0, 600
        xStep = xEnd/6
        yStep = yEnd/6

        # draw the grid
        for x in range(xStart, xEnd+1, xStep):
            pygame.draw.line(self.screen, BLACK, (x,yStart), (x,yEnd), 5)
        for y in range(yStart, yEnd+1, yStep):
            pygame.draw.line(self.screen, BLACK, (xStart,y), (xEnd,y), 5)

        # draw the labels
        for x in range(0, 6):
            text = self.smallFont.render(self.board[0][x], 1, WHITE)
            self.screen.blit(text, (x*xStep+10,25))
            for y in range(1, 6):
                text = self.bigFont.render(str(self.board[y][x]), 1, WHITE)
                self.screen.blit(text, (x*xStep+7,y*yStep+10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Jeopardy')
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 200))
    pygame.display.flip()
    #allsprites = pygame.sprite.renderPlain((fist, chimp))
    clock = pygame.time.Clock()

    # round 1
    #jeopardy = Jeopardy(screen, 'round1.jeopardy')
    
    # round 2
    jeopardy = Jeopardy(screen, 'round2.jeopardy', 2)

    quit = False
    while not quit:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit = True
            elif event.type == MOUSEBUTTONDOWN:
                jeopardy.mouseClick(pygame.mouse.get_pos())
        screen.blit(background, (0, 0))
        jeopardy.draw()
        pygame.display.flip()

if __name__ == '__main__':
    main()