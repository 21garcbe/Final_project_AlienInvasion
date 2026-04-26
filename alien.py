import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """A class to represent a single alien in the fleet.
    
    Each alien object manages its own position, movement, collisions and rendering. Aliens can be 
    classified as tough with increased hitpoints
    """
    
    def __init__(self, fleet: 'AlienFleet', x: float, y: float, tough: bool = False):
        """Initialize the alien and set its starting position."""
        
        super().__init__()
        
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(self.settings.alien_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.settings.alien_width, self.settings.alien_height))
        
       
        self.is_tough = tough
        self.hit_points = 1 

        if self.is_tough:
            self.hit_points = 2
            self.image = self.image.copy()
            self.image.fill((183,21,242), special_flags = pygame.BLEND_RGB_ADD)


        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = x
        self.rect.y = y

        #Store aliens position
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
    
    def update(self):
        """update the aliens position for the current frame
        
        Moves the alien horizontally based on fleet direction and speed
        """
        temp_speed = self.settings.fleet_speed

        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_alien(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Check if alien is at edge of screen. Returns True if at edge, False otherwise."""
        return(self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)
