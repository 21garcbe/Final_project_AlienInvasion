import pygame
from typing import TYPE_CHECKING
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """Represent a projectile fired from the player's ship.

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
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y_pos = float(self.rect.y)
    
    def update(self):
        """Update bullets position to move it up the screen based on speed settings."""
        self.y_pos -= self.settings.bullet_speed
        self.rect.y = self.y_pos

    def draw_bullet(self):
        """Draw the bullet sprite and hitbox to the screen."""
        self.screen.blit(self.image, self.rect)