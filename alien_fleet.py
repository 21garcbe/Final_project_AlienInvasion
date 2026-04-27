import pygame
import random
from alien import Alien
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
        """Create the fleet structure of alien instances based on randomized formation pattern choice
        
        Args:
            pattern (string): The formation type name (i.e "rectangle", "triangle, or "m_shape") 
        """
        alien_width = self.settings.alien_width
        alien_height = self.settings.alien_height
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height

        #calculate sizes for fleet width and height
        fleet_width, fleet_height = self.calculate_fleet_size(alien_width, screen_width, alien_height, screen_height)
        #calculate x and y offsets
        x_offset, y_offset = self.calculate_offsets(alien_width, alien_height, screen_width, fleet_width, fleet_height)
        
        #check passed pattern string and call the appropriate fleet generation function
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
            spread_bound = max(1, fleet_height - row -1) 
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
        """Creat "m" shaped formation with a row at the top of the screen and 3 columns fit to screen size """
        top_row = 1
        center_col = fleet_width // 2
        left_col = fleet_width // 4
        right_col = (3 * fleet_width) //4

        for row in range(fleet_height):
            for column in range(fleet_width):
               
                #set flag to false by default
                place_alien = False

                #if on one of the columns, place
                if column == left_col or column == center_col or column == right_col:
                    place_alien = True
                
                #if on top row, place
                if row == top_row and left_col <= column <= right_col:
                    place_alien = True
                
                if not place_alien:
                    continue

                current_x = alien_width * column + x_offset
                current_y = alien_height * row + y_offset
                self._create_alien(current_x, current_y)
            

        


    def calculate_offsets(self, alien_width, alien_height, screen_width, fleet_width, fleet_height):
        """Calculate horizontal and vertical offsets to center the fleet on screen
        Positions the fleet horizontally across full screen width and vertically within top half of screen

        returns:
          the x_offset and y_offset used to position each fleet
        """
        half_screen = self.settings.screen_height // 2
        fleet_vertical_space = fleet_height * alien_height
        fleet_horizontal_space = fleet_width * alien_width
        x_offset = int((screen_width - fleet_horizontal_space) // 2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset



    def calculate_fleet_size(self, alien_width, screen_width, alien_height, screen_height):
        """Determine the number of aliens that fit horizontally and vertically within screen width and 
        the upper half of the screen
        """
        fleet_width = (screen_width // alien_width)
        fleet_height = ((screen_height/2) // alien_height)

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
        """Create an alien and place it in the fleet. Calls _is_tough_alien to determine alien type"""
       
        tough = self._is_tough_alien()
        new_alien = Alien(self, current_x, current_y, tough = tough)
        self.fleet.add(new_alien)

    def _is_tough_alien(self):
        """Randomly determines whether each newly spawned alien should be tough or not (set to 20% chance)"""
        return random.random() < 0.20
    
    def _check_fleet_edges(self):
        """Check if any alien in the fleet has hit the left or right edge of the screen
        if an edge is hit calls _drop_alien_fleet to drop the aliens down and then reverses fleet direction
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
    
    def _drop_alien_fleet(self):
        """Moves the entire fleet down by configured drop speed in settings"""
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def draw_fleet(self):
        """Draw the fleet of aliens to the screen."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()
    
    def update_fleet(self):
        """Update fleet position each frame, calls _check_fleet_edges to apply movement"""
        self._check_fleet_edges()
        self.fleet.update()

    def check_collisions(self, other_group):
        """Check for collisions between alien in fleet and bullets.
        
        looks for collisions and removes aliens if their hit points are 0
        """
        collisions = pygame.sprite.groupcollide(self.fleet, other_group, False, True)

        for alien, bullets in collisions.items():
            alien.hit_points -= len(bullets)

            if alien.hit_points <= 0:
                alien.kill()

        return collisions
    
    def check_fleet_bottom(self):
        """Check if any alien has reached the bottom of the screen
        returns true if bottom has been hit and false otherwise
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_height:
                return True
        return False
    
    def check_destroyed_status(self):
        """Determine whether the fleet has been completely destroyed
        returns True if no aliens remain in fleet
        """
        return not self.fleet

        