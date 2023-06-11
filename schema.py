from typing import Any
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

association_table=Table(
    'association',
    Base.metadata,
    Column('player_id', ForeignKey('players.id')),
    Column('game_id', ForeignKey('games.id'))
)
class Player(Base):
    __tablename__ = "players"
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    net = Column("net", Float)
    VPIP_num = Column("VPIP_num", Integer)
    VPIP_denom = Column("VPIP_denom", Integer)
    UOPFR_num = Column("UOPFR_num", Integer)
    UOPFR_denom = Column("UOPFR_denom", Integer)
    PFR_num = Column("PFR_num", Integer)
    PFR_denom = Column("PFR_denom", Integer)
    threebet_num = Column("threebet_num", Integer)
    threebet_denom = Column("threebet_denom", Integer)
    fourbet_num = Column("fourbet_num", Integer)
    fourbet_denom = Column("fourbet_denom", Integer)
    fold_to_three_num = Column("fold_to_three_num", Integer)
    fold_to_three_denom = Column("fold_to_three_denom", Integer)
    c_bet_num = Column("c_bet_num", Integer)
    c_bet_denom = Column("c_bet_denom", Integer)
    donk_num = Column("donk_num", Integer)
    donk_denom = Column("donk_denom", Integer)
    limp_num = Column("limp_num", Integer)
    limp_denom = Column("limp_denom", Integer)
    games = relationship(
        'Game', 
        secondary=association_table,
        back_populates='players'
    )
    
    def __init__(self, id, username, net, VPIP_num, VPIP_denom, UOPFR_num, UOPFR_denom, PFR_num, PFR_denom, \
                 threebet_num, threebet_denom, fourbet_num, fourbet_denom, fold_to_three_num, fold_to_three_denom, c_bet_num, \
                 c_bet_denom, donk_num, donk_denom, limp_num, limp_denom
        ):
        self.id = id
        self.username = username
        self.net = net
        self.VPIP_num = VPIP_num
        self.VPIP_denom = VPIP_denom
        self.UOPFR_num = UOPFR_num
        self.UOPFR_denom = UOPFR_denom
        self.PFR_num = PFR_num
        self.PFR_denom = PFR_denom
        self.threebet_num = threebet_num
        self.threebet_denom = threebet_denom
        self.fourbet_num = fourbet_num
        self.fourbet_denom = fourbet_denom
        self.fold_to_three_num = fold_to_three_num
        self.fold_to_three_denom = fold_to_three_denom
        self.c_bet_num = c_bet_num
        self.c_bet_denom = c_bet_denom
        self.donk_num = donk_num
        self.donk_denom = donk_denom
        self.limp_num = limp_num
        self.limp_denom = limp_denom
        
    def __repr__(self):
        return f"PlayerStats(id={self.id}, username='{self.username}', net={self.net}, VPIP={self.VPIP_num}/{self.VPIP_denom}, " \
               f"UOPFR={self.UOPFR_num}/{self.UOPFR_denom}, PFR={self.PFR_num}/{self.PFR_denom}, " \
               f"3Bet={self.threebet_num}/{self.threebet_denom}, 4Bet={self.fourbet_num}/{self.fourbet_denom}, " \
               f"FoldTo3Bet={self.fold_to_three_num}/{self.fold_to_three_denom}, " \
               f"C-Bet={self.c_bet_num}/{self.c_bet_denom}, Donk={self.donk_num}/{self.donk_denom}, " \
               f"Limp={self.limp_num}/{self.limp_denom})"

class Game(Base):
    __tablename__="games"
    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date)
    name = Column("name", String)
    players = relationship(
        'Players',
        secondary=association_table,
        back_populates='games'
    )
    
    def __init__(self, id, date, name):
        self.id = id
        self.date = date
        self.name = name
    
    def __repr__(self):
        return f"Game(id={self.id}, date={self.date}, name='{self.name}')"
    

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# p1 = Player(1, "stepdealer", 150, 0, 0)
# session.add(p1)
# session.commit()