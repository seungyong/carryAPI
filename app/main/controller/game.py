from json import loads
from os import getenv
from urllib import request as url_request, parse
from urllib.error import HTTPError

from app import session


from ..models.game import Game as GameModel
from ..models.game_player import GamePlayer as GamePlayerModel
from ..models.game_team_info import GameTeamInfo as GameTeamInfoModel

from ..util.single_ton import Singleton

from ..util import response, riot_url, version as version_util
from re import compile, sub

from ..util.constants import *
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

from datetime import datetime, timedelta

class GameController(metaclass=Singleton):
    @staticmethod
    def insert_game(puuid, page, count, queue, current_timestamp):
        try:
            url = riot_url.matches_url(puuid, (page * count), count, queue)
            headers = {
                getenv('RIOT_HEADER_KEY'): getenv('RIOT_API_KEY')
            }
            req = url_request.Request(url, None, headers)

            with url_request.urlopen(req) as res:
                match_data = loads(res.read().decode())

            games = []
            game_players = []
            game_team_info = []

            for game_id in match_data:
                duplicated_game = [x.serialize for x in session.query(GameModel).filter_by(game_id=game_id)]

                if duplicated_game:
                    continue

                url = riot_url.matches_info_url(game_id)
                req = url_request.Request(url, None, headers)

                try:
                    with url_request.urlopen(req) as res:
                        game = loads(res.read().decode())

                        # 밀리초 제거
                        game_end_timestamp = str(game['info']['gameEndTimestamp'])[:-3]
                        played_time = datetime.fromtimestamp(int(game_end_timestamp))

                        # 게임 전적이 3달전이라면
                        if not played_time > current_timestamp:
                            break

                        games.append(GameModel(
                            game_id=game_id,
                            queue_id=game['info']['queueId'],
                            puuid=puuid,
                            game_duration=game['info']['gameDuration'],
                            team_win=100 if game['info']['teams'][0]['win'] else 200,
                            played_time=played_time,
                            #created_time=datetime.fromtimestamp(str(game['info']['gameCreation'])[:-3])
                        ))

                        blue_total_gold = 0
                        red_total_gold = 0

                        blue_champion_deaths = 0
                        red_champion_deaths = 0

                        blue_champion_assists = 0
                        red_champion_assists = 0

                        control_wards_placed = 0

                        for game_info in game['info']['participants']:
                            if game_info['pentaKills'] > 0:
                                kill_type = '펜타킬'
                            elif game_info['quadraKills'] > 0:
                                kill_type = '쿼드라킬'
                            elif game_info['tripleKills'] > 0:
                                kill_type = '트리플킬'
                            elif game_info['doubleKills'] > 0:
                                kill_type = '더블킬'
                            else:
                                kill_type = ''

                            if game_info['teamId'] == 100:
                                blue_total_gold += int(game_info['goldEarned'])
                                blue_champion_assists += game_info['assists']
                                blue_champion_deaths += game_info['deaths']
                            else:
                                red_total_gold += int(game_info['goldEarned'])
                                red_champion_assists += game_info['assists']
                                red_champion_deaths += game_info['deaths']

                            if 'challenges' in game_info:
                                kda = game_info['challenges']['kda']
                                control_wards_placed = game_info['challenges']['controlWardsPlaced']
                            else:
                                # -1은 Perfect 게임
                                # URF 같은 특수모드는 kda를 주지 않음 (0으로 나눌 시 ZeroDivision Error 발생)
                                if game_info['deaths'] == 0:
                                    kda = -1
                                else:
                                    kda = (game_info['kills'] + game_info['assists']) / game_info['deaths']

                            game_players.append(GamePlayerModel(
                                game_id=game_id,
                                team_id=game_info['teamId'],
                                puuid=puuid,
                                summoner_id=game_info['summonerId'],
                                summoner_name=game_info['summonerName'],
                                champion_id=game_info['championId'],
                                champion_level=game_info['champLevel'],
                                item0_id=game_info['item0'],
                                item1_id=game_info['item1'],
                                item2_id=game_info['item2'],
                                item3_id=game_info['item3'],
                                item4_id=game_info['item4'],
                                item5_id=game_info['item5'],
                                item6_id=game_info['item6'],
                                primary_rune_build = 'dummy1',
                                sub_rune_build = 'dummy2',
                                stat = 'dummy',
                                skill_build = 'dummy4',
                                team_position=game_info['teamPosition'],
                                #kda=kda,
                                first_blood=game_info['firstBloodKill'],
                                kills=game_info['kills'],
                                deaths=game_info['deaths'],
                                assists=game_info['assists'],
                                max_kill_type=kill_type,
                                total_damage_to_champions=game_info['totalDamageDealtToChampions'],
                                cs= game_info['totalMinionsKilled'] + game_info['neutralMinionsKilled'],
                                gold_earned=game_info['goldEarned'],
                                vision_score=game_info['visionScore'],
                                wards_placed = 100, #Dummy Data
                                control_wards_placed = control_wards_placed,
                                summoner1_id=game_info['summoner1Id'],
                                summoner2_id=game_info['summoner2Id'],
                            ))
                        print("check10")
                        team_win = (100 if game['info']['teams'][0]['win'] else 200)

                        game_team_info.append(GameTeamInfoModel(
                            game_id=game_id,
                            team_win=team_win,
                            blue_baron_kills=game['info']['teams'][0]['objectives']['baron']['kills'],
                            blue_dragon_kills=game['info']['teams'][0]['objectives']['dragon']['kills'],
                            blue_tower_kills=game['info']['teams'][0]['objectives']['tower']['kills'],
                            blue_champion_kills=game['info']['teams'][0]['objectives']['champion']['kills'],
                            blue_champion_deaths=blue_champion_deaths,
                            blue_champion_assists=blue_champion_assists,
                            blue_total_gold=blue_total_gold,
                            red_baron_kills=game['info']['teams'][1]['objectives']['baron']['kills'],
                            red_dragon_kills=game['info']['teams'][1]['objectives']['dragon']['kills'],
                            red_tower_kills=game['info']['teams'][1]['objectives']['tower']['kills'],
                            red_champion_kills=game['info']['teams'][1]['objectives']['champion']['kills'],
                            red_champion_deaths=red_champion_deaths,
                            red_champion_assists=red_champion_assists,
                            red_total_gold=red_total_gold,
                        ))
                    print('check11')
                except url_request.error.HTTPError as error:
                    print('check22')
                    if error.status == 429:
                        return 'Too Many Request', 429
            print(game_team_info)
            session.add_all(games)
            print("check1")
            session.add_all(game_players)
            print("check2")
            session.add_all(game_team_info)
            print("check3")
            session.commit()
            print('check2')
            status_code = CREATED
        except Exception as e:
            print(e)
            session.rollback()
            status_code = 500

        return '', status_code


