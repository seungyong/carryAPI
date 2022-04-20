from app import db
from flask_restx import fields, marshal

response_fields = {
    'game_id': fields.String(),
    'team_id': fields.Integer(),
    'puuid': fields.String(),
    'summoner_id': fields.String(),
    'summoner_name': fields.String(),
    'champion_id': fields.Integer(),
    'champion_level': fields.Integer(),
    'item0_id': fields.Integer(),
    'item1_id': fields.Integer(),
    'item2_id': fields.Integer(),
    'item3_id': fields.Integer(),
    'item4_id': fields.Integer(),
    'item5_id': fields.Integer(),
    'item6_id': fields.Integer(),
    'team_position': fields.String(),
    'kda': fields.Float(),
    'first_blood': fields.String(),
    'kills': fields.Integer(),
    'deaths': fields.Integer(),
    'assists': fields.Integer(),
    'max_kill_type': fields.String(),
    'total_damage_to_champions': fields.Integer(),
    'cs': fields.Integer(),
    'gold_earned': fields.Integer(),
    'vision_score': fields.Integer(),
    'summoner1_id': fields.Integer(),
    'summoner2_id': fields.Integer(),
}

dummy_data = {
    'game_id': 'KR_5799387823',
    'team_id': 200,
    'puuid': 'JHHvASQ2PcvLVWIyzGo2hY8ZBjf35DjyiVjSV4nQ5x70RJfSQAbP0EbZAOzm8Mn-ayoCSSlXUPoJSA',
    'summoner_id': 'vumohJCQwV-DEMRFQQqo4iTsxtSclzaQ00Sh0k6T4y2QFao',
    'summoner_name': '중복파일',
    'champion_id': 875,
    'champion_level': 16,
    'item0_id': 3044,
    'item1_id': 1037,
    'item2_id': 6630,
    'item3_id': 3181,
    'item4_id': 1028,
    'item5_id': 3047,
    'item6_id': 3364,
    'team_position': 'TOP',
    'kda': 7.5,
    'first_blood': 0,
    'kills': 2,
    'deaths': 2,
    'assists': 13,
    'max_kill_type': '',
    'total_damage_to_champions': 16781,
    'cs': 208,
    'gold_earned': 11378,
    'vision_score': 19,
    'summoner1_id': 12,
    'summoner2_id': 4,
}


def response_model():
    return marshal(dummy_data, response_fields)


class GamePlayer(db.Model):
    __table_name__ = 'game_player'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    game_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.String(15), db.ForeignKey('game.game_id'), nullable=False)
    team_id = db.Column(db.Integer, nullable=False)
    puuid = db.Column(db.String(80), nullable=False)
    summoner_id = db.Column(db.String(100), nullable=False)
    summoner_name = db.Column(db.String(30), nullable=False)
    champion_id = db.Column(db.Integer, nullable=False)
    champion_level = db.Column(db.Integer, default=1)
    item0_id = db.Column(db.Integer, default=-1)
    item1_id = db.Column(db.Integer, default=-1)
    item2_id = db.Column(db.Integer, default=-1)
    item3_id = db.Column(db.Integer, default=-1)
    item4_id = db.Column(db.Integer, default=-1)
    item5_id = db.Column(db.Integer, default=-1)
    item6_id = db.Column(db.Integer, default=-1)
    team_position = db.Column(db.String(10), nullable=False)
    kda = db.Column(db.Float(precision=5), default=0)
    first_blood = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    max_kill_type = db.Column(db.String(15), default='')
    total_damage_to_champions = db.Column(db.Integer, default=0)
    cs = db.Column(db.Integer, default=0)
    gold_earned = db.Column(db.Integer, default=0)
    vision_score = db.Column(db.Integer, default=0)
    summoner1_id = db.Column(db.Integer, nullable=False)
    summoner2_id = db.Column(db.Integer, nullable=False)

    def __init__(
            self, game_id, team_id, puuid, summoner_id, summoner_name, champion_id,
            champion_level, item0_id, item1_id, item2_id, item3_id, item4_id, item5_id,
            item6_id, team_position, kda, first_blood, kills, deaths, assists, max_kill_type,
            total_damage_to_champions, cs, gold_earned, vision_score, summoner1_id, summoner2_id
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
        self.team_position = team_position
        self.kda = kda
        self.first_blood = first_blood
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.max_kill_type = max_kill_type
        self.total_damage_to_champions = total_damage_to_champions
        self.cs = cs
        self.gold_earned = gold_earned
        self.vision_score = vision_score
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
            'team_position': self.team_position,
            'kda': self.kda,
            'first_blood': self.first_blood,
            'kills': self.kills,
            'deaths': self.deaths,
            'assists': self.assists,
            'max_kill_type': self.max_kill_type,
            'total_damage_to_champions': self.total_damage_to_champions,
            'cs': self.cs,
            'gold_earned': self.gold_earned,
            'vision_score': self.vision_score,
            'summoner1_id': self.summoner1_id,
            'summoner2_id': self.summoner2_id,
        }
