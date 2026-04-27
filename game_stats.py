"""Game_states.py

stores volatile data associated with the game
"""
from typing import TYPE_CHECKING
#from pathlib import Path
import json

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()
        self.current_pattern = "rectangle"
    
    def init_saved_scores(self):
        """Initialize max score from file"""
        self.path = self.settings.scores_file

        if self.path.exists() and self.path.stat().st_size > 80:
            contents = self.path.read_text()
            if not contents:
                print('file empty')
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()
            #save the file

    def save_scores(self):
        """"""
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent =4)

        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f"File not found: {e}")


    

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1
        self.credits =0
        self.machine_gun_unlocked = False

    def update(self, collisions):
        """Update game stats based on collisions"""
        #update score
        self._update_score(collisions)
        #update max score
        self._update_max_score()
        #update hi_score
        self._update_hi_score()



    def _update_max_score(self):
        """Update max score if current score exceeds it"""
        if self.score > self.max_score:
            self.max_score = self.score

        
    
    def _update_hi_score(self):
        """Update hi score if current score exceeds it"""
        if self.score > self.hi_score:
            self.hi_score = self.score

      

    def _update_score(self, collisions):
        """Update score and credits based on alien collisions"""
        for alien in collisions:
            self.score += self.settings.alien_points
            self.credits += self.settings.alien_points
        
        
        

    def update_level(self):
        """Update level and increase game difficulty(speed up aliens)"""
        self.level += 1
        print(f"Level: {self.level}")
    
    
        

        



