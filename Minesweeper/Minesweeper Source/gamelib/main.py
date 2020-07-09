import pygame
import sys, os

sys.path.append(os.path.dirname(__file__))
                
import config as cfg
from game import Game

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

def main():
    gray = pygame.Color(192,192,192)

    frame_delay = 10      # time between frames in milliseconds

    # set up the screen
    screensize = screenwidth,screenheight = 640,720
    screen = pygame.display.set_mode(screensize)

    icon = pygame.image.load(cfg.data_path + "icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Minesweeper")

    game = Game(screen)

    # main animation loop
    while True:
        # event loop
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pygame.image.save(screen,"sweep.png")
            else:
                game.handle_event(event)

        screen.fill(gray)
        
        game.draw()

        pygame.display.flip()

if __name__ == "__main__":
    main()
