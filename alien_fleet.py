import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    
class AlienFleet:
    """A class to manage the fleet of aliens."""
    
    def __init__(self, game: 'AlienInvasion'):
        """Initialize the fleet and set its starting position."""
        
        self.game = game
        self.fleet = pygame.sprite.Group()
        self.settings = game.settings
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        #temp create fleet of aliens
        self.create_fleet()
    
    def create_fleet(self):
        """Create the fleet structure of alien instances"""
        alien_width = self.settings.alien_width
        screen_width = self.settings.screen_width


        fleet_width = self.calculate_fleet_size(alien_width, screen_width)

        half_screen = self.settings.screen_width // 2
        fleet_horizontal_space = fleet_width * alien_width
        x_offset = int((screen_width - fleet_horizontal_space) // 2)

        #positioning each alien individually, starting at x_offset
        for column in range(fleet_width):
            if column % 2 == 0:
                continue
            current_x = alien_width * column + x_offset
            self._create_alien(current_x, 10)



    def calculate_fleet_size(self, alien_width, screen_width):
        fleet_width = (screen_width // alien_width)

        # allow for centered alien
        if fleet_width % 2 == 0:
            fleet_width -= 1
        else:
            fleet_width -= 2

        return fleet_width
        
    def _create_alien(self, current_x: int, current_y: int):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def draw_fleet(self):
        """Draw the fleet of aliens to the screen."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    

        