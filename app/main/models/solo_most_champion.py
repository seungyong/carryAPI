from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER, VARCHAR


class SoloMostChampion(db.Model):
    __table_name__ = 'solo_most_champion'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    solo_most_id = Column(INTEGER(unsigned=True), primary_key=True, auto_increment=True)
    summoner_id = Column(VARCHAR(100), ForeignKey('player.summoner_id'))
    champion_id = Column(SMALLINT, nullable=False)
    total_kill = Column(INTEGER, nullable=False)
    total_death = Column(INTEGER, nullable=False)
    total_assist = Column(INTEGER, nullable=False)
    total_win = Column(INTEGER, nullable=False)
    total_lose = Column(INTEGER, nullable=False)
    sample_match = Column(INTEGER, nullable=False)

    def __init__(
            self, summoner_id, champion_id, total_kill, total_death, total_assist, total_win, total_lose, sample_match
    ):
        self.summoner_id = summoner_id
        self.champion_id = champion_id
        self.total_kill = total_kill
        self.total_death = total_death
        self.total_assist = total_assist
        self.total_win = total_win
        self.total_lose = total_lose
        self.sample_match = sample_match

    @property
    def serialize(self):
        return {
            'solo_most_id': self.solo_most_id,
            'summoner_id': self.summoner_id,
            'champion_id': self.champion_id,
            'total_kill': self.total_kill,
            'total_death': self.total_death,
            'total_assist': self.total_assist,
            'total_win': self.total_win,
            'total_lose': self.total_lose,
            'sample_match': self.sample_match
        }
