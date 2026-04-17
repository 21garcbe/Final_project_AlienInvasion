import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, game: 'AlienInvasion', x: float, y: float):
        """Initialize the alien and set its starting position."""
        
        super().__init__()

        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_width, self.settings.alien_height))
        
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = x
        self.rect.y = y

       
        #self.y = float(self.rect.y)
    
    def update(self):
        pass

    def draw_alien(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)