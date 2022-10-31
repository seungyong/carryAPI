from os import getenv
from urllib import request as urllib_request
from json import loads
from datetime import datetime, timedelta

from flask import Blueprint, request as flask_request
from flask_restx import Namespace, Resource, fields
from sqlalchemy import desc

from app import session
from ..models.game import Game as Game_model
from ..models.game_player import GamePlayer as Game_player_model
from ..models.game_team_info import GameTeamInfo as Game_team_info_model

from ..util import response, riot_url

from ..controller.game import GameController
from ..util import constants
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

game_bp = Blueprint('game_bp', __name__)
game_ns = Namespace(
    'Game',
    'Game 관련 API입니다.',
    path='/games'
)

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
    @game_ns.response(200, 'Success')
    @game_ns.response(204, 'No Data', response_no_data_model)
    def get(self, puuid):
        """Get User game History."""
        page = flask_request.args.get('page', default=1, type=int)
        count = flask_request.args.get('count', default=20, type=int)
        queue = flask_request.args.get('queue', default=None, type=int)
        history = list()
        players = list()

        count *= count

        if page == 1:
            start = 0
        else:
            start = (page - 1) * count

        if queue is None:
            game_info = [x for x in session.query(Game_model, Game_player_model, Game_team_info_model)
            .filter(Game_model.puuid == puuid).join(Game_player_model, Game_model.game_id == Game_player_model.game_id)
            .join(Game_team_info_model, Game_model.game_id == Game_team_info_model.game_id)
            .order_by(desc(Game_model.played_time)).offset(start).limit(count)]
        else:
            game_info = [x for x in session.query(Game_model, Game_player_model, Game_team_info_model)
            .filter(Game_model.puuid == puuid, Game_model.queue_id == queue)
            .join(Game_player_model, Game_model.game_id == Game_player_model.game_id)
            .join(Game_team_info_model, Game_model.game_id == Game_team_info_model.game_id)
            .order_by(desc(Game_model.played_time)).offset(start).limit(count)]

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
        try:
            current_timestamp = datetime.today() - timedelta(days=90)
            page = flask_request.args.get('page', default=0, type=int)
            count = flask_request.args.get('count', default=20, type=int)
            queue = flask_request.args.get('queue', default=None, type=int)
            game_controller = GameController()
            code = game_controller.insert_game(puuid, page, count, queue, current_timestamp)
            print("잇힝")
            if code == constants.CREATED:
                return '', constants.CREATED
        except DataNotFound as e :
            return e.__dict__, e.code
        except Forbidden as e:
            return e.__dict__, e.code
        except Exception:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code

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
