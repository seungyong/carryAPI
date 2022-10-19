from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER, VARCHAR


class ChampionSpellBuild(db.Model):
    __table_name__ = 'champion_spell_build'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    spell_build_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), nullable=False)
    spell0_id = Column(VARCHAR(50), nullable=False)
    spell1_id = Column(VARCHAR(50), nullable=False)
    total_win = Column(INTEGER, nullable=False)
    total_lose = Column(INTEGER, nullable=False)

    def __init__(
            self, spell_build_id, champion_id, spell0_id, spell1_id, total_win, total_lose
    ):
        self.spell_build_id = spell_build_id
        self.champion_id = champion_id
        self.spell0_id = spell0_id
        self.spell1_id = spell1_id
        self.total_win = total_win
        self.total_lose = total_lose

    @property
    def serialize(self):
        return {
            'spell_build_id': self.spell_build_id,
            'champion_id': self.champion_id,
            'spell0_id': self.spell0_id,
            'spell1_id': self.spell1_id,
            'total_win': self.total_win,
            'total_lose': self.total_lose
        }
