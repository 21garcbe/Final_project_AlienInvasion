import pygame
from typing import TYPE_CHECKING
from pygame.sprite import Sprite
import math

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """Represents a projectile fired from the player's ship.

    Each bullet maintains its own position, movement behavior, and
    rendering logic. Bullets travel upward from the ship and are
    updated each frame until removed from the game.
    """
    def __init__(self, game: 'AlienInvasion'):
        """Initialize a bullet object at the ship's current position."""
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))
        #bullet rotation logic
        self.angle = game.ship.angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        
        #Added xpos to angle sprite starting angle based on ship angle
        self.x_pos =float(self.rect.x)
        self.y_pos = float(self.rect.y)

        #TODO: Calculate bullet trajectory based on ships angle
        angle_rad = math.radians(self.angle)
        self.x_velocity = -math.sin(angle_rad) * self.settings.bullet_speed
        self.y_velocity = math.cos(angle_rad) * self.settings.bullet_speed
    def update(self):
        """Update bullets position to move it up the screen based on speed settings."""
        self.x_pos += self.x_velocity
        self.y_pos -= self.y_velocity
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def draw_bullet(self):
        """Draw the bullet sprite and hitbox to the screen."""
        self.screen.blit(self.image, self.rect)





