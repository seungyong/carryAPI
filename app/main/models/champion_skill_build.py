from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER, VARCHAR


class ChampionSkillBuild(db.Model):
    __table_name__ = 'champion_skill_build'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    skill_build_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), nullable=False)
    build = Column(VARCHAR(35), nullable=False)
    total_win = Column(INTEGER, nullable=False)
    total_lose = Column(INTEGER, nullable=False)

    def __init__(
            self, shoes_build_id, champion_id, build, total_win, total_lose
    ):
        self.shoes_build_id = shoes_build_id
        self.champion_id = champion_id
        self.build = build
        self.total_win = total_win
        self.total_lose = total_lose

    @property
    def serialize(self):
        return {
            'shoes_build_id': self.shoes_build_id,
            'champion_id': self.champion_id,
            'build': self.build,
            'total_win': self.total_win,
            'total_lose': self.total_lose
        }
