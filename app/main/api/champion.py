from urllib import request
from json import loads

from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from app import session
from ..models.champion import Champion as Champion_model, response_all_model, response_name_model
from ..models.champion_skill import response_model as champion_skill_response_model

from .champion_skill import insert_champions_skill, get_champion_skill
from ..util import response, riot_url, version as version_util

champion_bp = Blueprint('champion_bp', __name__)
champion_ns = Namespace(
    'Champion',
    'Champion 관련 API입니다.',
    path='/champions'
)

request_model = champion_ns.model('Champion Id List', {
    'champion_ids': fields.List(fields.Integer(1), description='Champion Id List', required=True, default=[1, 2, 3, 4, 55])
})

response_model = champion_ns.model('Champion Response Model', {
    'results': fields.List(fields.String(response_all_model() | champion_skill_response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = champion_ns.model('Champion No Data', {
    'statusCode': fields.Integer(404)
})

response_name_model = champion_ns.model('Champion Name Information', {
    'results': fields.List(fields.String(response_name_model())),
    'statusCode': fields.Integer(200)
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

    @champion_ns.expect(request_model)
    @champion_ns.response(200, 'Success Get Data', response_model)
    @champion_ns.response(404, 'Bad Request')
    def post(self):
        """Select champions with body parameter."""
        request_data = request.get_json()

        if 'champion_ids' in request_data:
            champion_ids = request_data['champion_ids']

            try:
                champions = [x.serialize for x in session.query(Champion_model).filter(Champion_model.champion_id.in_(tuple(champion_ids))).all()]
                res = response.response_data(champions)

                return res, res['statusCode']
            except Exception as e:
                return {'message': 'Internal Server Error'}, 500
        else:
            return {'message': 'Bad Request'}, 400

    @champion_ns.response(204, 'Champions data add or update completed!')
    @champion_ns.response(503, 'Failed to receive champions information from Riot API')
    def put(self):
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
                champion_skill_status_code = insert_champions_skill(champions)

                if champion_skill_status_code == 204:
                    session.commit()
                    return '', 204
                else:
                    session.rollback()
                    return '', 500
        except Exception as e:
            session.rollback()
            return '', 500

    @champion_ns.response(204, 'Delete all champion data complete!')
    def delete(self):
        """ Delete Champions """
        try:
            # cascade 때문에 skills도 같이 삭제됨.
            session.query(Champion_model).delete()
            session.commit()

            status_code = 204
        except Exception:
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
        champion = [x.serialize for x in session.query(Champion_model).filter_by(champion_id=champion_id)]
        response_champion = response.response_data(champion)
        response_champion_skill = get_champion_skill(champion_id)

        if response_champion['statusCode'] == 404:
            response_data = {}
            status_code = 404
        elif response_champion_skill['statusCode'] == 200:
            response_data = response_champion['results'][0] | response_champion_skill['results'][0]
            status_code = 200
        else:
            response_data = {}
            status_code = 500

        return response_data, status_code


@champion_ns.route('/name')
@champion_ns.response(200, 'Success', response_name_model)
@champion_ns.response(404, 'No Found Data', response_no_data_model)
@champion_ns.response(500, 'Internal Server Error')
class ChampionName(Resource):
    @champion_ns.expect(request_model)
    def post(self):
        """Get Champions name Because this using show thumbnail, name and routing page."""
        request_data = request.get_json()

        if 'champion_ids' in request_data:
            champion_ids = request_data['champion_ids']

            try:
                champions = [dict(x) for x in session.query(Champion_model).filter(
                    Champion_model.champion_id.in_(tuple(champion_ids))).with_entities(Champion_model.champion_id, Champion_model.champion_name, Champion_model.eng_name)]
                res = response.response_data(champions)

                return res, res['statusCode']
            except Exception as e:
                print(e)
                return {'message': 'Internal Server Error'}, 500
        else:
            return {'message': 'Bad Request'}, 400
        