from app import db

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR


class Item(db.Model):
    __table_name__ = 'item'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    item_id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(20), nullable=False)
    description = Column(VARCHAR(800), nullable=False)
    plain_text = Column(VARCHAR(100), default='')
    price = Column(SMALLINT, nullable=False)
    sell = Column(SMALLINT, nullable=False)
    tags = Column(VARCHAR(200), default='')
    item_grade = Column(TINYINT, nullable=False)

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
