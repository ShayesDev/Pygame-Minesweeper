import pygame, sys, os

sys.path.append(os.path.dirname(__file__))

import config as cfg
import random
from cell import Cell
from button import Button

pygame.init()

class Game:
    def __init__(self,screen):
        # constructor that creates a Game object
        # this object contains the core logic behind the game, and is created
        # and updated in main.py
        self.screen = screen
        self.cells = []
        self.reset_button = Button((410,10),self.screen,30,"Restart",self.new_game,
                                   fill_color=pygame.Color(140,140,140),
                                   click_color=pygame.Color(127,127,127),
                                   custom_font=cfg.data_path + "8-bit pusab.ttf")
        self.text_image = pygame.Surface((0,0))

        # loops to create the cells in a 2d list, which is self.cells
        x,y = 0,80
        for i in range(cfg.board_h):
            cell_row = []
            for i in range(cfg.board_w):
                cell_row.append(Cell(self.screen,(x,y)))
                x += cfg.cell_size
            y += cfg.cell_size
            x = 0
            self.cells.append(cell_row)

        # loop to choose the cells that are miness
        chosen = []
        while len(chosen) != cfg.mine_amount:
            row = random.choice(self.cells)
            cell = random.choice(row)
            if not cell in chosen:
                cell.mine = True
                chosen.append(cell)

        # loops through all cells to count nearby mines
        for row in self.cells:
            for cell in row:
                cell.count_mines(self.cells)

    def new_game(self):
        self.__init__(self.screen)

    def message(self,message):
        # method that sets the message of self.text_image
        # currently just to display lose/win messages
        self.font = pygame.font.Font(cfg.data_path + "8-bit pusab.ttf",40)
        self.text_image = self.font.render(message,True,pygame.Color("black"))
        self.text_image.set_colorkey(pygame.Color("white"))

    def handle_event(self,event):
        # method that handles events passed in from the event loop in main.py
        
        correct_flags = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for row in self.cells:
                    for cell in row:
                        # check if cell is left clicked, revealing is handled in
                        # the cell itself if it is clicked
                        
                        # check_lclick returns True if cell is a mine
                        hit_mine = cell.check_lclick(event.pos)

                        # take action if a mine is hit
                        if hit_mine:
                            self.message("You lose!")
                            for row in self.cells:
                                for cell in row:
                                    cell.reveal()
            
            elif event.button == 3:
                for row in self.cells:
                    for cell in row:
                        # check if cell is right clicked, setting a flag is
                        # handled by the cell itself if it is clicked
                        cell.check_rclick(event.pos)
                        if cell.mine and cell.flag:
                            correct_flags += 1
                        if correct_flags == cfg.mine_amount:
                            self.message("You win!")

            self.reset_button.handle_event(event)

    def update(self):
        # dummy method right now, don't really need it in the case of this
        # game's current layout
        # some code from draw() should probably be here instead
        pass
        
    def draw(self):
        # method that draws the game
        for row in self.cells:
            for cell in row:
                cell.draw()
        self.reset_button.draw()
        self.screen.blit(self.text_image,(10,10))
