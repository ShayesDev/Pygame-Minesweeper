import pygame, os
from pygame import Color, Rect

pygame.init()

"""
========================================================================

A module for creating buttons in Pygame

========================================================================

Required parameters for creating a button:
    topleft: The top left position of the button
    
    surface: The surface that the button is drawn on
    
    size: The size of the prompt font
    
    prompt: The message that is displayed on the button
    
    callback: The function that is called when the button is clicked

Optional parameters:
    fill_color: The color of the button
    
    click_color: The color of the button when the button is clicked
    
    text_color: The color of the text on the button
    
    border_color: The color of the border on the button
    
    font: The system font that is used for the text
    
    custom_font: Replaces font using your own font file
    
    center: Positions the button's center at the given point rather than
    the topleft.

========================================================================

handle_event() function:
    Checks an event to see if it is left mouse button down. If so, check
    to see if the button was clicked. This should called with each event
    from the event loop.
    
update() function:
    Dummy function as of now, mostly for my own personal purposes
    because of how I arrange my code. Some code from draw() could be
    put in there, but makes more sense to me for it to be in draw().

draw() function:
    Changes the button color if clicked, and draws the button to
    self.surface.

========================================================================
"""

class Button:
    def __init__(self,topleft,surface,size,prompt,callback,fill_color=Color("white"),
                 click_color=Color(210,210,210),text_color=Color("black"),
                 border_color=Color("black"),font="Verdana",custom_font=None,
                 center=None):
        
        self.callback = callback
        self.clicked = False
        
        if not custom_font:
            self.font = pygame.font.SysFont(font,size)
        else:
            self.font = pygame.font.Font(custom_font,size)
            
        self.text_image = self.font.render(prompt,True,text_color)
        self.text_image_size = self.text_image.get_size()
        self.text_rect = self.text_image.get_rect()

        self.fill_color,self.click_color = fill_color,click_color
        self.border_color = border_color
        
        self.orig_freq = 1
        self.freq = self.orig_freq
        
        self.image = pygame.Surface((self.text_image_size[0] + 16,self.text_image_size[1] + 10)).convert_alpha()
        self.rect = self.image.get_rect()
        self.text_rect.center = self.rect.center
        
        self.rect = self.image.get_rect()
        
        if not center:
            self.rect.topleft = topleft
        else:
            self.rect.center = center
        
        self.surface = surface

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True

    def update(self):
        pass
            
    def draw(self):
        if self.clicked and self.freq:
            self.image.fill(self.click_color)
            self.freq -= 1
        elif self.clicked and not self.freq:
            self.clicked = False
            self.callback()
        else:
            self.image.fill(self.fill_color)
            self.clicked = False
            self.freq = self.orig_freq

        self.image.blit(self.text_image,self.text_rect)
        pygame.draw.rect(self.image,self.border_color,
                         Rect(0,0,self.text_image_size[0] + 16,self.text_image_size[1] + 10),3)
        self.surface.blit(self.image,self.rect)
