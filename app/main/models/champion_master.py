from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER, VARCHAR


class ChampionMaster(db.Model):
    __table_name__ = 'champion_master'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), primary_key=True)
    summoner_id = Column(VARCHAR(100), unique=True, nullable=False)
    sample_match = Column(INTEGER, nullable=False)

    def __init__(
            self, champion_id, summoner_id, sample_match
    ):
        self.champion_id = champion_id
        self.summoner_id = summoner_id
        self.sample_match = sample_match

    @property
    def serialize(self):
        return {
            'champion_id': self.champion_id,
            'summoner_id': self.summoner_id,
            'sample_match': self.sample_match
        }
