from json import loads
from urllib import request as url_request
from urllib.error import HTTPError

from app import session

from ..controller.champion_skill import ChampionSkillController
from ..models.champion import Champion as ChampionModel
from ..util.single_ton import Singleton
from ..util.version import get_version
from ..util.riot_url import champions_url
from ..util.constants import *
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden


class ChampionController(metaclass=Singleton):
    @staticmethod
    def insert_champion():
        """Insert Champions data that doesn't exist."""
        version = get_version()
        url = champions_url(version)

        try:
            with url_request.urlopen(url) as res:
                data = loads(res.read().decode())
        except HTTPError as e:
            if e.code == 403:
                raise Forbidden('Wrong Riot URL.')
            else:
                raise Exception

        # No Champions Data with Riot API
        if 'data' not in data:
            raise DataNotFound('Failed to get champion data from riot api.')

        riot_champions = []

        # add Champion Model List
        for key, info in data['data'].items():
            riot_champions.append(ChampionModel(
                champion_id=info['key'],
                kor_name=info['name'],
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
                score=12.5,
                current_tier=1,
                prev_tier=5,
                ad_damage_percent=90,
                ap_damage_percent=10,
                total_ban=10,
                total_pick=10,
                total_win=5,
                total_lose=5,
                total_match=10
            ))

        db_champions = [x.serialize for x in session.query(ChampionModel).all()]

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

            champion_skill_controller = ChampionSkillController()
            champions_skill = champion_skill_controller.get_champions_skill_with_api(champions, version)

            if champions_skill:
                session.add_all(champions)
                session.add_all(champions_skill)
                session.commit()
                return CREATED
            else:
                raise DataNotFound('Failed to get champion skills data from riot api.')
        else:
            return CREATED

    @staticmethod
    def get_all_champion_name():
        champions_name = [dict(x) for x in session.query(ChampionModel).with_entities(ChampionModel.champion_id,
                                                                                      ChampionModel.kor_name,
                                                                                      ChampionModel.eng_name)]

        if champions_name:
            return champions_name
        else:
            raise DataNotFound('Not Found Champion')
