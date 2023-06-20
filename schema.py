from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    String,
    Integer,
    Float,
    Date,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("player_id", ForeignKey("players.id")),
    Column("game_id", ForeignKey("games.id")),
)


class PlayerTable(Base):
    __tablename__ = "players"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
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
        "Game_Table", secondary=association_table, back_populates="players"
    )

    def __init__(
        self,
        username,
        net,
        vpip_num,
        vpip_denom,
        uopfr_num,
        uopfr_denom,
        pfr_num,
        pfr_denom,
        threebet_num,
        threebet_denom,
        fourbet_num,
        fourbet_denom,
        fold_to_three_num,
        fold_to_three_denom,
        c_bet_num,
        c_bet_denom,
        donk_num,
        donk_denom,
        limp_num,
        limp_denom,
    ):
        self.username = username
        self.net = net
        self.VPIP_num = vpip_num
        self.VPIP_denom = vpip_denom
        self.UOPFR_num = uopfr_num
        self.UOPFR_denom = uopfr_denom
        self.PFR_num = pfr_num
        self.PFR_denom = pfr_denom
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
        return (
            f"PlayerStats(id={self.id}, username='{self.username}', net={self.net}, "
            f"VPIP={self.VPIP_num}/{self.VPIP_denom}, UOPFR={self.UOPFR_num}/{self.UOPFR_denom}"
            f"PFR={self.PFR_num}/{self.PFR_denom}, 3Bet={self.threebet_num}/{self.threebet_denom}, "
            f"4Bet={self.fourbet_num}/{self.fourbet_denom}"
            f"FoldTo3Bet={self.fold_to_three_num}/{self.fold_to_three_denom}, "
            f"C-Bet={self.c_bet_num}/{self.c_bet_denom}, Donk={self.donk_num}/{self.donk_denom}, "
            f"Limp={self.limp_num}/{self.limp_denom})"
        )


class GameTable(Base):
    __tablename__ = "games"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    date = Column("date", Date)
    name = Column("name", String)
    players = relationship(
        "Player_Table", secondary=association_table, back_populates="games"
    )

    def __init__(self, date, name):
        self.date = date
        self.name = name

    def __repr__(self):
        return f"Game(id={self.id}, date={self.date}, name='{self.name}')"


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
engine.dispose()
