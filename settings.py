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

        #set ship image file path + settings
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_width = 40
        self.ship_height = 60
        self.ship_speed = 5
        
        #set bullet image filepath + settings
        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.bullet_speed = 7
        self.bullet_width = 25
        self.bullet_height = 80
        self.bullet_amount = 5