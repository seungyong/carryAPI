import time

from app import db

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy.sql import func



class Player(db.Model):
    __table_name__ = 'player'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    summoner_id = Column(VARCHAR(100), primary_key=True)
    puuid = Column(VARCHAR(80), unique=True, nullable=False)
    profile_icon_id = Column(SMALLINT, nullable=False)
    summoner_name = Column(VARCHAR(30), unique=True, nullable=False)
    level = Column(SMALLINT, nullable=False)
    solo_tier = Column(VARCHAR(10), nullable=False, default='Unranked')
    solo_rank = Column(TINYINT, nullable=False, default=5)
    solo_point = Column(TINYINT, nullable=False, default=0)
    flex_tier = Column(VARCHAR(10), nullable=False, default='Unranked')
    flex_rank = Column(TINYINT, nullable=False, default=5)
    flex_point = Column(TINYINT, nullable=False, default=0)
    total_win = Column(INTEGER, default=0)
    total_lose = Column(INTEGER, default=0)
    created_time = Column(TIMESTAMP, default=func.now())

    def __init__(
            self, summoner_id='', puuid='', profile_icon_id=0, summoner_name='', level=0,
            solo_tier='Unranked', solo_rank=5, solo_point=0, flex_tier='Unranked', flex_rank=5, flex_point=0,
            total_win=0, total_lose=0, created_time = func.now()
    ):
        self.summoner_id = summoner_id
        self.puuid = puuid
        self.profile_icon_id = profile_icon_id
        self.summoner_name = summoner_name
        self.level = level
        self.solo_tier = solo_tier
        self.solo_rank = solo_rank
        self.solo_point = solo_point
        self.flex_tier = flex_tier
        self.flex_rank = flex_rank
        self.flex_point = flex_point
        self.total_win = total_win
        self.total_lose = total_lose
        self.created_time = created_time

    @property
    def serialize(self):
        return {
            'summoner_id': self.summoner_id,
            'puuid': self.puuid,
            'profile_icon_id': self.profile_icon_id,
            'summoner_name': self.summoner_name,
            'level': self.level,
            'solo_tier': self.solo_tier,
            'solo_rank': self.solo_rank,
            'solo_point': self.solo_point,
            'flex_tier': self.flex_tier,
            'flex_rank': self.flex_rank,
            'flex_point': self.flex_point,
            'total_win': self.total_win,
            'total_lose': self.total_lose,
            'created_time': str(self.created_time)
        }
