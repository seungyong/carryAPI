from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, INTEGER, VARCHAR, DECIMAL


class CounterWeakAgainst(db.Model):
    __table_name__ = 'counter_strong_against'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    counter_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), nullable=False)
    to_champion_id = Column(SMALLINT, nullable=False)
    score = Column(DECIMAL(3, 1), nullable=False)
    win = Column(INTEGER, nullable=False)
    lose = Column(INTEGER, nullable=False)
    line_kills = Column(INTEGER, nullable=False)
    line_deaths = Column(INTEGER, nullable=False)
    champion_kills = Column(INTEGER, nullable=False)
    champion_deaths = Column(INTEGER, nullable=False)
    champion_assists = Column(INTEGER, nullable=False)
    total_first_tower = Column(VARCHAR(10), nullable=False)
    team_kills = Column(INTEGER, nullable=False)
    team_assists = Column(INTEGER, nullable=False)
    sample_match = Column(INTEGER, nullable=False)

    def __init__(
            self, champion_id, to_champion_id, score, win, lose, line_kills, line_deaths, champion_kills,
            champion_deaths, champion_assists, total_first_tower, team_kills, team_assists, sample_match
    ):
        self.champion_id = champion_id
        self.to_champion_id = to_champion_id
        self.score = score
        self.win = win
        self.lose = lose
        self.line_kills = line_kills
        self.line_deaths = line_deaths
        self.champion_kills = champion_kills
        self.champion_deaths = champion_deaths
        self.champion_assists = champion_assists
        self.total_first_tower = total_first_tower
        self.team_kills = team_kills
        self.team_assists = team_assists
        self.sample_match = sample_match

    @property
    def serialize(self):
        return {
            'champion_id': self.champion_id,
            'to_champion_id': self.to_champion_id,
            'score': float(self.score),
            'win': self.win,
            'lose': self.lose,
            'line_kills': self.line_kills,
            'line_deaths': self.line_deaths,
            'champion_kills': self.champion_kills,
            'champion_deaths': self.champion_deaths,
            'champion_assists': self.champion_assists,
            'total_first_tower': self.total_first_tower,
            'team_kills': self.team_kills,
            'team_assists': self.team_assists,
            'sample_match': self.sample_match
        }
