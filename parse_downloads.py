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
            players_dict[key].update(player)
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
    new_game_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: New hand \(ID [a-zA-Z0-9]+\) of NL Texas Holdem'
    time_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    bb_player_pattern = r'([a-zA-Z0-9_.-]+) \(\d+(\.\d{1,2})?, BB\)'
    in_hand_pattern = r'[a-zA-Z0-9_.-]+ \(\d+(\.\d{1,2})?, [A-Z0-9+]+\)'
    bb_post_pattern = r'[a-zA-Z0-9_.-]+ posted (\d+(\.\d{1,2})?)'
    # flop_pattern = r'board: ([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)\s+' \
    #                r'([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)\s+' \
    #                r'([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)'
    # turn_pattern = r'board: ([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)\s+' \
    #                r'([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)\s+' \
    #                r'([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)\s+' \
    #                r'([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)'
    flop_pattern = r'board: ([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+' \
                   r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+' \
                   r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)'
    turn_pattern = r'board: ([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+' \
                   r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+' \
                   r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+' \
                   r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)'
    bet_pattern = r'[a-zA-Z0-9_.-]+ bet \d+(\.\d{1,2})?'
    call_pattern = r'[a-zA-Z0-9_.-]+ called \d+(\.\d{1,2})?'
    raise_pattern = r'[a-zA-Z0-9_.-]+ raised to \d+(\.\d{1,2})?'
    fold_pattern = r'[a-zA-Z0-9_.-]+ folded'
    player_pattern = r'([a-zA-Z0-9_.-]+)'
    won_pattern = r'([a-zA-Z0-9_.-]+) won \d+(\.\d{1,2})? chips'

    with open(hand_histories, 'r') as f:
        player_dict: Dict[str, Player] = {}

        for line in f:
            if not re.search(new_game_pattern, line):
                continue
            time = dt.strptime(re.search(time_pattern, line).group(), '%Y-%m-%d %H:%M:%S')

            if time <= prev_latest_time:
                continue
            elif time > curr_latest_time:
                update_players(all_players, player_dict)
                return

            game_players: Dict[str, Player] = {}
            bb_player = None
            line = f.readline()

            while line and not re.match(bb_post_pattern, line):
                if re.match(in_hand_pattern, line):
                    player_name = re.match(player_pattern, line).group(1)
                    game_players[player_name] = Player(player_name)
                    if re.match(bb_player_pattern, line):
                        bb_player = game_players[player_name]
                line = f.readline()

            is_walk = True
            rfi_player, tb_player, fb_player, last_raise_player = None, None, None, None

            # preflop
            while line and not re.match(flop_pattern, line):
                if re.match(won_pattern, line):
                    if is_walk:
                        del game_players[bb_player]
                    break
                elif re.match(raise_pattern, line):
                    player = game_players[re.match(player_pattern, line).group(1)]

                    player.pfr = (1, 1)
                    player.vpip = (1, 1)

                    if rfi_player is None:
                        rfi_player = player
                        rfi_player.uopfr = (1, 1)
                    elif tb_player is None and not player.called_bb:
                        tb_player = player
                        tb_player.tb = (1, 1)
                    elif fb_player is None and player.raised:
                        fb_player = player
                        fb_player.fb = (1, 1)

                    last_raise_player = player
                    player.raised = True
                    is_walk = False
                elif re.match(call_pattern, line):
                    player = game_players[re.match(player_pattern, line).group(1)]
                    player.vpip = (1, 1)
                    player.pfr = (0, 1)
                    is_walk = False

                    if rfi_player is None:
                        player.uopfr = (0, 1)
                        player.called_bb = True
                    elif tb_player is None:
                        player.tb = (0, 1)
                    elif fb_player is None:
                        player.fb = (0, 1)
                    is_walk = False
                elif re.match(fold_pattern, line):
                    player = game_players[re.match(player_pattern, line).group(1)]
                    if player == rfi_player and fb_player is None:
                        game_players[player].f3b = (1, 1)
                line = f.readline()



            # print(repr(line))
            first_bet_on_flop_player = ""
            while line and not re.match(turn_pattern, line):
                # print(repr(line))
                if re.match(won_pattern, line):
                    break
                if re.match(bet_pattern, line):
                    player = re.match(player_pattern, line).group(1)
                    if first_bet_on_flop_player == "":
                        if player != last_raise_player:
                            game_players[player].donk = (1, 1)
                            game_players[last_raise_player].cbet = (0, 0)
                        else:
                            game_players[player].cbet = (1, 1)

                line = f.readline()
            update_players(player_dict, game_players)
            game_players.clear()
        update_players(all_players, player_dict)


prev_latest_time = dt.min
curr_latest_time = dt.strptime('2023-06-10 20:12:37', '%Y-%m-%d %H:%M:%S')
parse_stats(r'/Users/brandondu/Downloads/Test5.txt')
for p in all_players:
    print(all_players[p])

#
# text = 'board: Q\\uc0\\u9827  Q\\u9830  6\\u9824 \\\n'
# pattern = r'board: ([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)\s+' \
#           r'([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)\s+' \
#           r'([2-9]|10|J|Q|K|A)(\\uc0)?(\\u9830|\\u9827|\\u9829|\\u9824)'
# #
# matches = re.findall(pattern, text)
# print(matches)
