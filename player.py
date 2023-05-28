class Player:
    def __init__(self, username: str, net: float = 0, hands_seen: int = 0, hands_played: int = 0,
                 hands_raised_pre: int = 0, hands_tb: int = 0, hands_fb: int = 0, hands_cb: int = 0,
                 hands_fold_to_cb_after_raise: int = 0, hands_fold_to_cb: int = 0):
        self.username = username
        self.net = net
        self.hands_seen = hands_seen
        self.hands_played = hands_played
        self.hands_raised_pre = hands_raised_pre
        self.hands_tb = hands_tb
        self.hands_fb = hands_fb
        self.hands_cb = hands_cb
        self.hands_fold_to_cb_after_raise = hands_fold_to_cb_after_raise
        self.hands_fold_to_cb = hands_fold_to_cb

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.username == other.username
        return False

    def __hash__(self):
        return hash(self.username)

    def __str__(self):
        return f"Player(username={self.username}, net={self.net}, hands_seen={self.hands_seen}, " \
               f"hands_played={self.hands_played}, hands_raised_pre={self.hands_raised_pre})"

