class Player:
    def __init__(self, username: str, net: float = 0, hands_seen: int = 0, hands_played: int = 0,
                 hands_raised_pre: int = 0):
        self.username = username
        self.net = net
        self.hands_seen = hands_seen
        self.hands_played = hands_played
        self.hands_raised_pre = hands_raised_pre

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.username == other.username
        return False

    def __hash__(self):
        return hash(self.username)

    def __str__(self):
        return f"Player(username={self.username}, net={self.net}, hands_seen={self.hands_seen}, " \
               f"hands_played={self.hands_played}, hands_raised_pre={self.hands_raised_pre})"

