from urllib import request
from json import loads

from app import session
from ..models.champion_skill import ChampionSkill as ChampionSkill_model
from ..util import response, riot_url, version as version_util


def insert_champions_skill(champions):
    try:
        champions_skills = []
        version = version_util.get_version()

        for champion in champions:
            url = riot_url.champion_url(version, champion.eng_name)

            with request.urlopen(url) as res:
                data = loads(res.read().decode())
                info = data['data'][champion.eng_name]

                champions_skills.append(ChampionSkill_model(
                    champion_id=champion.champion_id,
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

        session.add_all(champions_skills)
        session.commit()

        return 204
    except Exception as e:
        return 500


def get_champion_skill(champion_id):
    try:
        champion_skill = [x.serialize for x in session.query(ChampionSkill_model).filter_by(champion_id=champion_id)]
        res = response.response_data(champion_skill)

        return res
    except Exception:
        return {}, 500

