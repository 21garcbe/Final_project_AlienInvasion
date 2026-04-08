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