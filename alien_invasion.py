import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal

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


        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)


        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))

        self.running = True
        #set up timer to control frame rate
        self.clock = pygame.time.Clock()
        #set up ship
        self.ship = Ship(self, Arsenal(self))

        #set up sound effects
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)


    def run_game(self):
        """Start the main game loop
        
        processes user input, updates game state,
        """
        while self.running:
            #call event listener function
            self._check_events()
            #update ship position based on movement flags
            self.ship.update()
            #call update screen function
            self._update_screen() 
            self.clock.tick(self.settings.FPS)


    def _update_screen(self):
        """Render the current frame to the display.

        Draws the background image, renders the ship, and updates the display
        using double buffering to present the latest frame.
        """
        #draw background image to screen
        self.screen.blit(self.bg, (0, 0))
        #draw ship to screen and update display    
        self.ship.draw()
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
    
