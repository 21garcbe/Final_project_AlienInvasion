import pygame.font

class StoreMenu:
    """A class to manage the in game store menu for purchasing upgrades with credits"""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.game_stats

        #font settings for store menu
        self.text_color = self.settings.text_color
        self.font = pygame.font.Font(self.settings.font_file, self.settings.button_font_size)
        self.panel_color = self.settings.text_color
    
    def draw(self):
        """Draw the store menu panel and text to the screen"""
        panel_rect = self.screen_rect
        self.screen.fill(self.panel_color, panel_rect)

        lines = self._get_menu_lines()

        y = panel_rect.top + 50

        for line in lines:
            image = self.font.render(line, True, self.settings.button_color, None)
            rect = image.get_rect()
            rect.centerx = self.screen_rect.centerx
            rect.top = y
            self.screen.blit(image, rect)
            y += 45
    
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