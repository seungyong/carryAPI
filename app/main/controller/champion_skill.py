from json import loads
from urllib import request as url_request

from app import session
from ..models.champion_skill import ChampionSkill
from ..util.single_ton import Singleton
from ..util.riot_url import champion_url


class ChampionSkillController(metaclass=Singleton):
    @staticmethod
    def get_champions_skill_with_api(champions, version):
        champions_skill = []

        for champion in champions:
            url = champion_url(version, champion.eng_name)

            with url_request.urlopen(url) as res:
                data = loads(res.read().decode())
                info = data['data'][champion.eng_name]

                champions_skill.append(ChampionSkill(
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

        return champions_skill

    def get_champions_skill_with_db(champions_id):
        pass
        # try:
        #     champion_skill = [x.serialize for x in
        #                       session.query(ChampionSkill).filter(
        #                           ChampionSkill.champion_id.in_(tuple(champions_id))).all()]
        #     res = response.response_data(champion_skill)
        #
        #     return res
        # except Exception:
        #     return {}, 500
