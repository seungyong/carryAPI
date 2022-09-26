from app import db
from flask_restx import fields, marshal

response_fields = {
    'rune_id': fields.Integer(),
    'eng_name': fields.String(),
    'rune_icon': fields.String(),
    'kor_name': fields.String(),
    'short_desc': fields.String(),
    'long_desc': fields.String()
}

dummy_data = {
    'rune_id': 8112,
    'eng_name': "Electrocute",
    'rune_icon': "perk-images/Styles/Domination/Electrocute/Electrocute.png",
    'kor_name': "감전",
    'short_desc': "3초 동안 같은 챔피언에게 기본 공격 또는 개별 스킬 3회를 적중시키면 추가 적응형 피해적용",
    'long_desc': "3초 동안 같은 챔피언에게 개별 공격 또는 스킬을 3회 적중시키면 추가 적응형 피해를 입힙니다.피해량: 30~180 (+추가 공격력의 0.4, +주문력의 0.25) 재사용 대기시간: 25~20초'우리는 그들을 천둥군주라고 부른다. 그들의 번개를 입에 올리는 것은 재앙을 부르는 길이기 때문이다."

}


def response_model():
    return marshal(dummy_data, response_fields)


class Rune(db.Model):
    __table_name__ = 'rune'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    rune_id = db.Column(db.Integer, primary_key=True)
    eng_name = db.Column(db.String(20), nullable=False, unique=True)
    rune_icon = db.Column(db.String(100), nullable=False)
    kor_name = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.String(500), nullable=True)
    long_desc = db.Column(db.String(1000), nullable=True)

    def __init__(
            self, rune_id, eng_name,rune_icon,kor_name, short_desc, long_desc
    ):
        self.rune_id = rune_id
        self.eng_name = eng_name
        self.rune_icon = rune_icon
        self.kor_name = kor_name
        self.short_desc = short_desc
        self.long_desc = long_desc

    def __repr__(self):
        return f"""
            rune_id = {self.rune_id}\n
            eng_name = {self.eng_name}\n
            rune_icon = {self.rune_icon}\n
            kor_name = {self.kor_name}\n
            short_desc = {self.short_desc}\n
            long_desc = {self.long_desc}\n
        """

    @property
    def serialize(self):
        return {
            'rune_id' : self.rune_id,
            'eng_name' : self.eng_name,
            'rune_icon' : self.rune_icon,
            'kor_name' : self.kor_name,
            'short_desc' : self.short_desc,
            'long_desc' : self.long_desc
        }
