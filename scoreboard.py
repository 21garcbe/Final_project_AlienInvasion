import pygame.font
from typing import TYPE_CHECKING
from ship import Ship
from arsenal import Arsenal
from pygame.sprite import Group

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class ScoreBoard:
    def __init__(self, game = 'AlienInvasion'):
        """Initalize scoreboard attributes and prepare inital images for score, high score, level and ships left"""
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
        self.prep_hi_score()

        #prep credits (spendable points)
        self.prep_credits()

        #prepare level
        self.prep_level()

        #prepare ship count display
        self.prep_ships()

    
    def prep_ships(self):
        """Display lives left as ship sprites"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game, Arsenal(self.game))
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    
    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        #display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_hi_score(self):
        """Render the high score as and image"""
        hi_score = round(self.stats.hi_score, -1)
        hi_score_str = f"{hi_score:,}"
        self.hi_score_image = self.font.render(hi_score_str, True, self.text_color, None)

        self.hi_screen_rect = self.hi_score_image.get_rect()
        self.hi_screen_rect.centerx = self.screen_rect.centerx
        self.hi_screen_rect.top = self.score_rect.top
    
    def prep_credits(self):
        """Render the credits as an image on HUD"""
        credits_str = f"Credits: {self.stats.credits}"
        self.credits_image = self.font.render(credits_str, True, self.text_color, None)

        self.credits_rect = self.credits_image.get_rect()
        self.credits_rect.left = self.screen_rect.left + 20
        self.credits_rect.bottom = self.screen_rect.bottom - 20

    def show_score(self):
        """draw score, level and lives left (ship count) to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hi_score_image, self.hi_screen_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.credits_image, self.credits_rect)
        self.ships.draw(self.screen)
    
    def prep_level(self):
        """Display level"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, None)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10