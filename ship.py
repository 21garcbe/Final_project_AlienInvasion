import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """Represent the players ship.

    Manages the ships position, movement, rendering, and interaction
    with its arsenal. The ship can move horizontally within screen
    boundaries and fire bullets.
    """

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """Initialize the ship and set its starting position.
        
        Loads and scales the ship image, sets up hitbox, associates arsenal 
        for firing bullets, and initializes movement flags.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))
        
        #collision rectangle (hitbox) for ship
        self.rect = self.image.get_rect()
        #draw ship at bottom center of screen
        self.rect.midbottom = self.boundaries.midbottom

        #movement flags
        self.moving_right = False
        self.moving_left = False
        self.x_pos = float(self.rect.x)
        self.arsenal = arsenal

    def update(self):
        """Update ships position based on movement flags for current frame"""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Update the ship's position based on movement flags."""

        temp_speed = self.settings.ship_speed
        #if movement flag is true and ship is within boundaries, move
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x_pos += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x_pos -= temp_speed

        #update hitbox position based on ship movement
        self.rect.x = self.x_pos


    def draw(self):
        """Draw the ship and its arsenal to the screen.
        draws all active bullets and renders ship at current position.
        """
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
    
    def fire(self):
        """Attempt to fire a bullet from the ship's arsenal.
        
        calls the fire_bullet method from arsenal class and return the result
        """
        return self.arsenal.fire_bullet()