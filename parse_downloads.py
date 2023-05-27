from datetime import datetime as dt
from typing import Dict
from player import Player

import math
import pandas as pd
import pickle
import re


try:
    with open('last_time.pickle', 'rb') as file:
        prev_latest_time = pickle.load(file)
except (EOFError, FileNotFoundError):
    prev_latest_time = dt.min

# curr_latest_time = prev_latest_time
all_players: Dict[str, Player] = {}


def update_latest_time():
    with open('last_time.pickle', 'wb') as f:
        pickle.dump(prev_latest_time, f)


def update_players(players_dict, game_players):
    for key in game_players:
        player = game_players[key]
        if player.username in players_dict:
            dict_player = players_dict.get(player.username)
            dict_player.net += player.net
            dict_player.hands_seen += player.hands_seen
            dict_player.hands_played += player.hands_played
            dict_player.hands_raised_pre += player.hands_raised_pre
        else:
            players_dict[key] = player


def parse_nets(in_and_outs: str):
    global curr_latest_time
    df = pd.read_csv(in_and_outs, skiprows=1, skip_blank_lines=False)

    game_players = list()
    for _, row in df.iterrows():
        user = row['User']
        net = row['Net']
        if not isinstance(user, str):
            game_players.clear()
        elif user == 'End time:' and math.isnan(net):
            curr_end_time = dt.strptime(row['In'], '%Y-%m-%d %H:%M:%S')
            if curr_end_time <= prev_latest_time:
                return
            curr_latest_time = max(curr_latest_time, curr_end_time)
            update_players(all_players, game_players)
        elif not math.isnan(net):
            game_players.append(Player(username=user, net=net))


def parse_stats(hand_histories: str):
    new_game_pattern = r'(\ufeff)?\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: New hand \(ID [a-zA-Z0-9]+\) of NL Texas Holdem'
    time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    bb_player_pattern = r'^([a-zA-Z0-9_.-]+) \(\d+(\.\d{1,2})?, BB\)'
    in_hand_pattern = r'^[a-zA-Z0-9_.-]+ \(\d+(\.\d{1,2})?, [A-Z0-9+]+\)'
    bb_post_pattern = r'^[a-zA-Z0-9_.-]+ posted (\d+(\.\d{1,2})?)'
    flop_pattern = r'^board: ([2-9]|10|J|Q|K|A)\? ([2-9]|10|J|Q|K|A)\? ([2-9]|10|J|Q|K|A)\? '
    won_pattern = r'^([a-zA-Z0-9_.-]+) won \d+(\.\d{1,2})? chips'
    vpip_pattern = r'^([a-zA-Z0-9_.-]+) (called \d+(\.\d{1,2})?|raised to \d+(\.\d{1,2})?)'
    raise_pattern = r'^[a-zA-Z0-9_.-]+ raised to \d+(\.\d{1,2})?'

    with open(hand_histories, 'r') as f:
        player_dict: Dict[str, Player] = {}
        for line in f:
            if re.match(pattern=new_game_pattern, string=line) is None:
                continue
            time = dt.strptime(re.search(pattern=time_pattern, string=line).group(1), '%Y-%m-%d %H:%M:%S')

            if time <= prev_latest_time:
                continue
            elif time > curr_latest_time:
                update_players(all_players, player_dict)
                return

            game_players: Dict[str, Player] = {}
            bb_player = str
            line = f.readline()

            while re.match(pattern=bb_post_pattern, string=line) is None:
                if re.match(pattern=in_hand_pattern, string=line):
                    player_name = re.match(pattern=r'^([a-zA-Z0-9_.-]+)', string=line).group(1)
                    game_players[player_name] = Player(username=player_name, hands_seen=1)
                    if re.match(pattern=bb_player_pattern, string=line):
                        bb_player = player_name
                line = f.readline()

            is_walk = True
            line = f.readline()
            while re.match(pattern=flop_pattern, string=line) is None:
                if re.match(pattern=won_pattern, string=line):
                    if is_walk:
                        del game_players[bb_player]
                    break
                if re.match(pattern=vpip_pattern, string=line) is not None:
                    player = re.match(pattern=vpip_pattern, string=line).group(1)
                    is_walk = False
                    game_players[player].hands_played = 1
                    if re.match(pattern=raise_pattern, string=line) is not None:
                        game_players[player].hands_raised_pre = 1
                line = f.readline()
            update_players(player_dict, game_players)
            game_players.clear()
        update_players(all_players, player_dict)


prev_latest_time = dt.min
curr_latest_time = dt.strptime('2023-05-25 20:12:37', '%Y-%m-%d %H:%M:%S')
parse_stats(r'Test.txt')
for p in all_players:
    print(all_players[p])