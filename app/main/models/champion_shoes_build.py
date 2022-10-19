from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER


class ChampionShoesBuild(db.Model):
    __table_name__ = 'champion_shoes_build'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    shoes_build_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), nullable=False)
    item_id = Column(SMALLINT, nullable=False)
    total_win = Column(INTEGER, nullable=False)
    total_lose = Column(INTEGER, nullable=False)

    def __init__(
            self, shoes_build_id, champion_id, item_id, total_win, total_lose
    ):
        self.shoes_build_id = shoes_build_id
        self.champion_id = champion_id
        self.item_id = item_id
        self.total_win = total_win
        self.total_lose = total_lose

    @property
    def serialize(self):
        return {
            'shoes_build_id': self.shoes_build_id,
            'champion_id': self.champion_id,
            'item_id': self.item_id,
            'total_win': self.total_win,
            'total_lose': self.total_lose
        }
