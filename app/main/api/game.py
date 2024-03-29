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
        print("get all")
        try:
            page = flask_request.args.get('page', default=1, type=int)
            count = flask_request.args.get('count', default=20, type=int)
            queue = flask_request.args.get('queue', default=None, type=int)

            game_controller = GameController

            res = game_controller.get_game(puuid, page, count, queue)

            return res, constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception as e:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code

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
        except DataNotFound as e:
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


@game_ns.route('/withid/<string:game_id>')
@game_ns.response(500, 'Internal Server Error')
class GameWithId(Resource):
    @staticmethod
    @game_ns.response(200, 'Success')
    @game_ns.response(404, 'No Data', response_no_data_model)
    def get(game_id):
        """Get item data with game_id"""
        print("asdas2")
        try:
            game_controller = GameController
            res = game_controller.get_game_with_game_id(game_id)
            return res, constants.OK
        except Exception as e:
            print(e)

    def post(self, game_id):
        try:
            game_contorller = GameController
            game_contorller.get_test_game(GameController, game_id, 'vumohJCQwV-DEMRFQQqo4iTsxtSclzaQ00Sh0k6T4y2QFao')
            return '', constants.OK
        except Exception as e:
            session.rollback()
            print(e)
