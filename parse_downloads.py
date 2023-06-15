from datetime import datetime as dt
from typing import Dict
from player import Player
from schema import Player_Table
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import math
import pandas as pd
import pickle
import re
import sys

all_players: Dict[str, Player] = {}
engine = create_engine('sqlite:///mydb.db')
Session = sessionmaker(bind=engine)
session = Session()


def init_info():
    with open('info.pickle', 'wb') as f:
        pickle.dump({}, f)


def load_info():
    with open('info.pickle', 'rb') as f:
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


def parse_nets(ledger, info):  # ledger
    table = re.search(r'(.*?)_ledger.csv', ledger).group(1)

    df = pd.read_csv(ledger, skiprows=1, skip_blank_lines=False)

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
            new_game = Game(game_end_time.date(), table)
            for player in game_players:
                new_game.players.append(player)
            all_games.append(new_game)
            if game_end_time <= latest_parsed_time:
                return
            new_latest_time = max(new_latest_time, game_end_time)
            update_players(all_players, game_players)
        elif not math.isnan(net):
            game_players[user] = Player(user, net=net)
    if new_latest_time > latest_parsed_time:
        info[f'{table} latest parsed time'] = new_latest_time


def parse_stats(hand_histories, prev_info, curr_info):  # hand histories
    patterns = {
        'new_game': r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: New hand \(ID [a-zA-Z0-9]+\) of NL Texas Holdem',
        'time': r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
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
    print(f'hand_histories: {hand_histories}')
    table = re.search(r'logs/(.*?)_hand_histories.txt', hand_histories).group(1)
    if f'{table} latest parsed time' in prev_info:
        prev_latest_time = prev_info[f'{table} latest parsed time']
    else:
        prev_latest_time = dt.min
    curr_latest_time = curr_info[f'{table} latest parsed time']

    with open(hand_histories, 'r') as f:
        player_dict: Dict[str, Player] = {}

        for line in f:
            if not re.search(patterns['new_game'], line):
                continue
            time = dt.strptime(re.search(patterns['time'], line).group(1), '%Y-%m-%d %H:%M:%S')
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

            num_players_in_hand = len(game_players)
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
                        rfi_player.lim = (0, 1)
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
                        player.lim = (1, 1)
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
                        player.lim = (0, 1)
                    elif tb_player is None:
                        player.tb = (0, 1)
                    elif fb_player is None:
                        if rfi_player == player:
                            player.f3b = (1, 1)
                        player.fb = (0, 1)

                    num_players_in_hand -= 1

                line = f.readline()

            first_bet_on_flop_player = None

            if num_players_in_hand < 3:
                if f'{table} hands reached flop with 3+ players' in curr_info:
                    percent = curr_info[f'{table} hands reached flop with 3+ players']
                    num = percent[0] + 0
                    denom = percent[1] + 1
                    curr_info[f'{table} hands reached flop with 3+ players'] = (num, denom)
                else:
                    curr_info[f'{table} hands reached flop with 3+ players'] = (0, 1)
            else:
                if f'{table} hands reached flop with 3+ players' in curr_info:
                    percent = curr_info[f'{table} hands reached flop with 3+ players']
                    num = percent[0] + 1
                    denom = percent[1] + 1
                    curr_info[f'{table} hands reached flop with 3+ players'] = (num, denom)
                else:
                    curr_info[f'{table} hands reached flop with 3+ players'] = (1, 1)

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
    init_info()
    prev_info = load_info()
    curr_info = prev_info.copy()
    parse_nets(sys.argv[2], curr_info)
    parse_stats(sys.argv[1], prev_info, curr_info)

    for play in all_players:   
        player = all_players[play]
        existing_row = session.query(Player_Table).filter_by(username=player.username).first()

        if existing_row:
            stmt = update(Player_Table).where(Player_Table.username == player.username).values(net=Player_Table.net+player.net,
                                                                                            VPIP_num=Player_Table.VPIP_num+player.vpip[0],
                                                                                            VPIP_denom=Player_Table.VPIP_denom+player.vpip[1],
                                                                                            UOPFR_num=Player_Table.UOPFR_num+player.uopfr[0],
                                                                                            UOPFR_denom=Player_Table.UOPFR_denom+player.uopfr[1],
                                                                                            PFR_num=Player_Table.PFR_num+player.pfr[0],
                                                                                            PFR_denom=Player_Table.PFR_denom+player.pfr[1],
                                                                                            threebet_num=Player_Table.threebet_num+player.tb[0],
                                                                                            threebet_denom=Player_Table.threebet_denom+player.tb[1],
                                                                                            fourbet_num=Player_Table.fourbet_num+player.fb[0],
                                                                                            fourbet_denom=Player_Table.fourbet_denom+player.fb[1],
                                                                                            fold_to_three_num = Player_Table.fold_to_three_num + player.f3b[0], 
                                                                                            fold_to_three_denom = Player_Table.fold_to_three_denom + player.f3b[1], 
                                                                                            c_bet_num = Player_Table.c_bet_num + player.cbet[0],
                                                                                            c_bet_denom = Player_Table.c_bet_denom + player.cbet[1],
                                                                                            donk_num = Player_Table.donk_num + player.donk[0], 
                                                                                            donk_denom = Player_Table.donk_denom + player.donk[1],
                                                                                            limp_num=Player_Table.limp_num + player.lim[0],
                                                                                            limp_denom = Player_Table.limp_denom + player.lim[1])
            session.execute(stmt)
            session.commit()
        else:
            new_row = Player_Table(username=player.username, net=player.net,
                                    VPIP_num=player.vpip[0],
                                    VPIP_denom=player.vpip[1],
                                    UOPFR_num=player.uopfr[0],
                                    UOPFR_denom=player.uopfr[1],
                                    PFR_num=player.pfr[0],
                                    PFR_denom=player.pfr[1],
                                    threebet_num=player.tb[0],
                                    threebet_denom=player.tb[1],
                                    fourbet_num=player.fb[0],
                                    fourbet_denom=player.fb[1],
                                    fold_to_three_num = player.f3b[0], 
                                    fold_to_three_denom = player.f3b[1], 
                                    c_bet_num = player.cbet[0],
                                    c_bet_denom = player.cbet[1],
                                    donk_num = player.donk[0], 
                                    donk_denom = player.donk[1],
                                    limp_num= player.lim[0],
                                    limp_denom = player.lim[1])
            session.add(new_row)
            session.commit()
        
    update_pickle_info(curr_info)
    # session.close()
    # engine.dispose()
    info = load_info()


if __name__ == '__main__':
    main()

