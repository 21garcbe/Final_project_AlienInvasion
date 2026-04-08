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
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'