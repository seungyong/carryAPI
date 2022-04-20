from urllib import request
from json import loads

from flask import Blueprint
from flask_restx import Namespace, Resource, fields
from app import session
from ..models.champion import Champion as Champion_model, response_model
from ..models.champion_skill import ChampionSkill as ChampionSkill_model

from .champion_skill import ChampionSkills
from ..util import response, riot_url, version as version_util

champion_bp = Blueprint('champion_bp', __name__)
champion_ns = Namespace(
    'Champion',
    'Champion 관련 API입니다.',
    path='/champions'
)

response_model = champion_ns.model('Champion Response Model', {
    'results': fields.List(fields.String(response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = champion_ns.model('Champion No Data', {
    'statusCode': fields.Integer(404)
})


@champion_ns.route('/')
@champion_ns.response(500, 'Internal Server Error')
class AllChampion(Resource):
    @champion_ns.response(200, 'Success', response_model)
    @champion_ns.response(404, 'No Data', response_no_data_model)
    def get(self):
        """Get All Champion Data"""
        champions = [x.serialize for x in session.query(Champion_model).all()]
        res = response.response_data(champions)

        return res, res['statusCode']

    @champion_ns.response(204, 'Champions data add or update completed!')
    def post(self):
        """Insert Champions data that doesn't exist."""
        version = version_util.get_version()
        url = riot_url.champions_url(version)

        with request.urlopen(url) as res:
            data = loads(res.read().decode())

        # No Champions Data with Riot API
        if 'data' not in data:
            # Riot API Error Return
            return {
                'statusCode': 503,
            }

        riot_champions = []

        # add Champion Model List
        try:
            for key, info in data['data'].items():
                riot_champions.append(Champion_model(
                    champion_id=info['key'],
                    champion_name=info['name'],
                    eng_name=info['id'],
                    sub_name=info['title'],
                    description=info['blurb'],
                    position='TOP',
                    tags=', '.join(info['tags']),
                    difficulty=info['info']['difficulty'],
                    hp=info['stats']['hp'],
                    hp_per_level=info['stats']['hpperlevel'],
                    mp=info['stats']['mp'],
                    mp_per_level=info['stats']['mpperlevel'],
                    move_speed=info['stats']['movespeed'],
                    armor=info['stats']['armor'],
                    armor_per_level=info['stats']['armorperlevel'],
                    attack_range=info['stats']['attackrange'],
                    attack_damage=info['stats']['attackdamage'],
                    attack_damage_per_level=info['stats']['attackdamageperlevel'],
                    attack_speed=info['stats']['attackspeed'],
                    attack_speed_per_level=info['stats']['attackspeedperlevel'],
                ))

            db_champions = [x.serialize for x in session.query(Champion_model).all()]

            set1 = set([int(x.champion_id) for x in riot_champions])
            set2 = set([int(x['champion_id']) for x in db_champions])

            not_champions = list(set1 - set2)
            champions = []

            if not_champions:
                for champion_id in not_champions:
                    # riot_champions에서 champion_id 없는 인덱스 반환
                    idx = next((
                        index for (index, item) in enumerate(riot_champions)
                        if int(item.champion_id) == int(champion_id)
                    ), None)

                    champions.append(riot_champions[idx])

                session.add_all(champions)
                session.commit()

            return '', 204
        except Exception as e:
            session.rollback()

    @champion_ns.response(204, 'Delete all champion data and insert complete!')
    def put(self):
        """Insert All Champion After Delete All Champion"""
        # DB savepoint
        session.begin_nested()

        try:
            # champion_skill도 같이 delete 되기 때문에 추가 해줘야함
            res = self.delete()
            champion_delete_status_code = res[1]

            if champion_delete_status_code == 204:
                res1 = self.post()
                res2 = ChampionSkills.post(ChampionSkills)
                champion_insert_status_code = res1[1]
                skill_delete_status_code = res2[1]

                if champion_insert_status_code == 204 and skill_delete_status_code == 204:
                    status_code = 204
                else:
                    session.rollback()
                    status_code = 500
        except Exception as e:
            status_code = 500
            session.rollback()

        return '', status_code

    @champion_ns.response(204, 'Delete all champion data complete!')
    def delete(self):
        """ Delete Champions """
        try:
            # 외래키로 인해 skill 테이블을 먼저 날려야 함.
            session.query(ChampionSkill_model).delete()
            session.query(Champion_model).delete()
            session.commit()

            status_code = 204
        except Exception as e:
            print(e)
            status_code = 500
            session.rollback()

        return '', status_code


@champion_ns.route('/<int:champion_id>')
@champion_ns.response(200, 'Success', response_model)
@champion_ns.response(404, 'No Found Data', response_no_data_model)
@champion_ns.response(500, 'Internal Server Error')
class ChampionWithId(Resource):
    def get(self, champion_id):
        """Get One Champion Data"""
        champions = [x.serialize for x in session.query(Champion_model).filter_by(champion_id=champion_id)]
        res = response.response_data(champions)

        return res, res['statusCode']
