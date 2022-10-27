from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, DECIMAL


class ChampionBasic(db.Model):
    __table_name__ = 'champion_basic'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    position_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), nullable=False)
    position = Column(VARCHAR(20))
    score = Column(DECIMAL(5, 3), nullable=False)
    current_tier = Column(TINYINT, nullable=False, default=5)
    prev_tier = Column(TINYINT, nullable=False, default=5)
    total_ban = Column(INTEGER(unsigned=True), nullable=False)
    total_pick = Column(INTEGER(unsigned=True), nullable=False)
    total_win = Column(INTEGER(unsigned=True), nullable=False)
    total_lose = Column(INTEGER(unsigned=True), nullable=False)
    total_match = Column(INTEGER(unsigned=True), nullable=False)

    def __init__(
            self, champion_id, position, score, current_tier, prev_tier,
            total_ban, total_pick, total_win, total_lose, total_match
    ):
        self.champion_id = champion_id
        self.position = position
        self.score = score
        self.current_tier = current_tier
        self.prev_tier = prev_tier
        self.total_ban = total_ban
        self.total_pick = total_pick
        self.total_win = total_win
        self.total_lose = total_lose
        self.total_match = total_match

    @property
    def serialize(self):
        return {
            'champion_id': self.champion_id,
            'position': self.position,
            'score': self.score,
            'current_tier': self.current_tier,
            'prev_tier': self.prev_tier,
            'total_ban': self.total_ban,
            'total_pick': self.total_pick,
            'total_win': self.total_win,
            'total_lose': self.total_lose,
            'total_match': self.total_match,
        }
