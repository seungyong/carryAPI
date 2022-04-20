from app import db
from flask_restx import fields, marshal

response_fields = {
    'game_id': fields.String(),
    'team_win': fields.Integer(),
    'blue_baron_kills': fields.Integer(),
    'blue_dragon_kills': fields.Integer(),
    'blue_tower_kills': fields.Integer(),
    'blue_champion_kills': fields.Integer(),
    'blue_total_gold': fields.Integer(),
    'red_baron_kills': fields.Integer(),
    'red_dragon_kills': fields.Integer(),
    'red_tower_kills': fields.Integer(),
    'red_champion_kills': fields.Integer(),
    'red_total_gold': fields.Integer(),
}

dummy_data = {
    'game_id': 'KR_5799387823',
    'team_win': 100,
    'blue_baron_kills': 1,
    'blue_dragon_kills': 2,
    'blue_tower_kills': 9,
    'blue_champion_kills': 24,
    'blue_total_gold': 59297,
    'red_baron_kills': 0,
    'red_dragon_kills': 2,
    'red_tower_kills': 3,
    'red_champion_kills': 24,
    'red_total_gold': 55371,
}


def response_model():
    return marshal(dummy_data, response_fields)


class GameTeamInfo(db.Model):
    __table_name__ = 'game_team_info'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    game_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.String(15), db.ForeignKey('game.game_id'), nullable=False)
    team_win = db.Column(db.Integer, nullable=False)
    blue_baron_kills = db.Column(db.Integer, default=0)
    blue_dragon_kills = db.Column(db.Integer, default=0)
    blue_tower_kills = db.Column(db.Integer, default=0)
    blue_champion_kills = db.Column(db.Integer, default=0)
    blue_total_gold = db.Column(db.Integer, default=0)
    red_baron_kills = db.Column(db.Integer, default=0)
    red_dragon_kills = db.Column(db.Integer, default=0)
    red_tower_kills = db.Column(db.Integer, default=0)
    red_champion_kills = db.Column(db.Integer, default=0)
    red_total_gold = db.Column(db.Integer, default=0)

    def __init__(
            self, game_id, team_win, blue_baron_kills, blue_dragon_kills, blue_tower_kills,
            blue_champion_kills, blue_total_gold, red_baron_kills,
            red_dragon_kills, red_tower_kills, red_champion_kills, red_total_gold
    ):
        self.game_id = game_id
        self.team_win = team_win
        self.blue_baron_kills = blue_baron_kills
        self.blue_dragon_kills = blue_dragon_kills
        self.blue_tower_kills = blue_tower_kills
        self.blue_champion_kills = blue_champion_kills
        self.blue_total_gold = blue_total_gold
        self.red_baron_kills = red_baron_kills
        self.red_dragon_kills = red_dragon_kills
        self.red_tower_kills = red_tower_kills
        self.red_champion_kills = red_champion_kills
        self.red_total_gold = red_total_gold

    @property
    def serialize(self):
        return {
            'game_id': self.game_id,
            'team_win': self.team_win,
            'blue_baron_kills': self.blue_baron_kills,
            'blue_dragon_kills': self.blue_dragon_kills,
            'blue_tower_kills': self.blue_tower_kills,
            'blue_champion_kills': self.blue_champion_kills,
            'blue_total_gold': self.blue_total_gold,
            'red_baron_kills': self.red_baron_kills,
            'red_dragon_kills': self.red_dragon_kills,
            'red_tower_kills': self.red_tower_kills,
            'red_champion_kills': self.red_champion_kills,
            'red_total_gold': self.red_total_gold,
        }
