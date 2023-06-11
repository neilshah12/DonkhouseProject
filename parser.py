from datetime import datetime as dt
from typing import Dict
from player import Player

import math
import pandas as pd
import pickle
import re
import sys

all_players: Dict[str, Player] = {}


def load_info():
    with open('info.pickle', 'wb') as f:
        return pickle.load(f)


def update_pickle_info(info):
    with open('info.pickle', 'wb') as f:
        pickle.dump(info, f)


def update_players(players_dict, game_players):
    for key in game_players:
        player = game_players[key]
        if player.username in players_dict:
            players_dict[key].update(player)
        else:
            players_dict[key] = player


def parse_nets(in_and_outs, info):  # ledger
    table = re.search(r'(.*?)_ledger.csv').group()
    if table is None:
        return
    df = pd.read_csv(in_and_outs, skiprows=1, skip_blank_lines=False)

    if f'{table} latest parsed time' in info:
        latest_parsed_time = info[f'{table} latest parsed time']
    else:
        latest_parsed_time = info[f'{table} latest parsed time'] = dt.min

    new_latest_time = latest_parsed_time
    game_players: Dict[str, Player] = {}
    for _, row in df.iterrows():
        user = row['User']
        net = row['Net']
        if not isinstance(user, str):
            game_players.clear()
        elif user == 'End time:' and math.isnan(net):
            game_end_time = dt.strptime(row['In'], '%Y-%m-%d %H:%M:%S')
            if game_end_time <= latest_parsed_time:
                return
            new_latest_time = max(new_latest_time, game_end_time)
            update_players(all_players, game_players)
        elif not math.isnan(net):
            game_players[user] = Player(user)

    if new_latest_time > latest_parsed_time:
        info[f'{table} latest parsed time'] = new_latest_time


def parse_stats(hand_histories, prev_info, curr_info):  # hand histories
    patterns = {
        'new_game': r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: New hand \(ID [a-zA-Z0-9]+\) of NL Texas Holdem',
        'time': r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
        'bb_player': r'([a-zA-Z0-9_.-]+) \(\d+(\.\d{1,2})?, BB\)',
        'in_hand': r'[a-zA-Z0-9_.-]+ \(\d+(\.\d{1,2})?, [A-Z0-9+]+\)',
        'bb_post': r'[a-zA-Z0-9_.-]+ posted (\d+(\.\d{1,2})?)',
        'flop': r'board: ([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+'
                r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+'
                r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)',
        'turn': r'board: ([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+'
                r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+'
                r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)\s+'
                r'([2-9]|10|J|Q|K|A)(\\uc0)?(♠|♦|♥|♣)',
        'bet': r'[a-zA-Z0-9_.-]+ bet \d+(\.\d{1,2})?',
        'call': r'[a-zA-Z0-9_.-]+ called \d+(\.\d{1,2})?',
        'raise': r'[a-zA-Z0-9_.-]+ raised to \d+(\.\d{1,2})?',
        'check': r'[a-zA-Z0-9_.-]+ checked',
        'fold': r'[a-zA-Z0-9_.-]+ folded',
        'player': r'([a-zA-Z0-9_.-]+)',
        'won': r'([a-zA-Z0-9_.-]+) won \d+(\.\d{1,2})? chips',
        'table': r'(.*?)_hand_histories.txt'
    }

    table = re.search(patterns['table'], hand_histories).group()
    if table is None:
        return

    # prev_latest_time = prev_info[f'{table} latest parsed time']
    # curr_latest_time = curr_info[f'{table} latest parsed time']

    prev_latest_time = dt.min  # for testing purposes
    curr_latest_time = dt.max  # for testing purposes

    with open(hand_histories, 'r') as f:
        player_dict: Dict[str, Player] = {}

        for line in f:
            if not re.search(patterns['new_game'], line):
                continue
            time = dt.strptime(re.search(patterns['time'], line).group(), '%Y-%m-%d %H:%M:%S')
            if time <= prev_latest_time:
                continue
            elif time > curr_latest_time:
                update_players(all_players, player_dict)
                return

            game_players: Dict[str, Player] = {}
            bb_player = None
            line = f.readline()

            while line and not re.match(patterns['bb_post'], line):
                if re.match(patterns['in_hand'], line):
                    player_name = re.match(patterns['player'], line).group(1)
                    game_players[player_name] = Player(player_name)
                    if re.match(patterns['bb_player'], line):
                        bb_player = game_players[player_name]
                line = f.readline()

            is_walk = True
            rfi_player, tb_player, fb_player, last_raise_player = None, None, None, None

            # preflop
            while line and not re.match(patterns['flop'], line):
                if re.match(patterns['won'], line):
                    if is_walk:
                        del bb_player
                    break
                elif re.match(patterns['raise'], line):
                    player = game_players[re.match(patterns['player'], line).group(1)]

                    player.pfr = (1, 1)
                    player.vpip = (1, 1)

                    if rfi_player is None:
                        rfi_player = player
                        rfi_player.uopfr = (1, 1)
                    elif tb_player is None:
                        tb_player = player
                        tb_player.tb = (1, 1)
                    elif player.raised:
                        fb_player = player
                        fb_player.fb = (1, 1)

                    last_raise_player = player
                    player.raised = True
                    is_walk = False
                elif re.match(patterns['call'], line):
                    player = game_players[re.match(patterns['player'], line).group(1)]
                    player.vpip = (1, 1)
                    player.pfr = (0, 1) if player.pfr != (1, 1) else (0, 1)
                    is_walk = False

                    if rfi_player is None:
                        player.uopfr = (0, 1)
                        player.called_bb = True
                    elif tb_player is None:
                        player.tb = (0, 1)
                    elif fb_player is None:
                        if rfi_player == player:
                            player.f3b = (0, 1)
                        player.fb = (0, 1)
                elif re.match(patterns['fold'], line):
                    player = game_players[re.match(patterns['player'], line).group(1)]

                    if player.vpip != (1, 1):
                        player.vpip = (0, 1)

                    if player.pfr != (1, 1):
                        player.pfr = (0, 1)

                    if rfi_player is None:
                        player.uopfr = (0, 1)
                    elif tb_player is None:
                        player.tb = (0, 1)
                    elif fb_player is None:
                        if rfi_player == player:
                            player.f3b = (1, 1)
                        player.fb = (0, 1)

                line = f.readline()

            first_bet_on_flop_player = None
            while line and not re.match(patterns['turn'], line):
                if re.match(patterns['won'], line):
                    break
                if re.match(patterns['bet'], line):
                    player = game_players[re.match(patterns['player'], line).group(1)]
                    if first_bet_on_flop_player is None:
                        if player != last_raise_player:
                            if last_raise_player is not None and last_raise_player.cbet == (0, 0):
                                player.donk = (1, 1)
                        else:
                            player.cbet = (1, 1)
                    first_bet_on_flop_player = player
                elif re.match(patterns['check'], line):
                    player = game_players[re.match(patterns['player'], line).group(1)]
                    if first_bet_on_flop_player is None:
                        player.donk = (0, 1)
                    if player == last_raise_player and first_bet_on_flop_player is None:
                        player.cbet = (0, 1)
                line = f.readline()
            update_players(player_dict, game_players)
            game_players.clear()
        update_players(all_players, player_dict)


def main():
    prev_info = load_info()
    curr_info = prev_info.copy()

    parse_nets(sys.argv[2], curr_info)
    parse_stats(sys.argv[1], prev_info, curr_info)

    update_pickle_info(curr_info)


if __name__ == '__main__':
    main()
