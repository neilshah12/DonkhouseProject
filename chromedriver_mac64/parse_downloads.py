import pandas as pd


class Player:
    def __init__(self, username, net=0, vpip=0):
        self.username = username
        self.net = net
        self.vpip = vpip


def parse_nets(in_and_outs):
    df = pd.read_csv(in_and_outs)
    print(df)


def parse_stats(hand_histories):
    pass
