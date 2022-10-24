from app import db

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import SMALLINT, VARCHAR, TIMESTAMP
from sqlalchemy.sql import func


class Game(db.Model):
    __table_name__ = 'game'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    game_id = Column(VARCHAR(15), primary_key=True, nullable=False)
    queue_id = Column(SMALLINT, nullable=False)
    puuid = Column(VARCHAR(80), nullable=False)
    game_duration = Column(VARCHAR(30), nullable=False)
    team_win = Column(VARCHAR(3), nullable=False, default=100)
    played_time = Column(VARCHAR(30), nullable=False)
    created_time = Column(TIMESTAMP, nullable=False, default=func.now())

    def __init__(
            self, game_id, queue_id, puuid, game_duration, team_win, played_time
    ):
        self.game_id = game_id
        self.queue_id = queue_id
        self.puuid = puuid
        self.game_duration = game_duration
        self.team_win = team_win
        self.played_time = played_time

    @property
    def serialize(self):
        return {
            'game_id': self.game_id,
            'queue_id': self.queue_id,
            'puuid': self.puuid,
            'game_duration': self.game_duration,
            'team_win': self.team_win,
            'played_time': self.played_time,
            'created_time': str(self.created_time)
        }
