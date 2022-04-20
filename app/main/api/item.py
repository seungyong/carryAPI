from urllib import request
from json import loads
from re import compile, sub

from flask import Blueprint
from flask_restx import Namespace, Resource, fields
from sqlalchemy.testing.exclusions import tags

from app import session
from ..models.item import Item as Item_model, response_model

from ..util import response, riot_url, version as version_util

item_bp = Blueprint('item_bp', __name__)
item_ns = Namespace(
    'Item',
    'item 관련 API입니다.',
    path='/items'
)

response_model = item_ns.model('Item Response Model', {
    'results': fields.List(fields.String(response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = item_ns.model('Item No Data', {
    'statusCode': fields.Integer(404)
})


@item_ns.route('/')
@item_ns.response(500, 'Internal Server Error')
class AllItem(Resource):
    @item_ns.response(200, 'Success', response_model)
    @item_ns.response(404, 'No Data', response_no_data_model)
    def get(self):
        """Get All item data."""
        try:
            items = [x.serialize for x in session.query(Item_model).all()]
            res = response.response_data(items)

            return res, res['statusCode']
        except:
            session.rollback()

    @item_ns.response(204, 'Insert items success')
    def post(self):
        """Insert data for items that do not exist."""
        try:
            version = version_util.get_version()
            url = riot_url.item_url(version)

            with request.urlopen(url) as res:
                data = loads(res.read().decode())

            # No data items
            if 'data' not in data:
                return {
                    'statusCode': 503
                }

            items_with_api = []
            cleaner = compile('<(?!br|/br).+?>')

            for key, item in data['data'].items():
                description = sub(cleaner, '', item['description'])

                if not item['gold']['purchasable']:
                    continue
                elif 'into' in item or item['gold']['total'] < 1500:
                    items_with_api.append(Item_model(
                        item_id=key,
                        name=item['name'],
                        description=description,
                        plain_text=item['plaintext'],
                        price=item['gold']['total'],
                        sell=item['gold']['sell'],
                        tags=','.join(item['tags']),
                        item_grade=0
                    ))
                else:
                    items_with_api.append(Item_model(
                        item_id=key,
                        name=item['name'],
                        description=description,
                        plain_text=item['plaintext'],
                        price=item['gold']['total'],
                        sell=item['gold']['sell'],
                        tags=','.join(item['tags']),
                        item_grade=2 if 'rarityMythic' in item['description'] else 1
                    ))

            items_with_db = [x.serialize for x in session.query(Item_model).all()]

            set1 = set([int(x.item_id) for x in items_with_api])
            set2 = set([int(x['item_id']) for x in items_with_db])

            not_items = list(set1 - set2)
            items = []

            if not_items:
                for item_id in not_items:
                    idx = next((
                        index for (index, item) in enumerate(items_with_api)
                        if int(item.item_id) == int(item_id)
                    ), None)

                    items.append(items_with_api[idx])

                session.add_all(items)
                session.commit()

            status_code = 204
        except:
            session.rollback()
            status_code = 500

        return '', status_code

    @item_ns.response(204, 'Insert items after Delete items')
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

    @item_ns.response(204, 'Delete items success')
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
    @item_ns.response(200, 'Success', response_model)
    @item_ns.response(404, 'No Data', response_no_data_model)
    def get(self, item_id):
        """Get item data with item_id"""
        try:
            item = [x.serialize for x in session.query(Item_model).filter_by(item_id=item_id)]
            res = response.response_data(item)

            return res, res['statusCode']
        except:
            return '', 500
