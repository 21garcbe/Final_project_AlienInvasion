import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """"Intialize game and all core components
        
        Sets Up: 
            - Pygame
            - Game Settings
            - Screen display
            - Background image
            - Game loop control
            - Frame rate control(game clock)
            - Ship
            - Sound effects
        """
        pygame.init()
        self.settings = Settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)


        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)


        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))

        self.running = True
        #set up timer to control frame rate
        self.clock = pygame.time.Clock()
        #set up ship
        self.ship = Ship(self, Arsenal(self))

        #create fleet of aliens
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

        #set game active flag to True
        self.game_active = True

        #set up sound effects
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        #impact sound
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

    def run_game(self):
        """Start the main game loop
        
        processes user input, updates game state,
        """
        while self.running:
            #call event listener function
            self._check_events()
            if self.game_active:
                #update ship position based on movement flags
                self.ship.update()
                #update alien fleet 
                self.alien_fleet.update_fleet()
                #update collision checks
                self._check_collisions()
            #call update screen function
            self._update_screen() 
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        """Check collisions between ship and aliens, aliens vs bottom of screen, bullets and aliens"""

        #ship collisions
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            #subtract a life
        #check collisions at bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()



        #check bullet and alien collision
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
        

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()

    
    def _check_game_status(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
        else: 
            self.game_active = False

        
    
    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
    

    def _update_screen(self):
        """Render the current frame to the display.

        Draws the background image, renders the ship, and updates the display
        using double buffering to present the latest frame.
        """
        #draw background image to screen
        self.screen.blit(self.bg, (0, 0))
        #draw ship to screen and update display    
        self.ship.draw()
        #call draw fleet function from alien_fleet to draw aliens to screen
        self.alien_fleet.draw_fleet()
        pygame.display.flip()

    def _check_events(self):
        """Listener function Respond to keypresses and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit() # Limit to 60 FPS

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """Responds to keypresses for movement and firing actions."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                #play laser sound effect when firing
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
                

        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()
            
    def _check_keyup_events(self, event):
        """Responds to key releases. Stopping movement when arrow keys are released."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    
