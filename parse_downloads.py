import pandas as pd
from datetime import datetime as dt
import math
import pickle
from player import Player

try:
    with open('last_time.pickle', 'rb') as file:
        latest_time = pickle.load(file)
except (EOFError, FileNotFoundError):
    latest_time = dt.min


all_players = dict()


def update_latest_time():
    with open('last_time.pickle', 'wb') as f:
        pickle.dump(latest_time, f)


def update_players(game_players):
    for player in game_players:
        if player in all_players:
            dict_player = dict.get(player.username)
            dict_player.net += player.net
            dict_player.hands += player.hands
        else:
            all_players[player.username] = player


def parse_nets(in_and_outs: str):
    df = pd.read_csv(in_and_outs, skiprows=1, skip_blank_lines=False)
    new_latest_time = latest_time
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
            update_players(game_players)
        elif not math.isnan(net):
            game_players.append(Player(username=user, net=net))
    update_latest_time()


def parse_stats(hand_histories):
    pass


parse_nets(r"/Users/brandondu/Downloads/Test.csv")
for key, value in all_players.items():
    print(f"{key}: {value}")
