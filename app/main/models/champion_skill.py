from app import db
from flask_restx import fields, marshal

response_fields = {
    'champion_id': fields.Integer(),
    'p_name': fields.String(),
    'p_description': fields.String(),
    'p_thumbnail': fields.String(),
    'q_id': fields.String(),
    'q_name': fields.String(),
    'q_description': fields.String(),
    'q_tooltip': fields.String(),
    'q_cooldown': fields.String(),
    'q_cost': fields.String(),
    'q_range': fields.String(),
    'q_thumbnail': fields.String(),
    'w_id': fields.String(),
    'w_name': fields.String(),
    'w_description': fields.String(),
    'w_tooltip': fields.String(),
    'w_cooldown': fields.String(),
    'w_cost': fields.String(),
    'w_range': fields.String(),
    'w_thumbnail': fields.String(),
    'e_id': fields.String(),
    'e_name': fields.String(),
    'e_description': fields.String(),
    'e_tooltip': fields.String(),
    'e_cooldown': fields.String(),
    'e_cost': fields.String(),
    'e_range': fields.String(),
    'e_thumbnail': fields.String(),
    'r_id': fields.String(),
    'r_name': fields.String(),
    'r_description': fields.String(),
    'r_tooltip': fields.String(),
    'r_cooldown': fields.String(),
    'r_cost': fields.String(),
    'r_range': fields.String(),
    'r_thumbnail': fields.String(),
}

dummy_data = {
    'champion_id': 1,
    'p_name': '방화광',
    'p_description': '애니가 스킬을 4번 사용한 후 다음 공격 스킬에 맞은 적은 기절합니다.',
    'p_thumbnail': 'Annie_Passive.png',
    'q_id': 'AnnieQ',
    'q_name': '붕괴',
    'q_description': '애니가 마나로 가득 찬 화염구를 던져 피해를 입히고 결정타를 냈을 때 사용한 마나를 되돌려 받습니다.',
    'q_tooltip': '애니가 화염구를 던져 <magicDamage>{{ totaldamage }}의 마법 피해</magicDamage>를 입힙니다. 대상이 사망하면 소모한 마나를 돌려받고 재사용 대기시간이 50% 감소합니다.',
    'q_cooldown': '4',
    'q_cost': '60/65/70/75/80',
    'q_range': '625',
    'q_thumbnail': 'AnnieQ.png',
    'w_id': 'AnnieW',
    'w_name': '소각',
    'w_description': '애니가 원뿔 형태의 화염을 내뿜어 해당 지역에 있는 모든 적에게 피해를 입힙니다.',
    'w_tooltip': '애니가 화염파를 발사하여 <magicDamage>{{ totaldamage }}의 마법 피해</magicDamage>를 입힙니다.',
    'w_cooldown': '8',
    'w_cost': '90/95/100/105/110',
    'w_range': '600',
    'w_thumbnail': 'AnnieW.png',
    'e_id': 'AnnieE',
    'e_name': '용암 방패',
    'e_description': '애니나 아군에게 보호막을 부여하고 이동 속도가 증가하며, 기본 공격을 가하는 적에게 피해를 입힙니다.',
    'e_tooltip': '애니가 자신이나 아군에게 {{ shieldduration }}초 동안 <shield>{{ shieldblocktotal }}의 피해를 흡수하는 보호막</shield>을 부여합니다. 보호막으로 인해 <speed>이동 속도가 {{ movespeedcalc }}</speed> 증가한 뒤 {{ movementspeedduration }}초에 걸쳐 원래대로 돌아옵니다. 보호막이 지속되는 동안 공격한 적은 <magicDamage>{{ damagereturn }}의 마법 피해</magicDamage>를 입습니다.',
    'e_cooldown': '14/13/12/11/10',
    'e_cost': '40',
    'e_range': '800',
    'e_thumbnail': 'AnnieE.png',
    'r_id': 'AnnieR',
    'r_name': '소환: 티버',
    'r_description': '애니가 자신의 곰 티버를 되살려 지정 구역에 있는 유닛에게 피해를 입힙니다. 티버는 주변의 적을 공격하거나 불태울 수도 있습니다.',
    'r_tooltip': '애니가 티버를 소환해 <magicDamage>{{ initialburstdamage }}의 마법 피해</magicDamage>를 입힙니다. 티버는 {{ tibberslifetime }}초간 주변 적을 불태워 <magicDamage>초당 {{ tibbersauradamage }}의 마법 피해</magicDamage>를 입히고 적을 공격해 <magicDamage>{{ tibbersaadamage }}의 마법 피해</magicDamage>를 입힙니다. 애니는 이 스킬을 <recast>재사용</recast>해 티버를 조종할 수 있습니다.<br /><br />애니가 사망하면 티버가 분노하여 <attackSpeed>공격 속도가 275%</attackSpeed>, <speed>이동 속도가 100%</speed> 증가합니다. 이 효과는 3초에 걸쳐 원래대로 돌아옵니다.',
    'r_cooldown': '120/100/80',
    'r_cost': '100',
    'r_range': '600',
    'r_thumbnail': 'AnnieR.png',
}


def response_model():
    return marshal(dummy_data, response_fields)


class ChampionSkill(db.Model):
    __table_name__ = 'champion_skill'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    champion_id = db.Column(db.Integer, db.ForeignKey('champion.champion_id'), primary_key=True, unique=True)
    p_name = db.Column(db.String(40), nullable=False)
    p_description = db.Column(db.String(500), nullable=False)
    p_thumbnail = db.Column(db.String(50), nullable=False)
    q_id = db.Column(db.String(40), nullable=False)
    q_name = db.Column(db.String(40), nullable=False)
    q_description = db.Column(db.String(500), nullable=False)
    q_tooltip = db.Column(db.String(1000), nullable=False)
    q_cooldown = db.Column(db.String(50), nullable=False)
    q_cost = db.Column(db.String(50), default=0)
    q_range = db.Column(db.String(50), nullable=False)
    q_thumbnail = db.Column(db.String(50), nullable=False)
    w_id = db.Column(db.String(40), nullable=False)
    w_name = db.Column(db.String(40), nullable=False)
    w_description = db.Column(db.String(500), nullable=False)
    w_tooltip = db.Column(db.String(1000), nullable=False)
    w_cooldown = db.Column(db.String(50), nullable=False)
    w_cost = db.Column(db.String(50), default=0)
    w_range = db.Column(db.String(50), nullable=False)
    w_thumbnail = db.Column(db.String(50), nullable=False)
    e_id = db.Column(db.String(40), nullable=False)
    e_name = db.Column(db.String(40), nullable=False)
    e_description = db.Column(db.String(500), nullable=False)
    e_tooltip = db.Column(db.String(1000), nullable=False)
    e_cooldown = db.Column(db.String(50), nullable=False)
    e_cost = db.Column(db.String(50), default=0)
    e_range = db.Column(db.String(50), nullable=False)
    e_thumbnail = db.Column(db.String(50), nullable=False)
    r_id = db.Column(db.String(40), nullable=False)
    r_name = db.Column(db.String(40), nullable=False)
    r_description = db.Column(db.String(500), nullable=False)
    r_tooltip = db.Column(db.String(1000), nullable=False)
    r_cooldown = db.Column(db.String(50), nullable=False)
    r_cost = db.Column(db.String(50), default=0)
    r_range = db.Column(db.String(50), nullable=False)
    r_thumbnail = db.Column(db.String(50), nullable=False)

    def __init__(
            self, champion_id, p_name, p_description, p_thumbnail,
            q_id, q_name, q_description, q_tooltip, q_cooldown, q_cost, q_range, q_thumbnail,
            w_id, w_name, w_description, w_tooltip, w_cooldown, w_cost, w_range, w_thumbnail,
            e_id, e_name, e_description, e_tooltip, e_cooldown, e_cost, e_range, e_thumbnail,
            r_id, r_name, r_description, r_tooltip, r_cooldown, r_cost, r_range, r_thumbnail,
    ):
        self.champion_id = champion_id
        self.p_name = p_name
        self.p_description = p_description
        self.p_thumbnail = p_thumbnail
        self.q_id = q_id
        self.q_name = q_name
        self.q_description = q_description
        self.q_tooltip = q_tooltip
        self.q_cooldown = q_cooldown
        self.q_cost = q_cost
        self.q_range = q_range
        self.q_thumbnail = q_thumbnail
        self.w_id = w_id
        self.w_name = w_name
        self.w_description = w_description
        self.w_tooltip = w_tooltip
        self.w_cooldown = w_cooldown
        self.w_cost = w_cost
        self.w_range = w_range
        self.w_thumbnail = w_thumbnail
        self.e_id = e_id
        self.e_name = e_name
        self.e_description = e_description
        self.e_tooltip = e_tooltip
        self.e_cooldown = e_cooldown
        self.e_cost = e_cost
        self.e_range = e_range
        self.e_thumbnail = e_thumbnail
        self.r_id = r_id
        self.r_name = r_name
        self.r_description = r_description
        self.r_tooltip = r_tooltip
        self.r_cooldown = r_cooldown
        self.r_cost = r_cost
        self.r_range = r_range
        self.r_thumbnail = r_thumbnail

    @property
    def serialize(self):
        return {
            'champion_id': self.champion_id,
            'p_name': self.p_name,
            'p_description': self.p_description,
            'p_thumbnail': self.p_thumbnail,
            'q_id': self.q_id,
            'q_name': self.q_name,
            'q_description': self.q_description,
            'q_tooltip': self.q_tooltip,
            'q_cooldown': self.q_cooldown,
            'q_cost': self.q_cost,
            'q_range': self.q_range,
            'q_thumbnail': self.q_thumbnail,
            'w_id': self.w_id,
            'w_name': self.w_name,
            'w_description': self.w_description,
            'w_tooltip': self.w_tooltip,
            'w_cooldown': self.w_cooldown,
            'w_cost': self.w_cost,
            'w_range': self.w_range,
            'w_thumbnail': self.w_thumbnail,
            'e_id': self.e_id,
            'e_name': self.e_name,
            'e_description': self.e_description,
            'e_tooltip': self.e_tooltip,
            'e_cooldown': self.e_cooldown,
            'e_cost': self.e_cost,
            'e_range': self.e_range,
            'e_thumbnail': self.e_thumbnail,
            'r_id': self.r_id,
            'r_name': self.r_name,
            'r_description': self.r_description,
            'r_tooltip': self.r_tooltip,
            'r_cooldown': self.r_cooldown,
            'r_cost': self.r_cost,
            'r_range': self.r_range,
            'r_thumbnail': self.r_thumbnail,
        }
