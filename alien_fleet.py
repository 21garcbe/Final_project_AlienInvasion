import pygame
from alien import Alien
from game_stats import GameStats
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    
class AlienFleet:
    """A class to manage the fleet of aliens."""
    
    def __init__(self, game: 'AlienInvasion'):
        """Initializes the fleet, sets its starting position, and
        asks for current fleet formation pattern from game_stats"""
        
        self.game = game
        self.fleet = pygame.sprite.Group()
        self.settings = game.settings
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        
        #create fleet of aliens based on current pattern
        self.create_fleet(self.game.game_stats.current_pattern)
    
    def create_fleet(self, pattern):
        """Create the fleet structure of alien instances"""
        alien_width = self.settings.alien_width
        alien_height = self.settings.alien_height
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height

        #calculate sizes for fleet width and height
        fleet_width, fleet_height = self.calculate_fleet_size(alien_width, screen_width, alien_height, screen_height)
        #calculate x and y offsets
        x_offset, y_offset = self.calculate_offsets(alien_width, alien_height, screen_width, fleet_width, fleet_height)
        
        #figure out which
        if pattern == "rectangle":
            self.create_fleet_rectangle(
                alien_width, alien_height, fleet_width, fleet_height, x_offset, y_offset
            )
        elif pattern == "triangle":
            self.create_fleet_triangle(
                alien_width, alien_height, fleet_width, fleet_height, x_offset, y_offset
            )
        elif pattern == "m_shape":
            self.create_fleet_m_formation(
                alien_width, alien_height, fleet_width, fleet_height, x_offset, y_offset
            )

    def create_fleet_rectangle(self, alien_width, alien_height, fleet_width, fleet_height, x_offset, y_offset):
        """draws alien fleet by drawing each alien into rows and columns, taking into account x and y offset and spacing"""
        for row in range(fleet_height):
            for column in range(fleet_width):
                current_x = alien_width * column + x_offset
                current_y = alien_height * row + y_offset
                if column % 2 == 0 or row %2 ==0:
                    continue
                self._create_alien(current_x, current_y)

    def create_fleet_triangle(self, alien_width, alien_height, fleet_width, fleet_height, x_offset, y_offset):
        """draws alien fleet in a triangle shape by drawing each alien into rows and columns , taking into account x and y offet and spacing"""
        center_col = fleet_width // 2

        
        for row in range(fleet_height):
            spread_bound = max(1, (fleet_height - row -1) //2)
            left_bound = center_col - spread_bound
            right_bound = center_col + spread_bound
        
        for column in range(fleet_width):
            if column < left_bound or column > right_bound:
                continue

            if column % 2 ==0 or row %2 ==0:
                continue

            current_x = alien_width * column + x_offset
            current_y = alien_height * row + y_offset

            self._create_alien(current_x,current_y)
        
        

    def create_fleet_m_formation(self, alien_width, alien_height, fleet_width, fleet_height, x_offset, y_offset):
        pass


    def calculate_offsets(self, alien_width, alien_height, screen_width, fleet_width, fleet_height):
        half_screen = self.settings.screen_height // 2
        fleet_vertical_space = fleet_height * alien_height
        fleet_horizontal_space = fleet_width * alien_width
        x_offset = int((screen_width - fleet_horizontal_space) // 2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset



    def calculate_fleet_size(self, alien_width, screen_width, alien_height, screen_height):
        fleet_width = (screen_width // alien_width)
        fleet_height = ((screen_height/2) // alien_height)

        # allow for centered alien
        if fleet_width % 2 == 0:
            fleet_width -= 1
        else:
            fleet_width -= 2
        
        if fleet_height % 2 == 0:
            fleet_height -=1
        else:
            fleet_height -=2

        return int(fleet_width), int(fleet_height)
        
    def _create_alien(self, current_x: int, current_y: int):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
    
    def _drop_alien_fleet(self):
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def draw_fleet(self):
        """Draw the fleet of aliens to the screen."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()
    
    def update_fleet(self):
        self._check_fleet_edges()
        self.fleet.update()

    def check_collisions(self, other_group):
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self):
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_height:
                return True
        return False
    
    def check_destroyed_status(self):
        return not self.fleet

        