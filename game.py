from __future__ import annotations
from typing import Dict, Optional
import datetime as dt
from player import Player
class Game:
    def __init__(self, name: str, date: dt.date = dt.date.min):
        self.name = name
        self.date = date
        self.player_nets : Dict[str, float] = {}

    @classmethod
    def fromdict(cls, dict) -> Game:
        game_date = dt.datetime.strptime(dict['date'], "%Y-%m-%d").date()
        game = cls(dict['name'], game_date)
        for k, v in dict.items():
            if k == 'player_nets':
                for username, net in v.items():
                    game.player_nets[username] = net
        return game
    
    
    def to_dict(self):
        dict = {}
        dict['name'] = self.name
        dict['date'] = self.date.strftime("%Y-%m-%d")
        dict['player_nets'] = self.player_nets
        return dict

    def add_player(self, player: Player):
        if player is None:
            return
        if player.username in self.player_nets:
            raise Exception('Duplicate player in game')
        
        self.player_nets[player.username] = player.net

    def __str__(self):
        return f"Game: {self.name}, Date: {self.date}, Players: {self.player_nets}"