from app import db
from flask_restx import fields, marshal

response_all_fields = {
    'champion_id': fields.Integer(),
    'champion_name': fields.String(),
    'eng_name': fields.String(),
    'sub_name': fields.String(),
    'description': fields.String(),
    'position': fields.String(),
    'tags': fields.String(),
    'difficulty': fields.Integer(),
    'hp': fields.String(),
    'hp_per_level': fields.String(),
    'mp': fields.String(),
    'mp_per_level': fields.String(),
    'move_speed': fields.Integer(),
    'armor': fields.Integer(),
    'armor_per_level': fields.Float(),
    'attack_range': fields.Integer(),
    'attack_damage': fields.Integer(),
    'attack_damage_per_level': fields.Integer(),
    'attack_speed': fields.Float(),
    'attack_speed_per_level': fields.Float(),
}

dummy_all_data = {
    "champion_id": 266,
    "champion_name": "아트록스",
    "eng_name": "Aatrox",
    "sub_name": "다르킨의 검",
    "description": "한때는 공허에 맞서 싸웠던 슈리마의 명예로운 수호자 아트록스와 그의 종족은 결국 공허보다 위험한 존재가 되어 룬테라의 존속을 위협했지만, 교활한 필멸자의 마법에 속아넘어가 "
                   "패배하게 되었다. 수백 년에 걸친 봉인 끝에, 아트록스는 자신의 정기가 깃든 마법 무기를 휘두르는 어리석은 자들을 타락시키고 육신을 바꾸는 것으로 다시 한번 자유의 길을 "
                   "찾아내었다. 이제 이전의 잔혹한 모습을 닮은 육체를 차지한 아트록스는 세상의 종말과 오랫동안 기다려온 복수를 열망한다.",
    "position": "TOP",
    "tags": "Fighter,Tank",
    "difficulty": 4,
    "hp": 580,
    "hp_per_level": 90,
    "mp": 0,
    "mp_per_level": 0,
    "move_speed": 345,
    "armor": 38,
    "armor_per_level": 3.25,
    "attack_range": 175,
    "attack_damage": 60,
    "attack_damage_per_level": 5,
    "attack_speed": 0.651,
    "attack_speed_per_level": 2.5
}

response_name_fields = {
    'champion_id': fields.Integer(),
    'champion_name': fields.String(),
    'eng_name': fields.String(),
}

dummy_name_data = {
    "champion_id": 266,
    "champion_name": "아트록스",
    "eng_name": "Aatrox",
}


def response_all_model():
    return marshal(dummy_all_data, response_all_fields)


def response_name_model():
    return marshal(dummy_name_data, response_name_fields)


class Champion(db.Model):
    __table_name__ = 'champion'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    champion_id = db.Column(db.Integer, primary_key=True, unique=True)
    champion_name = db.Column(db.String(10), unique=True, nullable=False)
    eng_name = db.Column(db.String(15), unique=True, nullable=False)
    sub_name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(300))
    position = db.Column(db.String(20), nullable=False)
    tags = db.Column(db.String(30))
    difficulty = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, nullable=False)
    hp_per_level = db.Column(db.Integer, nullable=False)
    mp = db.Column(db.Integer, default=0)
    mp_per_level = db.Column(db.Integer, default=0)
    move_speed = db.Column(db.Integer, nullable=False)
    armor = db.Column(db.Integer, nullable=False)
    armor_per_level = db.Column(db.Float(precision=5), nullable=False)
    attack_range = db.Column(db.Integer, nullable=False)
    attack_damage = db.Column(db.Integer, nullable=False)
    attack_damage_per_level = db.Column(db.Float(precision=5), nullable=False)
    attack_speed = db.Column(db.Float(precision=5), nullable=False)
    attack_speed_per_level = db.Column(db.Float(precision=5), nullable=False)

    def __init__(
            self, champion_id, champion_name, eng_name, sub_name, description,
            position, tags, difficulty, hp, hp_per_level, mp, mp_per_level, move_speed,
            armor, armor_per_level, attack_range, attack_damage, attack_damage_per_level,
            attack_speed, attack_speed_per_level

    ):
        self.champion_id = champion_id
        self.champion_name = champion_name
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

    def __repr__(self):
        return f"""
            champion_id = {self.champion_id}
            champion_name = {self.champion_name}
            eng_name = {self.eng_name}
            sub_name = {self.sub_name}
            description = {self.description}
            position = {self.position}
            tags = {self.tags}
            difficulty = {self.difficulty}
            hp = {self.hp}
            hp_per_level = {self.hp_per_level}
            mp = {self.mp}
            mp_per_level = {self.mp_per_level}
            move_speed = {self.move_speed}
            armor = {self.armor}
            armor_per_level = {self.armor_per_level}
            attack_range = {self.attack_range}
            attack_damage = {self.attack_damage}
            attack_damage_per_level = {self.attack_damage_per_level}
            attack_speed = {self.attack_speed}
            attack_speed_per_level = {self.attack_speed_per_level}
        """

    # SQLObject to Dict
    # property 데코레이터를 사용해 Class.serialize를 호출하면 return의 값이 반환됨
    @property
    def serialize(self):
        return {
            'champion_id': self.champion_id,
            'champion_name': self.champion_name,
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
            'armor_per_level': self.armor_per_level,
            'attack_range': self.attack_range,
            'attack_damage': self.attack_damage,
            'attack_damage_per_level': self.attack_damage_per_level,
            'attack_speed': self.attack_speed,
            'attack_speed_per_level': self.attack_speed_per_level
        }

    @property
    def name_serialize(self):
        return {
            'champion_id': self.champion_id,
            'champion_name': self.champion_name,
            'eng_name': self.eng_name
        }
