import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Initialize the alien and set its starting position."""
        
        super().__init__()

        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_width, self.settings.alien_height))
        
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = x
        self.rect.y = y

       #Store aliens position
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
    
    def update(self):
        temp_speed = self.settings.fleet_speed
        #check edges and change direction (in settings)
        if self.check_edges():
            self.settings.fleet_direction *= -1
            self.y += self.settings.fleet_drop_speed
            

        self.x += temp_speed * self.settings.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_alien(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Check if alien is at edge of screen. Returns True if at edge, False otherwise."""
        return(self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)
