import pygame
from typing import TYPE_CHECKING
from pygame.sprite import Sprite
import random

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship(Sprite):
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
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))
        
        #collision rectangle (hitbox) for ship
        self.rect = self.image.get_rect()

        #implemented random starting position for ship
        #calculates random x pos within boundaries and sets y to bottom of screen
        self.rect.x = random.randint(0, self.boundaries.width - self.rect.width)
        self.rect.bottom = self.boundaries.bottom
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)

        #horizontal movement flags
        self.moving_right = False
        self.moving_left = False
        
        self.arsenal = arsenal

        #vertical movement flags
        self.moving_up = False
        self.moving_down = False

        
        

        #define top movement boundary (halfway up screen)
        self.top_limit = self.boundaries.height // 2

        #initialize angle, rotation movement flags, turn speed, and original ship sprite for rotation
        self.original_image = pygame.image.load(self.settings.ship_file)
        self.original_image = pygame.transform.scale(self.original_image, (self.settings.ship_width, self.settings.ship_height))

        #start with no rotation (facing up)
        self.angle = 0
        self.image = self.original_image

        #rotation movement flags
        self.rotating_left = False
        self.rotating_right = False
        #turn speed (degrees per frame)
        self.rotation_speed = 5

        #return speed for ship to smoothly rotate back to center when not rotating
        self.return_speed = 2.5

    def _center_ship(self):
        """Reposition the ship to the bottom center of screen ONLY after a collision or other level reset condition"""
        self.rect.midbottom = self.boundaries.midbottom
        self.x_pos = float(self.rect.x)

    def update(self):
        """Update ships position based on movement flags for current frame"""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Update the ship's position and rotation based on movement flags.
        
        handles all movements within boundaries and rotation behavior/returning to neutral orientation
        """

        temp_speed = self.settings.ship_speed
        #if movement flag is true and ship is within boundaries, move
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x_pos += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x_pos -= temp_speed

        
        # Vertical movement
        # Move up (but stop at halfway point)
        if self.moving_up and self.rect.top > self.top_limit:
            self.y_pos -= temp_speed

        # Move down (but stop at bottom of screen)
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y_pos += temp_speed

        #update hitbox position based on ship movement (x and y positions)
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

        #rotation logic
        if self.rotating_left and not self.rotating_right:
            self.angle += self.rotation_speed
        elif self.rotating_right and not self.rotating_left:
            self.angle -= self.rotation_speed
        else:
            #when not rotating, drift back to 0 (straight up)
            if self.angle > 0:
                self.angle -= self.return_speed
            elif self.angle < 0:
                self.angle += self.return_speed
                

        #limit rotation 
        self.angle = max(-30, min(30, self.angle))

       

        #rotate the original image by the current angle to get the new image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        #update hitbox to match new rotated image
        self.rect = self.image.get_rect(center=self.rect.center)

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
    
    def check_collisions(self, other_group):
        if pygame.sprite.spritecollideany(self,other_group):
            self._center_ship()
            return True
        return False