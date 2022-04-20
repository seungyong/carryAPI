from app import db
from flask_restx import fields, marshal
from sqlalchemy.sql import func

response_fields = {
    'game_id': fields.String(),
    'puuid': fields.String(),
    'game_duration': fields.String(),
    'played_time': fields.String(),
    'created_time': fields.String()
}

dummy_data = {
    'game_id': 'JHHvASQ2PcvLVWIyzGo2hY8ZBjf35DjyiVjSV4nQ5x70RJfSQAbP0EbZAOzm8Mn-ayoCSSlXUPoJSA',
    'puuid': 'KR_5219417009',
    'game_duration': '1715542',
    'played_time': '1621910319279',
    'created_time': '2022-03-28 23:08:47'
}


def response_model():
    return marshal(dummy_data, response_fields)


class Game(db.Model):
    __table_name__ = 'game'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    game_id = db.Column(db.String(15), primary_key=True, nullable=False)
    queue_id = db.Column(db.Integer, nullable=False)
    puuid = db.Column(db.String(80), nullable=False)
    game_duration = db.Column(db.String(30), nullable=False)
    played_time = db.Column(db.String(30), nullable=False)
    created_time = db.Column(db.TIMESTAMP, nullable=False, default=func.now())

    def __init__(
            self, game_id, queue_id, puuid, game_duration, played_time
    ):
        self.game_id = game_id
        self.queue_id = queue_id
        self.puuid = puuid
        self.game_duration = game_duration
        self.played_time = played_time

    def __repr__(self):
        return f"""
            game_id = {self.game_id}\n
            queue_id = {self.queue_id}\n
            puuid = {self.puuid}\n
            game_duration = {self.game_duration}\n
            played_time = {self.played_time}\n
            created_time = {self.created_time}\n
        """

    @property
    def serialize(self):
        return {
            'game_id': self.game_id,
            'queue_id': self.queue_id,
            'puuid': self.puuid,
            'game_duration': self.game_duration,
            'played_time': self.played_time,
            'created_time': str(self.created_time)
        }
