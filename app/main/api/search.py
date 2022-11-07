from flask import Blueprint
from flask_restx import Namespace, Resource, fields
from app import session

from ..controller.champion import ChampionController
from ..controller.player import PlayerController

from ..util import constants
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

search_bp = Blueprint('search_bp', __name__)
search_ns = Namespace(
    'Search',
    'Search API',
    path='/search'
)

response_no_data_model = search_ns.model('Not Found Champion Data', DataNotFound.response_model())
response_forbidden_model = search_ns.model("Can't access URL or not found URL", Forbidden.response_model())
response_internal_server_error_model = search_ns.model('Server Error', InternalServerError.response_model())


@search_ns.route('/<string:target>')
@search_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
class AllSearch(Resource):
    @search_ns.response(201, 'Created')
    @search_ns.response(403, 'Forbidden', response_forbidden_model)
    def get(self, target):
        try:
            champion_controller = ChampionController
            res = champion_controller.get_champion_with_name(target)

            if res:
                return res, constants.OK
            else:
                player_controller = PlayerController
                resp = player_controller.get_player(self, target)
                if resp:
                    return resp, constants.OK
        except DataNotFound as e:
            print(e)
            return e.__dict__, e.code
        except Forbidden as e:
            return e.__dict__, e.code
        except Exception as e:
            print(e)
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code

#
# @champion_ns.route('/name')
# @champion_ns.response(200, 'Success')
# @champion_ns.response(404, 'No Found Data', response_no_data_model)
# @champion_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
# class ChampionName(Resource):
#     @staticmethod
#     def get():
#         """Get All Champion name, id"""
#         try:
#             champion_controller = ChampionController()
#             result = champion_controller.get_all_champion_name()
#
#             return result, constants.OK
#         except DataNotFound as e:
#             return e.__dict__, e.code
#         except Exception:
#             session.rollback()
#             e = InternalServerError('Unknown Error')
#             return e.__dict__, e.code
