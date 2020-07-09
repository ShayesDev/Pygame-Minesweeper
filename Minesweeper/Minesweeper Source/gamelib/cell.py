import pygame, sys, os

sys.path.append(os.path.dirname(__file__))

import config as cfg

pygame.init()

ids_list = ["h","f","m","0","1","2","3","4","5","6","7","8"]
tex_ids = {ids_list[i] : i for i in range(len(ids_list))}

class Cell:
    def __init__(self,screen,pos):
        self.textures = self.load_textures(cfg.cell_size,cfg.data_path + "textures.jpg")
        self.screen = screen
        
        self.mine = False
        self.flag = False
        self.revealed = False
        
        self.mines = 0
        
        self.image = self.textures[tex_ids["h"]]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.index_x,self.index_y = pos[0]//cfg.cell_size,(pos[1] - 80)//cfg.cell_size

    def reveal(self):
        self.revealed = True
        self.flag = False
        if self.mine:
            self.image = self.textures[tex_ids["m"]]

        else:
            self.image = self.textures[tex_ids[str(self.mines)]]
            if not self.mines:
                self.zero_spread()

    def check_lclick(self,pos):
        if not self.flag:
            if self.rect.collidepoint(pos):
                self.reveal()
                if self.mine:
                    return True

    def check_rclick(self,pos):
        flag_count = 0
        if self.rect.collidepoint(pos):
            for row in self.cells:
                for cell in row:
                    if cell.flag:
                        flag_count += 1
                        
            if not self.revealed:
                if not flag_count == cfg.mine_amount or self.flag:
                    self.flag = not self.flag
                
                if self.flag:
                    self.image = self.textures[tex_ids["f"]]
                else:
                    self.image = self.textures[tex_ids["h"]]

    def zero_spread(self):
        x,y = self.index_x - 1,self.index_y - 1
        for i in range(3):
            for i in range(3):
                try:
                    if x >= 0 and y >= 0:
                        if not self.cells[y][x].revealed and not self.cells[y][x].mine:
                            self.cells[y][x].reveal()

                except:
                    pass
                x += 1
            y += 1
            x = x - 3

    def count_mines(self,cells):
        self.cells = cells
        x,y = self.index_x - 1,self.index_y - 1
        for i in range(3):
            for i in range(3):
                try:
                    if x >= 0 and y >= 0:
                        if cells[y][x].mine:
                            self.mines += 1
                except:
                    pass
                x += 1
            y += 1
            x = x - 3

    def load_textures(self,cell_size,image):
        textures = []
        image = pygame.image.load(image)
        image = image.convert()
        
        x,y = 0,0
        for i in range(image.get_height()//cell_size):
            for i in range(image.get_width()//cell_size):
                texture = pygame.Surface((cell_size,cell_size))
                texture.blit(image,(0,0),(x,y,cell_size,cell_size))
                textures.append(texture)

                x += cell_size
            y += cell_size
            x = 0

        return textures

    def draw(self):
        self.screen.blit(self.image,self.rect)
