import pygame.font

class StoreMenu:
    """A class to manage the in game store menu for purchasing upgrades with credits"""

    def __init__(self, game):
        """Initialize the store menu attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.game_stats

        #font settings for store menu
        self.text_color = self.settings.text_color
        self.panel_color = self.settings.text_color

        self.title_font = pygame.font.Font(self.settings.font_file,self.settings.button_font_size)

        self.body_font = pygame.font.Font(
            self.settings.font_file,
            self.settings.HUD_font_size)
        
    def draw(self):
        """Draw the store menu panel and text to the screen, calls _get_menu_lines to get the menu body text for rendering on display"""
        panel_rect = self.screen_rect
        self.screen.fill(self.panel_color, panel_rect)

        lines = self._get_menu_lines()

        y = panel_rect.top + 50

        for i, line in enumerate(lines):
            # Title line
            if i == 0:
                font = self.title_font
            else:
                font = self.body_font

            image = font.render(
                line,
                True,
                self.settings.button_color,
                None
            )

            rect = image.get_rect()
            rect.centerx = panel_rect.centerx
            rect.top = y

            self.screen.blit(image, rect)

            #body line spacing
            if i == 0:
                y += 70
            else:
                y += 35
    
    def _get_menu_lines(self):
        """Generate the lines of text to show in the menu body"""
        machine_gun_text = ( f"1 - Machine Gun Upgrade: {self.settings.machine_gun_cost} credits"
                                if not self.stats.machine_gun_unlocked 
                                else "Machine Gun Upgrade: UNLOCKED"
            )
        return [ 
            "STORE MENU",
            f"Credits: {self.stats.credits}",
            "",
            machine_gun_text,
            "Press M to exit store"
        ]