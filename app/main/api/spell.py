from urllib import request
from json import loads

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

from app import session
from ..models.spell import Spell as Spell_model

from ..util import response, riot_url, version as version_util

from ..controller.spell import SpellController
from ..util import constants
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

spell_bp = Blueprint('spell_bp', __name__)
spell_ns = Namespace(
    'Spell',
    'Spell 관련 API입니다.',
    path='/spells'
)

response_no_data_model = spell_ns.model('Not Found Spell Data', DataNotFound.response_model())
response_forbidden_model = spell_ns.model("Can't access URL or not found URL", Forbidden.response_model())
response_internal_server_error_model = spell_ns.model('Server Error', InternalServerError.response_model())

@spell_ns.route('/')
@spell_ns.response(500, 'Internal Server Error')
class AllItem(Resource):
    @spell_ns.response(200, 'Success')
    @spell_ns.response(404, 'No Data', response_no_data_model)
    @spell_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
    def get(self):
        """Get All spell data."""
        try:
            spell_controller = SpellController
            res = spell_controller.spell_get()

            return res, constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception as e:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code

    @spell_ns.response(204, 'Insert spells success')
    def post(self):
        """Insert data for spells that do not exist."""
        try:
            spell_controller = SpellController
            code = spell_controller.spell_post()

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


    @spell_ns.response(204, 'Insert spells after Delete items')
    def put(self):
        """After deleting the spell data, insert the spell data."""
        """지울 예정"""
        try:
            res = self.delete()

            if res[1] != 204:
                return '', 500

            res = self.post()

            if res[1] != 204:
                return '', 500

            return '', 204
        except Exception as e:
            session.rollback()

    @spell_ns.response(204, 'Delete spells success')
    def delete(self):
        """Delete Spells data"""
        try:
            spell_controller = SpellController
            code = spell_controller.spell_delete()

            if code == constants.OK:
                return '', constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Forbidden as e:
            return e.__dict__, e.code
        except Exception:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code


@spell_ns.route('/<string:spell_id>')
@spell_ns.response(500, 'Internal Server Error')
class SpellWithId(Resource):
    @spell_ns.response(200, 'Success')
    @spell_ns.response(404, 'No Data', response_no_data_model)
    def get(self, spell_id):
        """Get Spell data with spell_id"""
        try:
            spell_controller = SpellController
            res = spell_controller.spell_get_with_id(spell_id)
            return res, constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception as e:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code
