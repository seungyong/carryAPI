from app import db

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, DECIMAL


class Champion(db.Model):
    __table_name__ = 'champion'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    champion_id = Column(SMALLINT, primary_key=True)
    kor_name = Column(VARCHAR(10), unique=True, nullable=False)
    eng_name = Column(VARCHAR(15), unique=True, nullable=False)
    sub_name = Column(VARCHAR(30), unique=True, nullable=False)
    description = Column(VARCHAR(300))
    tags = Column(VARCHAR(30))
    difficulty = Column(TINYINT, default=0)
    hp = Column(SMALLINT, nullable=False)
    hp_per_level = Column(TINYINT(unsigned=True), nullable=False)
    mp = Column(SMALLINT, default=0)
    mp_per_level = Column(TINYINT(unsigned=True), default=0)
    move_speed = Column(SMALLINT, nullable=False)
    armor = Column(TINYINT(unsigned=True), nullable=False)
    armor_per_level = Column(DECIMAL(5, 3), nullable=False)
    attack_range = Column(SMALLINT, nullable=False)
    attack_damage = Column(SMALLINT, nullable=False)
    attack_damage_per_level = Column(DECIMAL(5, 3), nullable=False)
    attack_speed = Column(DECIMAL(5, 3), nullable=False)
    attack_speed_per_level = Column(DECIMAL(5, 3), nullable=False)
    ad_damage_percent = Column(TINYINT, nullable=False)
    ap_damage_percent = Column(TINYINT, nullable=False)

    def __init__(
            self, champion_id, kor_name, eng_name, sub_name, description,
            tags, difficulty, hp, hp_per_level, mp, mp_per_level, move_speed,
            armor, armor_per_level, attack_range, attack_damage, attack_damage_per_level,
            attack_speed, attack_speed_per_level, ad_damage_percent, ap_damage_percent,
    ):
        self.champion_id = champion_id
        self.kor_name = kor_name
        self.eng_name = eng_name
        self.sub_name = sub_name
        self.description = description
        self.tags = tags
        self.difficulty = difficulty
        self.hp = hp
        self.hp_per_level = hp_per_level
        self.mp = mp
        self.mp_per_level = mp_per_level
        self.move_speed = move_speed
        self.armor = armor
        self.armor_per_level = armor_per_level
        self.attack_range = attack_range
        self.attack_damage = attack_damage
        self.attack_damage_per_level = attack_damage_per_level
        self.attack_speed = attack_speed
        self.attack_speed_per_level = attack_speed_per_level
        self.ad_damage_percent = ad_damage_percent
        self.ap_damage_percent = ap_damage_percent

    # SQLObject to Dict
    # property 데코레이터를 사용해 Class.serialize를 호출하면 return의 값이 반환됨
    @property
    def serialize(self):
        return {
            'champion_id': self.champion_id,
            'kor_name': self.kor_name,
            'eng_name': self.eng_name,
            'sub_name': self.sub_name,
            'description': self.description,
            'tags': self.tags,
            'difficulty': self.difficulty,
            'hp': self.hp,
            'hp_per_level': self.hp_per_level,
            'mp': self.mp,
            'mp_per_level': self.mp_per_level,
            'move_speed': self.move_speed,
            'armor': self.armor,
            'armor_per_level': self.armor_per_level,
            'attack_range': self.attack_range,
            'attack_damage': self.attack_damage,
            'attack_damage_per_level': self.attack_damage_per_level,
            'attack_speed': self.attack_speed,
            'attack_speed_per_level': self.attack_speed_per_level,
            'ad_damage_percent': self.ad_damage_percent,
            'ap_damage_percent': self.ap_damage_percent,
        }
