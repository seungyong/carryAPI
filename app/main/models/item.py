from app import db
from flask_restx import fields, marshal

response_fields = {
    'item_id': fields.Integer(),
    'name': fields.String(),
    'description': fields.String(),
    'plain_text': fields.String(),
    'price': fields.Integer(),
    'sell': fields.Integer(),
    'tags': fields.String(),
    'item_grade': fields.Integer()
}

dummy_data = {
    'item_id': 4005,
    'name': '제국의 명령',
    'description': '주문력 40<br>체력 200<br>스킬 가속 '
                   '20<br>기본 마나 재생 100%<br>합동 '
                   '공격: 챔피언을 스킬로 둔화 또는 이동 불가 상태로 만들면 45~75('
                   '레벨에 비례)의 추가 마법 피해를 입히고 4초 동안 표식을 남깁니다. (챔피언 하나당 재사용 대기시간 6초) 아군이 대상에게 피해를 입히면 표식이 '
                   '폭발하며 90~150(아군 레벨에 비례)의 마법 피해를 추가로 가하고 2초 동안 자신과 아군의 이동 속도가 '
                   '20% 상승합니다. <br><br>신화급 기본 지속 효과: 다른 모든 '
                   '전설급 아이템에 주문력 15 <br><br>레벨 비례 '
                   '효과는 아군의 레벨에 따라 상승합니다.<br>',
    'plain_text': '피해량의 일부를 나중에 받습니다.',
    'price': 2500,
    'sell': 1750,
    'tags': 'Health,SpellDamage,ManaRegen,CooldownReduction,NonbootsMovement',
    'item_grade': 2
}


def response_model():
    return marshal(dummy_data, response_fields)


class Item(db.Model):
    __table_name__ = 'item'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(800), nullable=False)
    plain_text = db.Column(db.String(100), default='')
    price = db.Column(db.Integer, nullable=False)
    sell = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(200), default='')
    item_grade = db.Column(db.Integer, nullable=False)

    def __init__(
            self, item_id, name, description, plain_text, price, sell, tags, item_grade
    ):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.plain_text = plain_text
        self.price = price
        self.sell = sell
        self.tags = tags
        self.item_grade = item_grade

    def __repr__(self):
        return f"""
            item_id = {self.item_id}\n
            name = {self.name}\n
            description = {self.description}\n
            plain_text = {self.plain_text}\n
            price = {self.price}\n
            sell = {self.sell}\n
            tags = {self.tags}\n
            item_grade = {self.item_grade}
        """

    # SQLObject to Dict
    # property 데코레이터를 사용해 Class.serialize를 호출하면 return의 값이 반환됨
    @property
    def serialize(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'plain_text': self.plain_text,
            'price': self.price,
            'sell': self.sell,
            'tags': self.tags,
            'item_grade': self.item_grade,
        }
