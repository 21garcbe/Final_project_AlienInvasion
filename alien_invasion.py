import sys
import pygame
import random
from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from button import Button
from store_menu import StoreMenu

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

        #how quickly game speeds up
        self.speedup_scale = 1.1

        self.settings.initialize_dynamic_settings()
        self.game_stats = GameStats(self)


        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)

        #Create Scoreboard instance tot store game stats
        self.scoreboard = ScoreBoard(self)


        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))

        self.running = True
        #set up timer to control frame rate
        self.clock = pygame.time.Clock()
        #set up ship
        self.ship = Ship(self, Arsenal(self))

        #create fleet of aliens
        self.alien_fleet = AlienFleet(self)
        #self.alien_fleet.create_fleet()

        #set up play button 
        self.play_button = Button(self, "Play")

        #set game active flag to False
        self.game_active = False

        #set up sound effects
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        #set up impact sound
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        #set up store menu
        self.store_menu = StoreMenu(self)
        self.store_active = False

    def run_game(self):
        """Start the main game loop
        
        processes user input, updates game state,
        """
        while self.running:
            #call event listener function
            self._check_events()
            if self.game_active and not self.store_active:
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
            self.game_stats.update(collisions)
            self.scoreboard.prep_score()
            self.scoreboard.prep_hi_score()
            self.scoreboard.prep_credits()

            
        
        #check for alien fleet destroyed to reset
        if self.alien_fleet.check_destroyed_status():
            self._advance_level()
            self._set_current_level_pattern()
            self._spawn_current_level()

    
    def _advance_level(self):
        """When called increments level number in game stats
            and resets object instances on level 
         """
        self.game_stats.level += 1
        
    def _spawn_current_level(self):
        """when called resets players arsenal and alien fleet, and recenters the ship"""
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet(self.game_stats.current_pattern)
        self.ship._center_ship()

    def _set_current_level_pattern(self):
        """sets the fleet formation pattern for the current level by random choice
        
        when starting the game (level == 1) fleet will always be a rectangle, otherwise 
        it makes a random choice between the 3 possible formations and sets that pattern in
        game_stats.py
        """
        if self.game_stats.level ==1:
            self.game_stats.current_pattern = "rectangle"
        else:
            self.game_stats.current_pattern = random.choice(["rectangle","triangle","m_shape"])
            self.settings.increase_speed()
            #update game stats level
            self.game_stats.update_level()
            #update HUD displayed level
            self.scoreboard.prep_level()
        

    def _check_game_status(self):
        """checks for player lives left and decides to reset if player has lives
          or "pause" (freeze by flagging game_active = False)"""
        
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            #update ship count on HUD
            self.scoreboard.prep_ships()
            self._reset_level()
        else: 
            self.game_active = False

        
    
    def _reset_level(self):
        """resets current level without advancing. resets current instances of ships aresenal and fleet
        while preserving the levels chosen fleet shape
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet(self.game_stats.current_pattern)
    
    def restart_game(self):
        #setting up dynamic settings
        self.settings.initialize_dynamic_settings()
        #reset game stats
        self.game_stats.reset_stats()

        # update HUD scores and lives
        self.scoreboard.prep_score()
        self.scoreboard.prep_hi_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

        #reset level
        self._reset_level()
        #recenter ship
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)
        
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
        #Draw HUD
        self.scoreboard.show_score()

        #draw store menu if active
        if self.store_active:
            self.store_menu.draw()

        #draw play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        """Listener function Respond to keypresses and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit() 

            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

                    
    
    def _check_keydown_events(self, event):
        """Responds to keypresses for movement and firing actions.(arrowkeys or WASD)
        Checks for roational movements with "q" and "a" key
        """
        if event.key == pygame.K_m and self.game_active:
            self.store_active = not self.store_active
            return
        if self.store_active:
            return
        #Horizontal movement flags
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        #Vertical movement flags
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        #Rotational movement flags
        elif event.key == pygame.K_q:
            self.ship.rotating_left = True
        elif event.key == pygame.K_e:
            self.ship.rotating_right = True
        elif event.key == pygame.K_SPACE:
            if self.game_stats.machine_gun_unlocked:
                self.ship.firing_machine_gun = True
            else:
                if self.ship.fire():
                    #play laser sound effect when firing
                    self.laser_sound.play()
                    self.laser_sound.fadeout(250)
                

        elif event.key == pygame.K_ESCAPE:
            self.running = False
            pygame.quit()
            sys.exit()

        

    def _check_keyup_events(self, event):
        """Responds to key releases (arrowkeys or WASD). Stopping movement when arrow keys are released. 
        Checks for roational movements with "q" and "a" key """
        #Horizontal movement flags
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

        #Vertical movement flags
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

        #Rotational movement flags
        elif event.key == pygame.K_q:
            self.ship.rotating_left = False
        elif event.key == pygame.K_e:
            self.ship.rotating_right = False

        #machine gun firing flag
        elif event.key == pygame.K_SPACE:     
            self.ship.firing_machine_gun = False

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    
