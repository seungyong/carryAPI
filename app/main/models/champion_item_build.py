from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER


class ChampionItemBuild(db.Model):
    __table_name__ = 'champion_item_build'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    item_build_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), nullable=False)
    item0_id = Column(SMALLINT, nullable=False)
    item1_id = Column(SMALLINT, nullable=False)
    item2_id = Column(SMALLINT, nullable=False)
    total_win = Column(INTEGER, nullable=False)
    total_lose = Column(INTEGER, nullable=False)
    sample_match = Column(INTEGER, nullable=False)

    def __init__(
            self, item_build_id, champion_id, item0_id, item1_id, item2_id, total_win, total_lose, sample_match
    ):
        self.item_build_id = item_build_id
        self.champion_id = champion_id
        self.item0_id = item0_id
        self.item1_id = item1_id
        self.item2_id = item2_id
        self.total_win = total_win
        self.total_lose = total_lose
        self.sample_match = sample_match

    @property
    def serialize(self):
        return {
            'item_build_id': self.item_build_id,
            'champion_id': self.champion_id,
            'item0_id': self.item0_id,
            'item1_id': self.item1_id,
            'item2_id': self.item2_id,
            'total_win': self.total_win,
            'total_lose': self.total_lose,
            'sample_match': self.sample_match
        }
