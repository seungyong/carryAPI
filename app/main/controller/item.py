from json import loads
from urllib import request as url_request, parse

from app import session


from ..models.item import Item as ItemModel
from ..util.single_ton import Singleton

from ..util import response, riot_url, version as version_util
from re import compile, sub

from ..util.constants import *
from ..exception.data_not_found import DataNotFound

class ItemController(metaclass=Singleton):
    @staticmethod
    def insert_item():
        try:
            version = version_util.get_version()
            url = riot_url.item_url(version)

            with url_request.urlopen(url) as res:
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
                    items_with_api.append(ItemModel(
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
                    items_with_api.append(ItemModel(
                        item_id=key,
                        name=item['name'],
                        description=description,
                        plain_text=item['plaintext'],
                        price=item['gold']['total'],
                        sell=item['gold']['sell'],
                        tags=','.join(item['tags']),
                        item_grade=2 if 'rarityMythic' in item['description'] else 1
                    ))

            items_with_db = [x.serialize for x in session.query(ItemModel).all()]

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

            status_code = CREATED
        except:
            session.rollback()
            status_code = 500

        return '', status_code

    @staticmethod
    def get_all_item():
        items = [ x.serialize for x in session.query(ItemModel).all()]
        #res = response.response_data(items)
        if items:
            return items
        else:
            raise DataNotFound('Not Found Item Data')

    @staticmethod
    def get_item_with_id(item_id):
        item = [ dict(x) for x in session.query(ItemModel).with_entities(ItemModel.item_id,
                                                                         ItemModel.name,
                                                                         ItemModel.description,
                                                                         ItemModel.plain_text,
                                                                         ItemModel.price,
                                                                         ItemModel.sell,
                                                                         ItemModel.tags,
                                                                         ItemModel.item_grade
                                                                         ).filter_by(item_id=item_id)]
        if item:
            return item
        else:
            raise DataNotFound('Not Found Item Data')







        # try:
        #     items = [x.serialize for x in session.query(Item_model).all()]
        #     res = response.response_data(items)
        #
        #     return res, res['statusCode']
        # except:
        #     session.rollback()
