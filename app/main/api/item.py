from urllib import request
from json import loads
from re import compile, sub

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

from app import session
from ..models.item import Item as Item_model # 그대로 써도 될듯.
from ..controller.item import ItemController

from ..util import response, riot_url, version as version_util

from ..util import constants
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from ..exception.internal_server_error import InternalServerError

item_bp = Blueprint('item_bp', __name__)
item_ns = Namespace(
    'Item',
    'item 관련 API입니다.',
    path='/items'
)

response_no_data_model = item_ns.model('Not Found Item Data', DataNotFound.response_model())
response_forbidden_model = item_ns.model("Can't access URL or not found URL", Forbidden.response_model())
response_internal_server_error_model = item_ns.model('Server Error', InternalServerError.response_model())


@item_ns.route('/')
@item_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
class AllItem(Resource):
    @staticmethod
    @item_ns.response(200, 'Success')
    @item_ns.response(404, 'No Found Data', response_no_data_model)
    @item_ns.response(500, 'Internal Server Error', response_internal_server_error_model)
    def get():
        """Get All item data."""
        try:
            item_controller = ItemController
            result = item_controller.get_all_item()

            return result, constants.OK
        except DataNotFound as e:
            return e.__dict__, e.code
        except Exception as e:
            session.rollback()
            e = InternalServerError('Unknown Error')
            return e.__dict__, e.code


    @staticmethod
    @item_ns.response(201, 'Created')
    @item_ns.response(403, 'Forbidden', response_forbidden_model)
    def post(self):
        """Insert data for items that do not exist."""
        try:
            item_controller = ItemController()
            code = item_controller.insert_item()

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


    @staticmethod
    def put(self):
        """After deleting the item data, insert the item data."""
        try:
            res = self.delete()

            if res[1] != 204:
                return '', 500

            res = self.post()

            if res[1] != 204:
                return '', 500

            return '', 204
        except Exception as e:
            print(e)
            session.rollback()

    @staticmethod
    def delete(self):
        """Delete items data"""
        try:
            session.query(Item_model).delete()
            session.commit()

            status_code = 204
        except:
            session.rollback()
            status_code = 500

        return '', status_code


@item_ns.route('/<int:item_id>')
@item_ns.response(500, 'Internal Server Error')
class ItemWithId(Resource):
    @item_ns.response(200, 'Success')
    @item_ns.response(404, 'No Data', response_no_data_model)
    def get(self, item_id):
        """Get item data with item_id"""
        try:
            item = [x.serialize for x in session.query(Item_model).filter_by(item_id=item_id)]
            res = response.response_data(item)

            return res, res['statusCode']
        except:
            return '', 500
