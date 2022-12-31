from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, TIMESTAMP, VARCHAR


class TierVariation(db.Model):
    __table_name__ = 'tier_variation'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    tier_variation_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    summoner_id = Column(VARCHAR(100), ForeignKey('player.summoner_id'), nullable=False)
    solo_tier = Column(VARCHAR(10), nullable=False)
    solo_rank = Column(TINYINT, nullable=False, default=5)
    solo_point = Column(TINYINT, nullable=False, default=0)
    played_time = Column(TIMESTAMP, nullable=False)

    def __init__(
            self, summoner_id, solo_tier, solo_rank, solo_point, played_time
    ):
        self.summoner_id = summoner_id
        self.solo_tier = solo_tier
        self.solo_rank = solo_rank
        self.solo_point = solo_point
        self.played_time = played_time

    @property
    def serialize(self):
        return {
            'tier_variation_id': self.tier_variation_id,
            'summoner_id': self.summoner_id,
            'solo_tier': self.solo_tier,
            'solo_rank': self.solo_rank,
            'solo_point': self.solo_point,
            'played_time': self.played_time
        }
