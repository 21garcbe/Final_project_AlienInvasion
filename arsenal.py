from typing import TYPE_CHECKING
import pygame
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion



class Arsenal:
    """A class to manage the arsenal of weapons.
    
    """
    
    def __init__(self, game: 'AlienInvasion'):
        """Initialize the ship's arsenal.
        Stores references to the game instance and settings.
        creates a sprite group to track acitve bullets
        """
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """Update the position of all bullets in the arsenal.
        
        Calls the update mthod on each bullet and calls remove_offscreen_bullets
        for cleanup.
        """
        self.arsenal.update()
        self._remove_offscreen_bullets()
    
    def _remove_offscreen_bullets(self):
        """Remove bullets that have moved off the top of the screen from the arsenal."""
        for bullet in self.arsenal.copy():
            #remove bullet if it has moved off the top of the screen
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self):
        """Draw all bullets fired from arsenal to the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()
    
    def fire_bullet(self):
        """Attempt to fire a bullet if under the limit set in settings.
        
        returns True if a bullet was fired, False otherwise.
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
    
        

