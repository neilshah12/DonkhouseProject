class Player:
    def __init__(self, username: str, net: float = 0, hands_seen: int = 0, hand_played: int = 0):
        self.username = username
        self.net = net
        self.hands = hands_seen
        self.hands = hand_played

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.username == other.username
        return False

    def __hash__(self):
        return hash(self.username)

    def __str__(self):
        return f"Player(username={self.username}, net={self.net}, hands_seen={self.hands_seen})"
