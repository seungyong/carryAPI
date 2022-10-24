from app import db

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, VARCHAR


class ChampionSkill(db.Model):
    __table_name__ = 'champion_skill'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    champion_id = Column(SMALLINT, ForeignKey('champion.champion_id'), primary_key=True)
    p_name = Column(VARCHAR(40), nullable=False)
    p_description = Column(VARCHAR(500), nullable=False)
    p_thumbnail = Column(VARCHAR(50), nullable=False)
    q_id = Column(VARCHAR(40), nullable=False)
    q_name = Column(VARCHAR(40), nullable=False)
    q_description = Column(VARCHAR(500), nullable=False)
    q_tooltip = Column(VARCHAR(1000), nullable=False)
    q_cooldown = Column(VARCHAR(50), nullable=False)
    q_cost = Column(VARCHAR(50), default=0)
    q_range = Column(VARCHAR(50), nullable=False)
    q_thumbnail = Column(VARCHAR(50), nullable=False)
    w_id = Column(VARCHAR(40), nullable=False)
    w_name = Column(VARCHAR(40), nullable=False)
    w_description = Column(VARCHAR(500), nullable=False)
    w_tooltip = Column(VARCHAR(1000), nullable=False)
    w_cooldown = Column(VARCHAR(50), nullable=False)
    w_cost = Column(VARCHAR(50), default=0)
    w_range = Column(VARCHAR(50), nullable=False)
    w_thumbnail = Column(VARCHAR(50), nullable=False)
    e_id = Column(VARCHAR(40), nullable=False)
    e_name = Column(VARCHAR(40), nullable=False)
    e_description = Column(VARCHAR(500), nullable=False)
    e_tooltip = Column(VARCHAR(1000), nullable=False)
    e_cooldown = Column(VARCHAR(50), nullable=False)
    e_cost = Column(VARCHAR(50), default=0)
    e_range = Column(VARCHAR(50), nullable=False)
    e_thumbnail = Column(VARCHAR(50), nullable=False)
    r_id = Column(VARCHAR(40), nullable=False)
    r_name = Column(VARCHAR(40), nullable=False)
    r_description = Column(VARCHAR(500), nullable=False)
    r_tooltip = Column(VARCHAR(1000), nullable=False)
    r_cooldown = Column(VARCHAR(50), nullable=False)
    r_cost = Column(VARCHAR(50), default=0)
    r_range = Column(VARCHAR(50), nullable=False)
    r_thumbnail = Column(VARCHAR(50), nullable=False)

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
