from json import loads
from os import getenv
from urllib import request as url_request, parse
from urllib.error import HTTPError

from sqlalchemy import desc

from app import session

from ..models.game import Game as GameModel
from ..models.game_player import GamePlayer as GamePlayerModel
from ..models.game_team_info import GameTeamInfo as GameTeamInfoModel
from ..models.solo_most_champion import SoloMostChampion as SoloMostChampionModel
from ..models.flex_most_champion import FlexMostChampion as FlexMostChampionModel
from .player import PlayerController

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
                            # created_time=datetime.fromtimestamp(str(game['info']['gameCreation'])[:-3])
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
                                primary_rune_build='dummy1',
                                sub_rune_build='dummy2',
                                stat='dummy',
                                skill_build='dummy4',
                                team_position=game_info['teamPosition'],
                                # kda=kda,
                                first_blood=game_info['firstBloodKill'],
                                kills=game_info['kills'],
                                deaths=game_info['deaths'],
                                assists=game_info['assists'],
                                max_kill_type=kill_type,
                                total_damage_to_champions=game_info['totalDamageDealtToChampions'],
                                cs=game_info['totalMinionsKilled'] + game_info['neutralMinionsKilled'],
                                gold_earned=game_info['goldEarned'],
                                vision_score=game_info['visionScore'],
                                wards_placed=100,  # Dummy Data
                                control_wards_placed=control_wards_placed,
                                summoner1_id=game_info['summoner1Id'],
                                summoner2_id=game_info['summoner2Id'],
                            ))
                        print("check10")
                        # team_win = (100 if game['info']['teams'][0]['win'] else 200)

                        game_team_info.append(GameTeamInfoModel(
                            game_id=game_id,
                            # team_win=team_win,
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
                # except url_request.error.HTTPError as error:
                except HTTPError as error:
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

    @staticmethod
    def get_game(puuid, page, count, queue):
        history = list()
        players = list()

        count *= count

        if page == 1:
            start = 0
        else:
            start = (page - 1) * count

        if queue is None:
            game_info = [x for x in session.query(GameModel, GamePlayerModel, GameTeamInfoModel)
            .filter(GameModel.puuid == puuid).join(GamePlayerModel, GameModel.game_id == GamePlayerModel.game_id)
            .join(GameTeamInfoModel, GameModel.game_id == GameTeamInfoModel.game_id)
            .order_by(desc(GameModel.played_time)).offset(start).limit(count)]
        else:
            game_info = [x for x in session.query(GameModel, GamePlayerModel, GameTeamInfoModel)
            .filter(GameModel.puuid == puuid, GameModel.queue_id == queue)
            .join(GamePlayerModel, GameModel.game_id == GamePlayerModel.game_id)
            .join(GameTeamInfoModel, GameModel.game_id == GameTeamInfoModel.game_id)
            .order_by(desc(GameModel.played_time)).offset(start).limit(count)]

        # 데이터 가공
        for i, game in enumerate(game_info):
            info = dict()
            i += 1
            players.append(game[1].serialize)

            # 10개당(플레이어) 1개의 게임
            if i % 10 == 0:
                for key, value in game[0].serialize.items():
                    info[key] = value

                for key, value in game[2].serialize.items():
                    info[key] = value

                info['players'] = players
                players = list()
                history.append(info)

        res = response.response_data(history)

        return res

    @staticmethod
    def get_game_with_game_id(game_id):
        history = list()
        players = list()
        game_info = [x for x in
                     session.query(GameModel, GamePlayerModel, GameTeamInfoModel).filter(GameModel.game_id == game_id)
                     .join(GamePlayerModel, GameModel.game_id == GamePlayerModel.game_id)
                     .join(GameTeamInfoModel, GameModel.game_id == GameTeamInfoModel.game_id)]

        # 데이터 가공
        for i, game in enumerate(game_info):
            info = dict()
            i += 1
            players.append(game[1].serialize)

            # 10개당(플레이어) 1개의 게임
            if i % 10 == 0:
                for key, value in game[0].serialize.items():
                    info[key] = value

                for key, value in game[2].serialize.items():
                    info[key] = value

                info['players'] = players
                players = list()
                history.append(info)
        res = response.response_data(history)

        return res

    def get_game_id_filter_queue(self, puuid, queue):
        print(puuid, queue)
        if queue is None:
            res = [dict(x) for x in session.query(GameModel)
            .with_entities(GameModel.game_id)
            .filter_by(puuid=puuid)]
        else:
            res = [dict(x) for x in session.query(GameModel)
            .with_entities(GameModel.game_id)
            .filter_by(puuid=puuid, queue_id=queue)]
        return res

    def post_most_champion(self, summoner_id, queue, game_id):
        game_info = self.get_game_with_game_id(game_id['game_id'])
        print("TAKE")
        for player in game_info['results'][0]['players']:
            for key, value in player.items():
                if key == 'summoner_id':
                    if value == summoner_id:
                        most_champion = []
                        champion_ids = [x for x in
                                        session.query(SoloMostChampionModel).with_entities(
                                            SoloMostChampionModel.champion_id).filter_by(
                                            summoner_id=summoner_id)]
                        if player['champion_id'] in champion_ids[0]:
                            champion_exist = True
                        else:
                            champion_exist = False
                        print("Check1")
                        if str(game_info['results'][0]['team_win']) == str(player['team_id']):
                            win = 1
                            lose = 0
                        else:
                            win = 0
                            lose = 1
                        print("Check2")
                        if champion_exist:
                            most_champion_temp = [dict(x) for x in
                                                  session.query(SoloMostChampionModel).with_entities(
                                                      SoloMostChampionModel.total_kill,
                                                      SoloMostChampionModel.total_death,
                                                      SoloMostChampionModel.total_assist,
                                                      SoloMostChampionModel.total_win,
                                                      SoloMostChampionModel.total_lose,
                                                      SoloMostChampionModel.sample_match)
                                                  .filter_by(summoner_id=summoner_id,
                                                             champion_id=player['champion_id'])]
                            print("Check3")
                            most_champion.append(SoloMostChampionModel(
                                summoner_id=summoner_id,
                                champion_id=player['champion_id'],
                                total_kill=most_champion_temp[0]['total_kill'] + player['kills'],
                                total_death=most_champion_temp[0]['total_death'] + player['deaths'],
                                total_assist=most_champion_temp[0]['total_assist'] + player['assists'],
                                total_win=most_champion_temp[0]['total_win'] + win,
                                total_lose=most_champion_temp[0]['total_lose'] + lose,
                                sample_match=most_champion_temp[0]['sample_match'] + 1
                            ))
                            print("Check4")
                        else:
                            most_champion.append(SoloMostChampionModel(
                                summoner_id=summoner_id,
                                champion_id=player['champion_id'],
                                total_kill=player['kills'],
                                total_death=player['deaths'],
                                total_assist=player['assists'],
                                total_win=win,
                                total_lose=lose,
                                sample_match=1
                            ))
                        session.add_all(most_champion)
                        session.commit()
        return OK

    def get_test_game(self, game_id, summoner_id):
        try:
            headers = {
                getenv('RIOT_HEADER_KEY'): getenv('RIOT_API_KEY')
            }
            url = riot_url.matches_info_url(game_id)
            req = url_request.Request(url, None, headers)

            games = {'history': ''}
            print("ck")
            try:
                with url_request.urlopen(req) as res:
                    game = loads(res.read().decode())
                    print("ck2")
                    # 밀리초 제거
                    game_end_timestamp = str(game['info']['gameEndTimestamp'])[:-3]
                    played_time = datetime.fromtimestamp(int(game_end_timestamp))
                    print("ck33")



                    tmp = {'gameId': game['metadata']['matchId'],
                           'gameDuration': game['info']['gameDuration'],
                           'playedTime': played_time,
                           'queueId': game['info']['queueId'],
                           'teamWin': "100",
                           'players': {},
                           'teamInfos': {},
                           'itemBuild': {},
                           'skillsBuild': {}
                           }
                    games['history'] = tmp
                    player_index = 0
                    blue_total_gold = 0
                    red_total_gold = 0
                    blue_champion_deaths = 0
                    red_champion_deaths = 0
                    blue_champion_assists = 0
                    red_champion_assists = 0
                    for participant in game['info']['participants']:
                        print("ck4")
                        player = PlayerController.get_player_with_summoner_id(participant['summonerId'])
                        if participant['pentaKills'] > 0:
                            kill_type = '펜타킬'
                        elif participant['quadraKills'] > 0:
                            kill_type = '쿼드라킬'
                        elif participant['tripleKills'] > 0:
                            kill_type = '트리플킬'
                        elif participant['doubleKills'] > 0:
                            kill_type = '더블킬'
                        else:
                            kill_type = ''

                        if participant['teamId'] == 100:
                            blue_total_gold += int(participant['goldEarned'])
                            blue_champion_assists += participant['assists']
                            blue_champion_deaths += participant['deaths']
                        else:
                            red_total_gold += int(participant['goldEarned'])
                            red_champion_assists += participant['assists']
                            red_champion_deaths += participant['deaths']

                        if 'challenges' in participant:
                            kda = participant['challenges']['kda']
                            control_wards_placed = participant['challenges']['controlWardsPlaced']
                        else:
                            # -1은 Perfect 게임
                            # URF 같은 특수모드는 kda를 주지 않음 (0으로 나눌 시 ZeroDivision Error 발생)
                            if participant['deaths'] == 0:
                                kda = -1
                            else:
                                kda = (participant['kills'] + participant['assists']) / participant['deaths']




                        player_data = {
                            'teamId': participant['teamId'],
                            'puuid': player[0]['puuid'],
                            'summonerId': participant['summonerId'],
                            'summonerName': participant['summonerName'],
                            'level': player[0]['level'],
                            'soloTier': player[0]['solo_tier'],
                            'soloRank': player[0]['solo_rank'],
                            'soloPoint': player[0]['solo_point'],
                            'flexTier': player[0]['flex_tier'],
                            'flexRank': player[0]['flex_rank'],
                            'flexPoint': player[0]['flex_point'],
                            'championId': participant['championId'],
                            'championLevel': participant['champLevel'],
                            'item0Id': participant['item0'],
                            'item1Id': participant['item1'],
                            'item2Id': participant['item2'],
                            'item3Id': participant['item3'],
                            'item4Id': participant['item4'],
                            'item5Id': participant['item5'],
                            'item6Id': participant['item6'],
                            'teamPosition': participant['teamPosition'],
                            'killInvolvement': 80, # 뭔지 모르겠음.
                            'kda': kda,
                            'firstBlood': 1 if participant['firstBloodKill'] else 0,
                            'kills': participant['kills'],
                            'deaths': participant['deaths'],
                            'assists': participant['assists'],
                            'maxKillType': kill_type,
                            'totalDamageToChampions': participant['totalDamageDealtToChampions'],
                            'cs': participant['totalMinionsKilled'] + participant['neutralMinionsKilled'],
                            'goldEarned': participant['goldEarned'],
                            'visionScore': participant['visionScore'],
                            'wardsPlaced': participant['wardsPlaced'],
                            'controlWardsPlaced': control_wards_placed,
                            'summoner1Id': participant['summoner1Id'],
                            'summoner2Id': participant['summoner2Id']
                        }
                        games['history']['players'][player_index] = player_data
                        player_index += 1

                    teaminfos_data_blue = {
                        "teamId": 100,
                        "baronKills": game['info']['teams'][0]['objectives']['baron']['kills'],
                        "dragonKills": game['info']['teams'][0]['objectives']['dragon']['kills'],
                        "towerKills": game['info']['teams'][0]['objectives']['tower']['kills'],
                        "championKills": game['info']['teams'][0]['objectives']['champion']['kills'],
                        "totalGold": blue_total_gold,
                        "totalKills": game['info']['teams'][0]['objectives']['champion']['kills'],
                        "totalDeaths": blue_champion_deaths,
                        "totalAssist": blue_champion_assists
                    }
                    teaminfos_data_red = {
                        "teamId": 100,
                        "baronKills": game['info']['teams'][1]['objectives']['baron']['kills'],
                        "dragonKills": game['info']['teams'][1]['objectives']['dragon']['kills'],
                        "towerKills": game['info']['teams'][1]['objectives']['tower']['kills'],
                        "championKills": game['info']['teams'][1]['objectives']['champion']['kills'],
                        "totalGold": red_total_gold,
                        "totalKills": game['info']['teams'][1]['objectives']['champion']['kills'],
                        "totalDeaths": red_champion_deaths,
                        "totalAssist": red_champion_assists
                    }
                    games['history']['teamInfos'][0] = teaminfos_data_blue
                    games['history']['teamInfos'][1] = teaminfos_data_red
                    print(games)

                    return '', OK

            except HTTPError as error:
                if error.status == 429:
                    return 'Too Many Request', 429

            status_code = CREATED
        except Exception as e:
            print(e)
            session.rollback()
            status_code = 500

        return '', status_code
