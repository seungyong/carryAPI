import random
from json import loads
from urllib import request as url_request
from urllib.error import HTTPError
from collections import defaultdict

from app import session

from ..controller.champion_skill import ChampionSkillController
from ..models.champion import Champion as ChampionModel
from ..models.champion_basic import ChampionBasic as ChampionBasicModel
from ..models.champion_counter import ChampionCounter as ChampionCounterModel

from ..util.single_ton import Singleton
from ..util.version import get_version
from ..util.riot_url import champions_url
from ..util.constants import *

from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden


class ChampionController(metaclass=Singleton):
    @staticmethod
    def get_ranking(count):
        api_results = defaultdict()
        db_results = defaultdict()

        for position in POSITIONS:
            # ranking champion count 개씩 가져오기
            db_results[position] = [
                list([x[0].serialize, x[1].serialize]) for x in
                session
                .query(ChampionModel, ChampionBasicModel)
                .join(ChampionBasicModel, ChampionModel.champion_id == ChampionBasicModel.champion_id)
                .filter(ChampionModel.position == position)
                .order_by(ChampionBasicModel.score.desc()).limit(count)
            ]
            api_results[position] = list()

            for idx in range(len(db_results[position])):
                # counter champion 넣기
                db_results[position][idx].append([
                    dict(x) for x in
                    session
                    .query(ChampionModel, ChampionCounterModel)
                    .join(ChampionModel, ChampionModel.champion_id == ChampionCounterModel.to_champion_id)
                    .filter(ChampionCounterModel.champion_id == db_results[position][idx][0]['champion_id'])
                    .with_entities(ChampionModel.eng_name, ChampionCounterModel.to_champion_id, ChampionCounterModel.score)
                    .order_by(ChampionCounterModel.score.desc())
                    .limit(5)
                ])

                # response 반환 값 맞추기
                api_results[position].append(
                    ChampionModel.to_response_ranking(
                        db_results[position][idx][0], db_results[position][idx][1], db_results[position][idx][2]
                    )
                )

        is_empty = not bool([item for item in api_results.values() if item != []])

        if is_empty:
            raise DataNotFound('Not found ranking champions.')

        return api_results

    @staticmethod
    def get_all_champion_name():
        # with_entities 사용하면 튜플형태로 값이 넘어옴
        champions_name = [dict(x) for x in
                          session.query(ChampionModel).with_entities(ChampionModel.champion_id, ChampionModel.kor_name,
                                                                     ChampionModel.eng_name,
                                                                     ChampionModel.position)]
        result = defaultdict()

        for champion in champions_name:
            if champion['position'] in result:
                result[champion['position']].append(ChampionModel.to_response_name(champion))
            else:
                result[champion['position']] = list()
                result[champion['position']].append(ChampionModel.to_response_name(champion))

        if result:
            return result
        else:
            raise DataNotFound('Not Found Champion')

    # Admin API
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
                position=random.choice(POSITIONS),
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
                attack_speed_per_level=info['stats']['attackspeedperlevel']
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
    def champion_basic_analysis():
        # 여기서 chmapion table position 수정
        tier = [1, 2, 3, 4, 5]
        champions = [x['champion_id'] for x in session.query(ChampionModel).with_entities(ChampionModel.champion_id)]
        analyzed_champions = []

        if champions:
            for champion_id in champions:
                analyzed_champions.append(ChampionBasicModel(
                    champion_id=champion_id,
                    score=round(random.uniform(1, 99.9), 1),
                    current_tier=random.choice(tier),
                    prev_tier=5,
                    total_pick=100,
                    total_ban=50,
                    total_win=50,
                    total_lose=50,
                    total_match=100,
                    ad_damage_percent=90,
                    ap_damage_percent=10
                ))

            session.add_all(analyzed_champions)
            session.commit()
        else:
            raise DataNotFound('Not Found Champion Data.')

        return CREATED

    @staticmethod
    def champion_counter_analysis():
        champions = [x['champion_id'] for x in session.query(ChampionModel).with_entities(ChampionModel.champion_id)]
        analyzed_champions = []

        # x => y로 지정했으면 반대로 y => x를 지정해줘야함.
        # list not in으로 비교하면서 사용.
        if champions:
            for subject in champions:
                for target in champions:
                    if subject == target:
                        continue

                    score = round(random.uniform(1, 99.9), 1)
                    win = random.randrange(1000, 100000)
                    lose = random.randrange(1000, 100000)
                    line_kills = random.randrange(100, 10000)
                    line_deaths = random.randrange(100, 10000)

                    analyzed_champions.append(ChampionCounterModel(
                        champion_id=subject,
                        to_champion_id=target,
                        score=score,
                        win=win,
                        lose=lose,
                        line_kills=line_kills,
                        line_deaths=line_deaths,
                        champion_kills=random.randrange(line_kills, 10000),
                        champion_deaths=random.randrange(line_deaths, 10000),
                        champion_assists=random.randrange(100, 10000),
                        total_first_tower='20:05',
                        team_kills=random.randrange(10000, 1000000),
                        team_assists=random.randrange(10000, 1000000),
                        sample_match=win + lose
                    ))

            session.add_all(analyzed_champions)
            session.commit()
        else:
            raise DataNotFound('Not Found Champion Data.')

        return CREATED
