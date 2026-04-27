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
        #draw panel
        panel_rect = pygame.Rect(0, 0, self.screen_rect.width, self.screen_rect.height)
        panel_rect.center = self.screen_rect.center
        pygame.draw.rect(self.screen, self.panel_color, panel_rect)

        #draw store menu text
        title_text = "Store Menu"
        title_image = self.font.render(title_text, True, self.settings.button_color, None)
        title_rect = title_image.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = self.screen_rect.top + 50
        self.screen.blit(title_image, title_rect)
       