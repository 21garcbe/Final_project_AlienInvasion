"""Game_states.py

stores volatile data associated with the game
"""
class GameStats():

    def __init__(self, ship_limit):
        self.ships_left = ship_limit
        self.level = 1
        self.current_pattern = "rectangle"

