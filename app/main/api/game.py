from os import getenv
from urllib import request as urllib_request
from json import loads
from datetime import datetime, timedelta

from flask import Blueprint, request as flask_request
from flask_restx import Namespace, Resource, fields

from app import session
from ..models.game import Game as Game_model, response_model
from ..models.game_player import GamePlayer as Game_player_model
from ..models.game_team_info import GameTeamInfo as Game_team_info_model

from ..util import response, riot_url, version as version_util

game_bp = Blueprint('game_bp', __name__)
game_ns = Namespace(
    'Game',
    'Game 관련 API입니다.',
    path='/games'
)

response_model = game_ns.model('Game Response Model', {
    'results': fields.List(fields.String(response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = game_ns.model('Game No Data', {
    'statusCode': fields.Integer(404)
})


@game_ns.route('/<string:puuid>')
@game_ns.response(500, 'Internal Server Error')
# 6개월 이후 기록은 전체 유저 기록을 싹 정리하는 API를 넣는 게 좋을듯
class AllGame(Resource):
    @game_ns.doc(
        params={
            'page': {'description': 'Matches Start', 'default': 1, 'type': 'int'},
            'count': {'description': 'Matches Count', 'default': 20, 'type': 'int'},
            'queue': {'description': 'Queue Type', 'default': None, 'type': 'int'}
        }
    )
    @game_ns.response(200, 'Success', response_model)
    @game_ns.response(204, 'No Data', response_no_data_model)
    def get(self, puuid):
        """Get User game History."""
        page = flask_request.args.get('page', default=1, type=int)
        count = flask_request.args.get('count', default=20, type=int)
        queue = flask_request.args.get('queue', default=None, type=int)

        page *= count

        if queue is None:
            games = [x.serialize for x in
                     session.query(Game_model).filter(Game_model.puuid == puuid).order_by(
                         Game_model.created_time).limit(count).all()]
        else:
            games = [x.serialize for x in
                     session.query(Game_model).filter(Game_model.puuid == puuid, Game_model.queue == queue).order_by(
                         Game_model.created_time).limit(count).all()]

        res = response.response_data(games)

        return res, res['statusCode']

    @game_ns.doc(
        params={
            'page': {'description': 'Matches Page', 'default': 0, 'type': 'int'},
            'count': {'description': 'Matches Count', 'default': 20, 'type': 'int'},
            'queue': {'description': 'Queue Type', 'default': None, 'type': 'int'}
        }
    )
    @game_ns.response(204, 'Success')
    @game_ns.response(204, 'No Data')
    def post(self, puuid):
        """Insert User Game History"""
        current_timestamp = datetime.today() - timedelta(days=90)
        page = flask_request.args.get('page', default=0, type=int)
        count = flask_request.args.get('count', default=20, type=int)
        queue = flask_request.args.get('queue', default=None, type=int)
        url = riot_url.matches_url(puuid, (page * count), count, queue)
        headers = {
            getenv('RIOT_HEADER_KEY'): getenv('RIOT_API_KEY')
        }
        req = urllib_request.Request(url, None, headers)

        with urllib_request.urlopen(req) as res:
            match_data = loads(res.read().decode())

        games = []
        game_players = []
        game_team_info = []

        for game_id in match_data:
            duplicated_game = [x.serialize for x in session.query(Game_model).filter_by(game_id=game_id)]

            if duplicated_game:
                continue

            url = riot_url.matches_info_url(game_id)
            req = urllib_request.Request(url, None, headers)

            try:
                with urllib_request.urlopen(req) as res:
                    game = loads(res.read().decode())

                    # 밀리초 제거
                    game_end_timestamp = str(game['info']['gameEndTimestamp'])[:-3]
                    played_time = datetime.fromtimestamp(int(game_end_timestamp))

                    # 게임 전적이 3달전이라면
                    if not played_time > current_timestamp:
                        break

                    games.append(Game_model(
                        game_id=game_id,
                        queue_id=game['info']['queueId'],
                        puuid=puuid,
                        game_duration=game['info']['gameDuration'],
                        played_time=played_time
                    ))

                    blue_total_gold = 0
                    red_total_gold = 0

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
                        else:
                            red_total_gold += int(game_info['goldEarned'])

                        if 'challenges' in game_info:
                            kda = game_info['challenges']['kda']
                        else:
                            kda = (game_info['kills'] + game_info['assists']) / game_info['deaths']

                        game_players.append(Game_player_model(
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
                            team_position=game_info['teamPosition'],
                            kda=kda,
                            first_blood=game_info['firstBloodKill'],
                            kills=game_info['kills'],
                            deaths=game_info['deaths'],
                            assists=game_info['assists'],
                            max_kill_type=kill_type,
                            total_damage_to_champions=game_info['totalDamageDealtToChampions'],
                            cs=int(game_info['totalMinionsKilled']) + int(game_info['neutralMinionsKilled']),
                            gold_earned=game_info['goldEarned'],
                            vision_score=game_info['visionScore'],
                            summoner1_id=game_info['summoner1Id'],
                            summoner2_id=game_info['summoner2Id'],
                        ))

                    team_win = (100 if game['info']['teams'][0]['win'] else 200)

                    game_team_info.append(Game_team_info_model(
                        game_id=game_id,
                        team_win=team_win,
                        blue_baron_kills=game['info']['teams'][0]['objectives']['baron']['kills'],
                        blue_dragon_kills=game['info']['teams'][0]['objectives']['dragon']['kills'],
                        blue_tower_kills=game['info']['teams'][0]['objectives']['tower']['kills'],
                        blue_champion_kills=game['info']['teams'][0]['objectives']['champion']['kills'],
                        blue_total_gold=blue_total_gold,
                        red_baron_kills=game['info']['teams'][1]['objectives']['baron']['kills'],
                        red_dragon_kills=game['info']['teams'][1]['objectives']['dragon']['kills'],
                        red_tower_kills=game['info']['teams'][1]['objectives']['tower']['kills'],
                        red_champion_kills=game['info']['teams'][1]['objectives']['champion']['kills'],
                        red_total_gold=red_total_gold,
                    ))
            except urllib_request.error.HTTPError as error:
                if error.status == 429:
                    return 'Too Many Request', 429

        session.add_all(games)
        session.add_all(game_players)
        session.add_all(game_team_info)
        session.commit()

        return '', 204

    def delete(self):
        """Delete game history within 3 Month."""
        try:
            current_timestamp = datetime.today() - timedelta(days=20)
            session.query(Game_model).filter(Game_model.played_time < current_timestamp).delete()
            session.commit()
            status_code = 204
        except Exception as e:
            print(e)
            session.rollback()
            status_code = 500

        return '', status_code
