import json

from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    Text,
    Integer,
    Float,
    Date,
    Table,
    TypeDecorator
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from game import Game
from player import Player

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("player_id", ForeignKey("players.id")),
    Column("game_id", ForeignKey("games.id")),
)

class PlayerType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value.__dict__)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            player_data = json.loads(value)
            return Player.fromdict(player_data)
        return None

class PlayerTable(Base):
    __tablename__ = "players"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column('username', Text)
    stats = Column("stats", PlayerType)
    games = relationship(
        "Game_Table", secondary=association_table, back_populates="players"
    )

    def __init__(self, player : Player):
        self.username = player.username
        self.stats = player


class GameType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value.__dict__)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            game_data = json.loads(value)
            return Game.fromdict(game_data)
        return None


class GameTable(Base):
    __tablename__ = "games"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", Text)
    date = Column("date", Date)
    game = Column("game", GameType)

    players = relationship(
        "Player_Table", secondary=association_table, back_populates="games"
    )

    def __init__(self, game: Game):
        self.name = game.name
        self.date = game.date
        self.game = game
        

    def __repr__(self):
        return f"Game(id={self.id}, date={self.date}, name='{self.name}')"

server = 'MYSQL5048.site4now.net'
database = 'db_a53d6c_donktrk'
uid = 'a53d6c_donktrk'
password = 'donkhouse72'
driver = '{MySQL ODBC 8.0 UNICODE Driver}'
# Create the connection URL for SQLAlchemy
connection_string = f"mysql://{uid}:{password}@{server}/{database}"
engine = create_engine(connection_string, echo=True)

# Drop existing tables
# Base.metadata.drop_all(bind=engine)

# Create new empty tables
#Base.metadata.create_all(bind=engine)
#engine.dispose()
