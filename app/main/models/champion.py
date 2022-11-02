from ..util.decimal import to_first_decimal_place_cut

from app import db

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, VARCHAR, DECIMAL


class Champion(db.Model):
    __table_name__ = 'champion'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    champion_id = Column(SMALLINT, primary_key=True)
    kor_name = Column(VARCHAR(10), unique=True, nullable=False)
    eng_name = Column(VARCHAR(15), unique=True, nullable=False)
    sub_name = Column(VARCHAR(30), unique=True, nullable=False)
    description = Column(VARCHAR(300))
    position = Column(VARCHAR(20))
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

    def __init__(
            self, champion_id, kor_name, eng_name, sub_name, description, position,
            tags, difficulty, hp, hp_per_level, mp, mp_per_level, move_speed,
            armor, armor_per_level, attack_range, attack_damage, attack_damage_per_level,
            attack_speed, attack_speed_per_level
    ):
        self.champion_id = champion_id
        self.kor_name = kor_name
        self.eng_name = eng_name
        self.sub_name = sub_name
        self.description = description
        self.position = position
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
            'position': self.position,
            'tags': self.tags,
            'difficulty': self.difficulty,
            'hp': self.hp,
            'hp_per_level': self.hp_per_level,
            'mp': self.mp,
            'mp_per_level': self.mp_per_level,
            'move_speed': self.move_speed,
            'armor': self.armor,
            'armor_per_level': float(self.armor_per_level),
            'attack_range': self.attack_range,
            'attack_damage': self.attack_damage,
            'attack_damage_per_level': float(self.attack_damage_per_level),
            'attack_speed': float(self.attack_speed),
            'attack_speed_per_level': float(self.attack_speed_per_level),
        }

    @staticmethod
    def to_response_ranking(self_class, basic_class, counter_classes):
        total_match = 100000000
        win_rate = to_first_decimal_place_cut(basic_class['total_win'] / basic_class['total_match'] * 100)
        pick_rate = to_first_decimal_place_cut(basic_class['total_pick'] / total_match * 100)
        ban_rate = to_first_decimal_place_cut(basic_class['total_ban'] / total_match * 100)

        return {
            'championId': self_class['champion_id'],
            'info': {
                'korName': self_class['kor_name'],
                'engName': self_class['eng_name'],
                'subName': self_class['sub_name'],
                'description': self_class['description'],
                'position': self_class['position'],
                'tags': self_class['tags'],
                'difficulty': self_class['difficulty'],
                'hp': self_class['hp'],
                'hpPerLevel': self_class['hp_per_level'],
                'mp': self_class['mp'],
                'mpPerLevel': self_class['mp_per_level'],
                'moveSpeed': self_class['move_speed'],
                'armor': self_class['armor'],
                'armorPerLevel': float(self_class['armor_per_level']),
                'attackRange': self_class['attack_range'],
                'attackDamage': self_class['attack_damage'],
                'attackDamagePerLevel': float(self_class['attack_damage_per_level']),
                'attackSpeed': float(self_class['attack_speed']),
                'attackSpeedPerLevel': float(self_class['attack_speed_per_level']),
                'analysis': {
                    'tier': {
                        'current': basic_class['current_tier'],
                        'prev': basic_class['prev_tier'],
                        'changed': basic_class['prev_tier'] - basic_class['current_tier']
                    },
                    'damageKind': {
                        'ad': basic_class['ad_damage_percent'],
                        'ap': basic_class['ap_damage_percent']
                    },
                    'score': basic_class['score'],
                    'winRate': win_rate,
                    'pickRate': pick_rate,
                    'banRate': ban_rate,
                    'sampleMatch': basic_class['total_match']
                },
                'counter': [
                    {
                        'championId': counter_class['to_champion_id'],
                        'engName': counter_class['eng_name'],
                        'score': float(counter_class['score'])
                    }
                    for counter_class in counter_classes
                ]
            },
        }

    @staticmethod
    def to_response_name(champion):
        return {
            'championId': champion['champion_id'],
            'info': {
                'korName': champion['kor_name'],
                'engName': champion['eng_name']
            }
        }
