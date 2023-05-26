from datetime import datetime as dt
from typing import Dict

import math
import pandas as pd
import pickle
import re

from player import Player

try:
    with open('last_time.pickle', 'rb') as file:
        latest_time = pickle.load(file)
except (EOFError, FileNotFoundError):
    latest_time = dt.min

new_latest_time = latest_time
all_players = Dict[str, Player]


def update_latest_time():
    with open('last_time.pickle', 'wb') as f:
        pickle.dump(latest_time, f)


def update_players(players_dict, game_players):
    for player in game_players:
        if player in players_dict:
            dict_player = players_dict.get(player.username)
            dict_player.net += player.net
            dict_player.hands += player.hands_seen
        else:
            players_dict[player.username] = player


def parse_nets(in_and_outs: str):
    global new_latest_time
    df = pd.read_csv(in_and_outs, skiprows=1, skip_blank_lines=False)

    game_players = list()
    for _, row in df.iterrows():
        user = row['User']
        net = row['Net']
        if not isinstance(user, str):
            game_players.clear()
        elif user == 'End time:' and math.isnan(net):
            curr_end_time = dt.strptime(row['In'], '%Y-%m-%d %H:%M:%S')
            new_latest_time = max(new_latest_time, curr_end_time)
            if curr_end_time <= latest_time:
                return
            update_players(all_players, game_players)
        elif not math.isnan(net):
            game_players.append(Player(username=user, net=net))


def parse_stats(hand_histories: str):
    count = 0
    with open(hand_histories, 'r') as f:
        new_game_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: New hand \(ID [a-zA-Z0-9]+\) of NL Texas Holdem$'
        time_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        bb_player_pattern = r'^([a-zA-Z0-9_.-]+) \(\d+(\.\d{1,2})?, BB\)'
        in_hand_pattern = r'^[a-zA-Z0-9_.-]+ \(\d+(\.\d{1,2})?, [A-Z]{2}\)'
        bb_post_pattern = r'^[a-zA-Z0-9_.-]+ posted (\d+(\.\d{1,2})?)$'
        flop_pattern = r'^board: [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] $'
        turn_pattern = r'^board: [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] $'
        river_pattern = r'^board: [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] [2-10JKQA][♣♦♥♠] $'
        won_pattern = r'^([a-zA-Z0-9_.-]+) won (\d+(\.\d{1,2}) chips'
        vpip_pattern = r'^([a-zA-Z0-9_.-]+) (called \d+(\.\d{1,2})?|raised to \d+(\.\d{1,2})?)$'
        player_dict = Dict[str, Player]
        for line in f:
            game_over = False
            # hand started
            if re.match(pattern=new_game_pattern, string=line):
                time = dt.strptime(re.match(pattern=time_pattern, string=line).group(1), '%Y-%m-%d %H:%M:%S')
                if time <= latest_time:
                    continue
                game_players = Dict[str, Player]
                line = f.readline()
                bb_player = str
                while not re.match(pattern=bb_post_pattern, string=line):
                    if re.match(pattern=in_hand_pattern, string=line):
                        player_name = re.match(r'^([a-zA-Z0-9_.-]+)').group(1)
                        game_players[player_name] = Player(username=player_name, hands_seen=1)
                        if re.match(pattern=bb_player_pattern, string=line):
                            bb_player = player_name
                    line = f.readline()

                is_walk = True
                line = f.readline()
                while not re.match(pattern=flop_pattern, string=line):
                    if re.match(pattern=won_pattern, string=line):
                        game_over = True
                        if is_walk:
                            del game_players[bb_player]
                        break
                    player = re.match(pattern=vpip_pattern, string=line).group(1)
                    if player is not None:
                        game_players.get(player).hands_played = 1
                        is_walk = False

                if not game_over:
                    line = f.readline()
                    while not re.match(pattern=won_pattern, string=line):
                        line = f.readline()

                    winner = re.match(pattern=won_pattern, string=line).group(1)
                    while winner is not None:
                        game_players.get(winner)

                update_players(player_dict, game_players)


#
# parse_nets(r"/Users/brandondu/Downloads/Test.csv")
# for key, value in all_players.items():
#     print(f"{key}: {value}")

# parse_stats(r'/Users/brandondu/Downloads/game_log_2023-5-25_20-12EST.txt')

# preflop_action_pattern = r'^([a-zA-Z0-9_.-]+) (called \d+(\.\d{1,2})?|raised to \d+(\.\d{1,2})?|folded)$'
# text = "Player1 folded"
# print(re.match(preflop_action_pattern, text).group(1))