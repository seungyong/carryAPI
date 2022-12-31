from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, MEDIUMINT, INTEGER, VARCHAR, BOOLEAN


class GamePlayer(db.Model):
    __table_name__ = 'game_player'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    game_num = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    game_id = Column(VARCHAR(15), ForeignKey('game.game_id'), nullable=False)
    team_id = Column(VARCHAR(3), nullable=False)
    puuid = Column(VARCHAR(80), nullable=False)
    summoner_id = Column(VARCHAR(100), nullable=False)
    summoner_name = Column(VARCHAR(30), nullable=False)
    champion_id = Column(SMALLINT, nullable=False)
    champion_level = Column(TINYINT, default=1)
    item0_id = Column(SMALLINT, default=-1)
    item1_id = Column(SMALLINT, default=-1)
    item2_id = Column(SMALLINT, default=-1)
    item3_id = Column(SMALLINT, default=-1)
    item4_id = Column(SMALLINT, default=-1)
    item5_id = Column(SMALLINT, default=-1)
    item6_id = Column(SMALLINT, default=-1)
    primary_rune_build = Column(VARCHAR(30), nullable=False)
    sub_rune_build = Column(VARCHAR(25), nullable=False)
    stat = Column(VARCHAR(5), nullable=False)
    skill_build = Column(VARCHAR(35), nullable=False)
    team_position = Column(VARCHAR(10), nullable=False)
    first_blood = Column(BOOLEAN, default=False)
    kills = Column(TINYINT(unsigned=True), default=0)
    deaths = Column(TINYINT(unsigned=True), default=0)
    assists = Column(TINYINT(unsigned=True), default=0)
    max_kill_type = Column(VARCHAR(15), default='')
    total_damage_to_champions = Column(MEDIUMINT, default=0)
    cs = Column(MEDIUMINT(unsigned=True), default=0)
    gold_earned = Column(MEDIUMINT, default=0)
    vision_score = Column(TINYINT, default=0)
    wards_placed = Column(TINYINT(unsigned=True), default=0)
    control_wards_placed = Column(TINYINT(unsigned=True), default=0)
    summoner1_id = Column(VARCHAR(50), nullable=False)
    summoner2_id = Column(VARCHAR(50), nullable=False)

    def __init__(
            self, game_id, team_id, puuid, summoner_id, summoner_name, champion_id,
            champion_level, item0_id, item1_id, item2_id, item3_id, item4_id, item5_id,
            item6_id, primary_rune_build, sub_rune_build, stat, skill_build,
            team_position, first_blood, kills, deaths, assists, max_kill_type,
            total_damage_to_champions, cs, gold_earned, vision_score, wards_placed, control_wards_placed,
            summoner1_id, summoner2_id
    ):
        self.game_id = game_id
        self.team_id = team_id
        self.puuid = puuid
        self.summoner_id = summoner_id
        self.summoner_name = summoner_name
        self.champion_id = champion_id
        self.champion_level = champion_level
        self.item0_id = item0_id
        self.item1_id = item1_id
        self.item2_id = item2_id
        self.item3_id = item3_id
        self.item4_id = item4_id
        self.item5_id = item5_id
        self.item6_id = item6_id
        self.primary_rune_build = primary_rune_build
        self.sub_rune_build = sub_rune_build
        self.stat = stat
        self.skill_build = skill_build
        self.team_position = team_position
        self.first_blood = first_blood
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.max_kill_type = max_kill_type
        self.total_damage_to_champions = total_damage_to_champions
        self.cs = cs
        self.gold_earned = gold_earned
        self.vision_score = vision_score
        self.wards_placed = wards_placed
        self.control_wards_placed = control_wards_placed
        self.summoner1_id = summoner1_id
        self.summoner2_id = summoner2_id

    @property
    def serialize(self):
        return {
            'game_id': self.game_id,
            'team_id': self.team_id,
            'puuid': self.puuid,
            'summoner_id': self.summoner_id,
            'summoner_name': self.summoner_name,
            'champion_id': self.champion_id,
            'champion_level': self.champion_level,
            'item0_id': self.item0_id,
            'item1_id': self.item1_id,
            'item2_id': self.item2_id,
            'item3_id': self.item3_id,
            'item4_id': self.item4_id,
            'item5_id': self.item5_id,
            'item6_id': self.item6_id,
            'primary_rune_build': self.primary_rune_build,
            'sub_rune_build': self.sub_rune_build,
            'stat': self.stat,
            'skill_build': self.skill_build,
            'team_position': self.team_position,
            'first_blood': self.first_blood,
            'kills': self.kills,
            'deaths': self.deaths,
            'assists': self.assists,
            'max_kill_type': self.max_kill_type,
            'total_damage_to_champions': self.total_damage_to_champions,
            'cs': self.cs,
            'gold_earned': self.gold_earned,
            'vision_score': self.vision_score,
            'wards_placed': self.wards_placed,
            'control_wards_placed': self.control_wards_placed,
            'summoner1_id': self.summoner1_id,
            'summoner2_id': self.summoner2_id,
        }
