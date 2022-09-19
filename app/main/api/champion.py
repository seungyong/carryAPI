from urllib import request
from json import loads

from flask import Blueprint
from flask_restx import Namespace, Resource, fields
from app import session
from ..models.champion import Champion as Champion_model, response_all_model, response_name_model
from ..models.champion_skill import ChampionSkill as ChampionSkill_model
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
    'champion_ids': fields.List(fields.Integer(1), description='Champion Id List', required=True,
                                default=[1, 2, 3, 4, 55])
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


def insert_champions():
    """Insert Champions data that doesn't exist."""
    version = version_util.get_version()
    url = riot_url.champions_url(version)

    with request.urlopen(url) as res:
        data = loads(res.read().decode())

    # No Champions Data with Riot API
    if 'data' not in data:
        # Riot API Error Return
        return 503

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

            if champion_skill_status_code == 201:
                session.commit()
                return 201
            else:
                session.rollback()
                return 500
    except Exception as e:
        session.rollback()
        return '', 500


def insert_champions_for_update(champion_names):
    """Insert a few Champions for update"""
    try:
        champions = []
        champions_skills = []
        version = version_util.get_version()

        for champion in champion_names:
            url = riot_url.champion_url(version, champion)

            with request.urlopen(url) as res:
                data = loads(res.read().decode())
                info = data['data'][champion]

                champions.append(Champion_model(
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

                champions_skills.append(ChampionSkill_model(
                    champion_id=info['key'],
                    p_name=info['passive']['name'],
                    p_description=info['passive']['description'],
                    p_thumbnail=info['passive']['image']['full'],
                    q_id=info['spells'][0]['id'],
                    q_name=info['spells'][0]['name'],
                    q_description=info['spells'][0]['description'],
                    q_tooltip=info['spells'][0]['tooltip'],
                    q_cooldown=info['spells'][0]['cooldownBurn'],
                    q_cost=info['spells'][0]['costBurn'],
                    q_range=info['spells'][0]['rangeBurn'],
                    q_thumbnail=info['spells'][0]['image']['full'],
                    w_id=info['spells'][1]['id'],
                    w_name=info['spells'][1]['name'],
                    w_description=info['spells'][1]['description'],
                    w_tooltip=info['spells'][1]['tooltip'],
                    w_cooldown=info['spells'][1]['cooldownBurn'],
                    w_cost=info['spells'][1]['costBurn'],
                    w_range=info['spells'][1]['rangeBurn'],
                    w_thumbnail=info['spells'][1]['image']['full'],
                    e_id=info['spells'][2]['id'],
                    e_name=info['spells'][2]['name'],
                    e_description=info['spells'][2]['description'],
                    e_tooltip=info['spells'][2]['tooltip'],
                    e_cooldown=info['spells'][2]['cooldownBurn'],
                    e_cost=info['spells'][2]['costBurn'],
                    e_range=info['spells'][2]['rangeBurn'],
                    e_thumbnail=info['spells'][2]['image']['full'],
                    r_id=info['spells'][3]['id'],
                    r_name=info['spells'][3]['name'],
                    r_description=info['spells'][3]['description'],
                    r_tooltip=info['spells'][3]['tooltip'],
                    r_cooldown=info['spells'][3]['cooldownBurn'],
                    r_cost=info['spells'][3]['costBurn'],
                    r_range=info['spells'][3]['rangeBurn'],
                    r_thumbnail=info['spells'][3]['image']['full'],
                ))

        session.add_all(champions)
        session.add_all(champions_skills)
        session.commit()

        return 204
    except Exception:
        session.rollback()
        return 500


def delete_champions_for_update(champion_names):
    """Delete a few Champions for update"""
    try:
        # cascade 때문에 skills도 같이 삭제됨.
        session.query(Champion_model).filter(Champion_model.eng_name.in_(tuple(champion_names))).delete()
        session.commit()

        status_code = 204
    except Exception as e:
        print(e)
        status_code = 500
        session.rollback()

    return status_code


@champion_ns.route('/')
@champion_ns.response(500, 'Internal Server Error')
class AllChampion(Resource):
    @champion_ns.expect(request_model)
    @champion_ns.response(200, 'Success Get Data', response_model)
    @champion_ns.response(404, 'Bad Request')
    def post(self):
        """Select champions with body parameter."""
        request_data = request.get_json()

        if 'champion_ids' in request_data:
            champion_ids = request_data['champion_ids']

            try:
                champions = [x.serialize for x in session.query(Champion_model).filter(
                    Champion_model.champion_id.in_(tuple(champion_ids))).all()]
                res = response.response_data(champions)

                return res, res['statusCode']
            except Exception as e:
                return {'message': 'Internal Server Error'}, 500
        else:
            return {'message': 'Bad Request'}, 400


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
                    Champion_model.champion_id.in_(tuple(champion_ids))).with_entities(Champion_model.champion_id,
                                                                                       Champion_model.champion_name,
                                                                                       Champion_model.eng_name)]
                res = response.response_data(champions)

                return res, res['statusCode']
            except Exception:
                return {'message': 'Internal Server Error'}, 500
        else:
            return {'message': 'Bad Request'}, 400
