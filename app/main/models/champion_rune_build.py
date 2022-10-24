from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER, VARCHAR


class ChampionRuneBuild(db.Model):
    __table_name__ = 'champion_rune_build'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    rune_build_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), nullable=False)
    primary_rune_build = Column(VARCHAR(30), nullable=False)
    sub_rune_build = Column(VARCHAR(25))
    stat = Column(VARCHAR(5), nullable=False)
    total_win = Column(INTEGER, nullable=False)
    total_lose = Column(INTEGER, nullable=False)

    def __init__(
            self, rune_build_id, champion_id, primary_rune_build, sub_rune_build, stat, total_win, total_lose
    ):
        self.rune_build_id = rune_build_id
        self.champion_id = champion_id
        self.primary_rune_build = primary_rune_build
        self.sub_rune_build = sub_rune_build
        self.stat = stat
        self.total_win = total_win
        self.total_lose = total_lose

    @property
    def serialize(self):
        return {
            'rune_build_id': self.rune_build_id,
            'champion_id': self.champion_id,
            'primary_rune_build': self.primary_rune_build,
            'sub_rune_build': self.sub_rune_build,
            'stat': self.stat,
            'total_win': self.total_win,
            'total_lose': self.total_lose
        }
