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
        self.last_machine_gun_shot = 0


    def update_arsenal(self):
        """Update the position of all bullets in the arsenal.
        
        Calls the update mthod on each bullet and calls remove_offscreen_bullets
        for cleanup.
        """
        self.arsenal.update()
        self._remove_offscreen_bullets()
    
    def _remove_offscreen_bullets(self):
        """Remove bullets that have moved off the screen."""
        for bullet in self.arsenal.copy():
            #remove bullet if it has moved off any edges of the screen
            for bullet in self.arsenal.copy():
                if (bullet.rect.bottom < 0 or bullet.rect.top > self.settings.screen_height or
                    bullet.rect.right < 0 or bullet.rect.left > self.settings.screen_width):
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
    
    def fire_machine_gun(self):
        """Attempt to fire machine gun if under bullet limit and cooldown has passed."""
        if not self.game.game_stats.machine_gun_unlocked:
            return False
        
        now = pygame.time.get_ticks()
        #if cooldown has not passed yet, return false
        if now - self.last_machine_gun_shot < self.settings.machine_gun_fire_delay:
            return False
        #if bullet limit reached return false
        if len(self.arsenal) >= self.settings.machine_gun_bullet_limit:
            return False
        new_bullet = Bullet(self.game)
        self.arsenal.add(new_bullet)
        self.last_machine_gun_shot = now
        return True

