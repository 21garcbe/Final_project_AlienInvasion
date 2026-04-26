import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class ScoreBoard:
    def __init__(self, game = 'AlienInvasion'):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.game_stats

        #font settings for scoring info
        self.text_color = self.settings.text_color
        self.font = pygame.font.Font(self.settings.font_file, self.settings.HUD_font_size)

        #prepare initial score image
        self.prep_score()
    
    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        #display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """draw score to screen"""
        self.screen.blit(self.score_image, self.score_rect)