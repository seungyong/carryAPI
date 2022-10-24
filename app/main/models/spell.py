from app import db

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import SMALLINT, VARCHAR


class Spell(db.Model):
    __table_name__ = 'spell'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    spell_id = Column(VARCHAR(50), primary_key=True)
    name = Column(VARCHAR(20), nullable=False)
    description = Column(VARCHAR(150), nullable=False)
    cooldown = Column(SMALLINT, nullable=False)

    def __init__(
            self, spell_id, name, description, cooldown
    ):
        self.spell_id = spell_id
        self.name = name
        self.description = description
        self.cooldown = cooldown

    @property
    def serialize(self):
        return {
            'spell_id': self.spell_id,
            'name': self.name,
            'description': self.description,
            'cooldown': self.cooldown
        }
