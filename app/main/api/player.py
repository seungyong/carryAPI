import urllib.error
from os import getenv
from urllib import request
from json import loads

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

from app import session
from ..models.player import Player as Player_model

from ..util import response, riot_url

from ..controller.player import PlayerController
from ..util import constants
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

player_bp = Blueprint('player_bp', __name__)
player_ns = Namespace(
    'Player',
    'Player 관련 API입니다.',
    path='/players'
)

response_no_data_model = player_ns.model('Not Found Player Data', DataNotFound.response_model())
response_forbidden_model = player_ns.model("Can't access URL or not found URL", Forbidden.response_model())
response_internal_server_error_model = player_ns.model('Server Error', InternalServerError.response_model())



@player_ns.route('/<string:username>')
@player_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
class GameWithUsername(Resource):
    @player_ns.response(200, 'Success')
    @player_ns.response(404, 'No Data', response_no_data_model)
    @player_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
    def get(self, username):
        try:
            player_controller = PlayerController()
            result = player_controller.get_player(self,username)

            return result, constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code

    @player_ns.response(200, 'Success Insert User Data')
    @player_ns.response(400, 'Already User Data')
    @player_ns.response(404, 'No Search User Data')
    @player_ns.response(201, 'Created')
    @player_ns.response(403, 'Forbidden', response_forbidden_model)
    def post(self, username):
        """Insert player data with username."""
        try:
            print(username)
            player_controller = PlayerController()
            code = player_controller.insert_player(username)

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


