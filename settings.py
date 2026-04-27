from pathlib import Path

class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize game settings."""
        
        self.name: str = "Alien Invasion"

        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.FPS = 60
        #set background image file path
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        #set ship image file path + settings
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_width = 40
        self.ship_height = 60
        
        
        #set bullet image filepath + settings
        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        
       

        #Alien settings
        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
       
        self.alien_width = 25
        self.alien_height = 25
        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        

        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 135, 50)

        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'fonts' / 'Silkscreen' / "Silkscreen-Bold.ttf"
    
    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_speed = 7
        self.bullet_amount = 5
        self.bullet_width = 25
        self.bullet_height = 80

        self.fleet_speed = 1
        self.fleet_drop_speed = 15
        self.alien_points = 50

        self.machine_gun_cost = 300
        self.machine_gun_bullet_limit = 10
        self.machine_gun_fire_delay = 100
        self.machine_gun_burst_size = 20
        self.machine_gun_reload_delay = 1000

    def increase_speed(self):
        self.speedup_scale = 1.1
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.fleet_speed *= self.speedup_scale


