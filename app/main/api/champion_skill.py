from urllib import request
from json import loads

from flask import Blueprint
from flask_restx import Namespace, Resource, fields
from app import session
from ..models.champion_skill import ChampionSkill as ChampionSkill_model, response_model
from ..models.champion import Champion as Champion_model
from ..util import response, riot_url, version as version_util

champion_skills_bp = Blueprint('champion_skills_bp', __name__)
champion_skills_ns = Namespace(
    'Champion SKill',
    'Champion Skill 관련 API입니다.',
    path='/championSkills'
)

response_model = champion_skills_ns.model('Champion Skills Response Model', {
    'results': fields.List(fields.String(response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = champion_skills_ns.model('Champion Skills No Data', {
    'statusCode': fields.Integer(404)
})


@champion_skills_ns.route('/')
@champion_skills_ns.response(500, 'Internal Server Error')
class ChampionSkills(Resource):
    @champion_skills_ns.response(204, 'Champion skills insertion completed!')
    def post(self):
        """Insert champion skills data that doesn't exist."""
        try:
            champions_skill_with_api = []
            champions = [x.serialize for x in session.query(Champion_model).all()]
            champion_skill_with_db = [x.serialize for x in session.query(ChampionSkill_model).all()]

            version = version_util.get_version()

            for champion in champions:
                url = riot_url.champion_url(version, champion['eng_name'])

                with request.urlopen(url) as res:
                    data = loads(res.read().decode())
                    info = data['data'][champion['eng_name']]

                    champions_skill_with_api.append(ChampionSkill_model(
                        champion_id=champion['champion_id'],
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

            set1 = set([int(x.champion_id) for x in champions_skill_with_api])
            set2 = set([int(x['champion_id']) for x in champion_skill_with_db])

            not_champion_skills = list(set1 - set2)
            champion_skills = []

            if not_champion_skills:
                for champion_id in not_champion_skills:
                    idx = next((
                        index for (index, item) in enumerate(champions_skill_with_api)
                        if int(item.champion_id) == int(champion_id)
                    ), None)

                    champion_skills.append(champions_skill_with_api[idx])

                session.add_all(champion_skills)
                session.commit()

            return '', 204
        except Exception as e:
            print(e)
            return '', 500

    @champion_skills_ns.response(204, 'Champion skills insertion completed!')
    def put(self):
        """Champion skills inserted based on champion table after Champion skills deleted."""
        try:
            res = self.delete()

            if res[1] != 204:
                return '', 500

            champions_skill = []
            champions = [x.serialize for x in session.query(Champion_model).all()]

            version = version_util.get_version()

            for champion in champions:
                url = riot_url.champion_url(version, champion['eng_name'])

                with request.urlopen(url) as res:
                    data = loads(res.read().decode())
                    info = data['data'][champion['eng_name']]

                    champions_skill.append(ChampionSkill_model(
                        champion_id=champion['champion_id'],
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

            session.add_all(champions_skill)
            session.commit()

            return '', 204
        except:
            return '', 500

    @champion_skills_ns.response(204, 'Champion skills delete completed!')
    def delete(self):
        """Delete from Champion skills"""
        try:
            session.query(ChampionSkill_model).delete()
            session.commit()

            status_code = 204
        except:
            session.rollback()
            status_code = 500

        return '', status_code


@champion_skills_ns.route('/<int:champion_id>')
@champion_skills_ns.response(500, 'Internal Server Error')
class ChampionSkillsWithName(Resource):
    @champion_skills_ns.response(200, 'Success', response_model)
    @champion_skills_ns.response(404, 'Success', response_no_data_model)
    def get(self, champion_id):
        """Get champion skills with champion_id"""
        champion = [x.serialize for x in session.query(ChampionSkill_model).filter_by(champion_id=champion_id)]
        res = response.response_data(champion)

        return res, res['statusCode']
