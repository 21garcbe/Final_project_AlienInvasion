import sys
import pygame
from settings import Settings

class AlienInvasion:
    
    def __init__(self):
        """"Intialize game and draw screen"""
        pygame.init()
        self.settings = Settings()


        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)


        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))

        self.running = True
        #set up timer to control frame rate
        self.clock = pygame.time.Clock()

    def run_game(self):
        #Game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            self.screen.blit(self.bg, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.settings.FPS)  # Limit to 60 FPS


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    
