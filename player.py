class Player:
    def __init__(self, username: str, net: float = 0, hands: float = 0):
        self.username = username
        self.net = net
        self.hands = hands

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.username == other.username
        return False

    def __hash__(self):
        return hash(self.username)

    def __str__(self):
        return f"Player(username={self.username}, net={self.net}, hands={self.hands})"

