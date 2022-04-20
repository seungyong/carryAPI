import time

from app import db
from flask_restx import fields, marshal
from sqlalchemy.sql import func

response_fields = {
    'summoner_id': fields.String(),
    'puuid': fields.String(),
    'profile_id': fields.Integer(),
    'username': fields.String(),
    'level': fields.Integer(),
    'solo_tier': fields.String(),
    'solo_rank': fields.String(),
    'solo_point': fields.Integer(),
    'flex_tier': fields.String(),
    'flex_rank': fields.String(),
    'flex_point': fields.Integer(),
    'total_win': fields.Integer(),
    'total_lose': fields.Integer(),
    'created_time': fields.String()
}

dummy_data = {
    'summoner_id': 'vumohJCQwV-DEMRFQQqo4iTsxtSclzaQ00Sh0k6T4y2QFao',
    'puuid': 'JHHvASQ2PcvLVWIyzGo2hY8ZBjf35DjyiVjSV4nQ5x70RJfSQAbP0EbZAOzm8Mn-ayoCSSlXUPoJSA',
    'profile_id': 4571,
    'username': '중복파일',
    'level': 178,
    'solo_tier': 'SILVER',
    'solo_rank': 'II',
    'solo_point': 53,
    'flex_tier': 'GOLD',
    'flex_rank': 'I',
    'flex_point': 100,
    'total_win': 38,
    'total_lose': 48,
    'created_time': '2022-03-28 23:08:47'
}


def response_model():
    return marshal(dummy_data, response_fields)


class Player(db.Model):
    __table_name__ = 'player'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    summoner_id = db.Column(db.String(100), primary_key=True, nullable=False)
    puuid = db.Column(db.String(80), unique=True, nullable=False)
    profile_icon_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    solo_tier = db.Column(db.String(10))
    solo_rank = db.Column(db.CHAR(3))
    solo_point = db.Column(db.Integer)
    flex_tier = db.Column(db.String(10))
    flex_rank = db.Column(db.CHAR(3))
    flex_point = db.Column(db.Integer)
    total_win = db.Column(db.Integer)
    total_lose = db.Column(db.Integer)
    created_time = db.Column(db.TIMESTAMP, nullable=False, default=func.now())

    def __init__(
            self, summoner_id='', puuid='', profile_icon_id=0, username='', level=0,
            solo_tier='', solo_rank='', solo_point=0, flex_tier='', flex_rank='', flex_point=0,
            total_win=0, total_lose=0
    ):
        self.summoner_id = summoner_id
        self.puuid = puuid
        self.profile_icon_id = profile_icon_id
        self.username = username
        self.level = level
        self.solo_tier = solo_tier
        self.solo_rank = solo_rank
        self.solo_point = solo_point
        self.flex_tier = flex_tier
        self.flex_rank = flex_rank
        self.flex_point = flex_point
        self.total_win = total_win
        self.total_lose = total_lose

    @property
    def serialize(self):
        return {
            'summoner_id': self.summoner_id,
            'puuid': self.puuid,
            'profile_icon_id': self.profile_icon_id,
            'username': self.username,
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
