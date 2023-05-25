import pandas as pd
import datetime as dt
from datetime import time
import pickle
from player import Player

try:
    with open('last_time.pickle', 'wb') as file:
        latest_time = pickle.load(file)
except EOFError:
    latest_time = time()

players = set()

def parse_nets(in_and_outs):
    df = pd.read_csv(in_and_outs, skiprows=1, skip_blank_lines=False)
    finished_game = False
    new_latest_time = time()
    for _, row in df.iterrows():
        user = row['User']
        if user == 'nan' and not finished_game:
            players.clear()
        elif user == 'End time':
            curr_end_time = dt.strptime(row['In'], '%Y-%m-%d %H:%M:%S')
            if curr_end_time <= latest_time:
                return
            finished_game = True
            new_latest_time = max(new_latest_time, curr_end_time)
            
        players.add(Player(username=user))

    # for col in df.columns:
    #     print(col)
    # print(df['In']) 
    # print(df['User'].iloc[20])


def parse_stats(hand_histories):
    pass


parse_nets(r"C:\Users\bdu82\Downloads\chip_history_2023-5-24_20-51EST.csv")