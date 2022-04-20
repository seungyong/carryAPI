from app import db
from flask_restx import fields, marshal

response_fields = {
    'spell_id': fields.String(),
    'name': fields.String(),
    'description': fields.String(),
    'cooldown': fields.Integer(),
}

dummy_data = {
    'spell_id': 'SummonerFlash',
    'name': '점멸',
    'description': '커서 방향으로 챔피언이 짧은 거리를 순간이동합니다.',
    'cooldown': 300
}


def response_model():
    return marshal(dummy_data, response_fields)


class Spell(db.Model):
    __table_name__ = 'spell'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    spell_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    cooldown = db.Column(db.Integer, nullable=False)

    def __init__(
            self, spell_id, name, description, cooldown
    ):
        self.spell_id = spell_id
        self.name = name
        self.description = description
        self.cooldown = cooldown

    def __repr__(self):
        return f"""
            spell_id = {self.spell_id}\n
            name = {self.name}\n
            description = {self.description}\n
            cooldown = {self.cooldown}\n
        """

    @property
    def serialize(self):
        return {
            'spell_id': self.spell_id,
            'name': self.name,
            'description': self.description,
            'cooldown': self.cooldown
        }
