from fractions import Fraction


class Player:
    def __init__(self, username, net=0):
        self.username = username
        self.net = net
        self.vpip = (0, 0)
        self.uopfr = (0, 0)
        self.pfr = (0, 0)
        self.tb = (0, 0)
        self.fb = (0, 0)
        self.f3b = (0, 0)
        self.cbet = (0, 0)
        self.donk = (0, 0)
        self.lim = (0, 0)
        self.raised = False


    def __eq__(self, other):
        if isinstance(other, Player):
            return self.username == other.username
        return False

    def __hash__(self):
        return hash(self.username)

    def __str__(self):
        return f"Player: {self.username}, " \
               f"Net: {self.net}, " \
               f"VPIP: {self.vpip}, " \
               f"UOPFR: {self.uopfr}, " \
               f"PFR: {self.pfr}, " \
               f"3-Bet: {self.tb}, " \
               f"4-Bet: {self.fb}, " \
               f"F3B: {self.f3b}, " \
               f"C-Bet: {self.cbet}, " \
               f"Donk Bet: {self.donk}, " \
               f"LIM: {self.lim}"

    def update(self, other):
        if not isinstance(other, Player) or self.username != other.username:
            return
        self.net += other.net

        self.vpip = tuple(map(lambda i, j: i + j, self.vpip, other.vpip))
        self.pfr = tuple(map(lambda i, j: i + j, self.pfr, other.pfr))
        self.uopfr = tuple(map(lambda i, j: i + j, self.uopfr, other.uopfr))
        self.tb = tuple(map(lambda i, j: i + j, self.tb, other.tb))
        self.fb = tuple(map(lambda i, j: i + j, self.fb, other.fb))
        self.f3b = tuple(map(lambda i, j: i + j, self.f3b, other.f3b))
        self.cbet = tuple(map(lambda i, j: i + j, self.cbet, other.cbet))
        self.donk = tuple(map(lambda i, j: i + j, self.donk, other.donk))
        self.lim = tuple(map(lambda i, j: i + j, self.lim, other.lim))
