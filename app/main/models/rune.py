from app import db

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import SMALLINT, VARCHAR


class Rune(db.Model):
    __table_name__ = 'rune'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    rune_id = Column(SMALLINT, primary_key=True)
    kor_name = Column(VARCHAR(15), unique=True, nullable=False)
    eng_name = Column(VARCHAR(20), unique=True, nullable=False)
    thumbnail = Column(VARCHAR(100), nullable=False)
    short_desc = Column(VARCHAR(300))
    long_desc = Column(VARCHAR(500))

    def __init__(
            self, rune_id, kor_name, eng_name, thumbnail, short_desc, long_desc
    ):
        self.rune_id = rune_id
        self.kor_name = kor_name
        self.eng_name = eng_name
        self.thumbnail = thumbnail
        self.short_desc = short_desc
        self.long_desc = long_desc

    @property
    def serialize(self):
        return {
            'rune_id': self.rune_id,
            'kor_name': self.kor_name,
            'eng_name': self.eng_name,
            'thumbnail': self.thumbnail,
            'short_desc': self.short_desc,
            'long_desc': self.long_desc
        }
