class Player:
    def __init__(self, username, net=0, vpip=0):
        self.username = username
        self.net = net
        self.vpip = vpip
    
    def __eq__(self, other):
        if(isinstance(other, Player)):
            return self.username == other.username
        return False