from flask import Blueprint, request as flask_request
from flask_restx import Namespace, Resource, fields

from app import session

from ..controller.champion import ChampionController

from ..util import constants
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

champion_bp = Blueprint('champion_bp', __name__)
champion_ns = Namespace(
    'Champion',
    'Champion 관련 API입니다.',
    path='/champions'
)

request_model = champion_ns.model('Champion Id List', {
    'champions_id': fields.List(fields.Integer(1), description='Champion Id List', required=True,
                                default=[1, 2, 3, 4, 55])
})

response_no_data_model = champion_ns.model('Not Found Champion Data', DataNotFound.response_model())
response_forbidden_model = champion_ns.model("Can't access URL or not found URL", Forbidden.response_model())
response_internal_server_error_model = champion_ns.model('Server Error', InternalServerError.response_model())


@champion_ns.route('/')
@champion_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
class AllChampion(Resource):
    @staticmethod
    @champion_ns.response(201, 'Created')
    @champion_ns.response(403, 'Forbidden', response_forbidden_model)
    def post():
        """(Admin API) Insert Champions data that doesn't exist."""
        try:
            champion_controller = ChampionController()
            code = champion_controller.insert_champion()

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


@champion_ns.route('/ranking')
@champion_ns.doc(
    params={
        'count': {'description': 'Get Ranking champion count', 'default': 5, 'type': 'int'}
    }
)
@champion_ns.response(200, 'Success')
@champion_ns.response(404, 'No Found Data', response_no_data_model)
@champion_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
class ChampionRanking(Resource):
    @staticmethod
    def get():
        try:
            count = flask_request.args.get(key='count', default=5, type=int)

            champion_controller = ChampionController()
            result = champion_controller.get_ranking(count)

            return result, constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code


@champion_ns.route('/name')
@champion_ns.response(200, 'Success')
@champion_ns.response(404, 'No Found Data', response_no_data_model)
@champion_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
class ChampionName(Resource):
    @staticmethod
    def get():
        """Get All Champion name, id"""
        try:
            champion_controller = ChampionController()
            result = champion_controller.get_all_champion_name()

            return result, constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code


@champion_ns.route('/analysis/basic')
class ChampionAnalysisBasic(Resource):
    @staticmethod
    def post():
        """(Admin API) Analyze the basic of the champion."""
        try:
            champion_controller = ChampionController()
            code = champion_controller.champion_basic_analysis()

            if code == constants.CREATED:
                return '', constants.CREATED
            else:
                raise Exception('Wrong code')
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception as e:
            print('Error : ', e)


@champion_ns.route('/analysis/counter')
class ChampionAnalysisCounter(Resource):
    @staticmethod
    def post():
        """(Admin API) Analyze the counter of the champion."""
        try:
            champion_controller = ChampionController()
            code = champion_controller.champion_counter_analysis()

            if code == constants.CREATED:
                return '', constants.CREATED
            else:
                raise Exception('Wrong code')
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception as e:
            session.rollback()
            print(e)
