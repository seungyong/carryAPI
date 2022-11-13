from flask import Blueprint
from flask_restx import Namespace, Resource, fields
from app import session

from ..controller.game import GameController
from ..controller.player import PlayerController
from flask import Blueprint, request as flask_request

from ..util import constants
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

most_bp = Blueprint('most_bp', __name__)
most_ns = Namespace(
    'Most',
    'Most 관련 API입니다.',
    path='/mosts'
)

response_no_data_model = most_ns.model('Not Found Champion Data', DataNotFound.response_model())
response_forbidden_model = most_ns.model("Can't access URL or not found URL", Forbidden.response_model())
response_internal_server_error_model = most_ns.model('Server Error', InternalServerError.response_model())


@most_ns.route('/<string:summoner_id>')
@most_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
class AllMost(Resource):
    @most_ns.doc(
        params={
            'queue': {'description': 'Queue Type', 'default': None, 'type': 'int'}
        }
    )
    @most_ns.response(201, 'Created')
    @most_ns.response(403, 'Forbidden', response_forbidden_model)
    def post(self, summoner_id):
        try:
            queue = flask_request.args.get('queue', default=None, type=int)
            game_controller = GameController
            player_controller = PlayerController
            puuid = player_controller.get_player_puuid(summoner_id)
            print(str(puuid)[3:-4])
            player_game_list = game_controller.get_game_id_filter_queue(self, str(puuid)[3:-4], queue)

            print(player_game_list)

            for game_id in player_game_list:
                game_controller.post_most_champion(GameController, summoner_id, queue, game_id)
            # 여기까지 함.


        except DataNotFound as e:
            print(e)
            session.rollback()
            return e.__dict__, e.code
        except Forbidden as e:
            print(e)
            session.rollback()
            return e.__dict__, e.code
        except Exception as e:
            print(e)
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code

