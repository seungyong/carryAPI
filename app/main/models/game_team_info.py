from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, MEDIUMINT, INTEGER, VARCHAR


class GameTeamInfo(db.Model):
    __table_name__ = 'game_team_info'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    game_num = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    game_id = Column(VARCHAR(15), ForeignKey('game.game_id'), nullable=False)
    team_win = Column(TINYINT, nullable=False)
    blue_baron_kills = Column(TINYINT, nullable=False, default=0)
    blue_dragon_kills = Column(TINYINT, nullable=False, default=0)
    blue_tower_kills = Column(TINYINT, nullable=False, default=0)
    blue_total_gold = Column(MEDIUMINT(unsigned=True), nullable=False, default=0)
    blue_champion_kills = Column(SMALLINT(unsigned=True), nullable=False, default=0)
    blue_champion_deaths = Column(SMALLINT(unsigned=True), nullable=False, default=0)
    blue_champion_assists = Column(SMALLINT(unsigned=True), nullable=False, default=0)
    red_baron_kills = Column(TINYINT, nullable=False, default=0)
    red_dragon_kills = Column(TINYINT, nullable=False, default=0)
    red_tower_kills = Column(TINYINT, nullable=False, default=0)
    red_total_gold = Column(MEDIUMINT(unsigned=True), nullable=False, default=0)
    red_champion_kills = Column(SMALLINT(unsigned=True), nullable=False, default=0)
    red_champion_deaths = Column(SMALLINT(unsigned=True), nullable=False, default=0)
    red_champion_assists = Column(SMALLINT(unsigned=True), nullable=False, default=0)

    def __init__(
            self, game_id, team_win, blue_baron_kills, blue_dragon_kills, blue_tower_kills,
            blue_total_gold, blue_champion_kills, blue_champion_deaths, blue_champion_assists,
            red_baron_kills, red_dragon_kills, red_tower_kills, red_total_gold,
            red_champion_kills, red_champion_deaths, red_champion_assists
    ):
        self.game_id = game_id
        self.team_win = team_win
        self.blue_baron_kills = blue_baron_kills
        self.blue_dragon_kills = blue_dragon_kills
        self.blue_tower_kills = blue_tower_kills
        self.blue_total_gold = blue_total_gold
        self.blue_champion_kills = blue_champion_kills
        self.blue_champion_deaths = blue_champion_deaths
        self.blue_champion_assists = blue_champion_assists
        self.red_baron_kills = red_baron_kills
        self.red_dragon_kills = red_dragon_kills
        self.red_tower_kills = red_tower_kills
        self.red_total_gold = red_total_gold
        self.red_champion_kills = red_champion_kills
        self.red_champion_deaths = red_champion_deaths
        self.red_champion_assists = red_champion_assists

    @property
    def serialize(self):
        return {
            'game_id': self.game_id,
            'team_win': self.team_win,
            'blue_baron_kills': self.blue_baron_kills,
            'blue_dragon_kills': self.blue_dragon_kills,
            'blue_tower_kills': self.blue_tower_kills,
            'blue_total_gold': self.blue_total_gold,
            'blue_champion_kills': self.blue_champion_kills,
            'blue_champion_deaths': self.blue_champion_deaths,
            'blue_champion_assists': self.blue_champion_assists,
            'red_baron_kills': self.red_baron_kills,
            'red_dragon_kills': self.red_dragon_kills,
            'red_tower_kills': self.red_tower_kills,
            'red_total_gold': self.red_total_gold,
            'red_champion_kills': self.red_champion_kills,
            'red_champion_deaths': self.red_champion_deaths,
            'red_champion_assists': self.red_champion_assists
        }
