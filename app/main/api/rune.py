import itertools
from urllib import request
from json import loads
from re import compile, sub

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

from app import session
from ..models.rune import Rune as Rune_model, response_model

from ..util import response, riot_url, version as version_util

rune_bp = Blueprint('rune_bp', __name__)
rune_ns = Namespace(
    'Rune',
    'Rune 관련 API입니다.',
    path='/runes'
)

response_model = rune_ns.model('Runes Response Model', {
    'results': fields.List(fields.String(response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = rune_ns.model('Rune No Data', {
    'statusCode': fields.Integer(404)
})


@rune_ns.route('/')
@rune_ns.response(500, 'Internal Server Error')
class AllRunes(Resource):
    @rune_ns.response(200, 'Success', response_model)
    @rune_ns.response(404, 'No Data', response_no_data_model)
    def get(self):
        """Get All Rune data."""
        try:
            items = [x.serialize for x in session.query(Rune_model).all()]
            res = response.response_data(items)
            print(items);
            return res, res['statusCode']
        except Exception as e :
            session.rollback()
            print(e);

    @rune_ns.response(204, 'Insert runes success')
    def post(self):
        """Insert data for Runes that do not exist."""
        try:
            version = version_util.get_version()
            url = riot_url.runes_url(version)


            with request.urlopen(url) as res:
                runes = loads(res.read().decode())

            #print(runes[0].items())
            # No data items
            if 'id' not in runes[0]:
                return {
                    'statusCode': 503
                }
            runes_with_api = []

            for i in range(len(runes)) :
                runes_with_api.append(Rune_model(
                    rune_id=runes[i]['id'],
                    eng_name=runes[i]['key'],
                    rune_icon=runes[i]['icon'],
                    kor_name=runes[i]['name'],
                    short_desc=" ",
                    long_desc=" "
                ))
                for j in range(len(runes[i]['slots'])) :
                    for rune in runes[i]['slots'][j]['runes']:
                        runes_with_api.append(Rune_model(
                            rune_id=rune['id'],
                            eng_name=rune['key'],
                            rune_icon = rune['icon'],
                            kor_name=rune['name'],
                            short_desc=rune['shortDesc'],
                            long_desc=rune['longDesc']
                        ))

            runes_with_db = [x.serialize for x in session.query(Rune_model).all()]

            set1 = set([x.rune_id for x in runes_with_api])
            set2 = set([x['rune_id'] for x in runes_with_db])

            not_runes = list(set1 - set2)
            runes = []

            if not_runes:
                for rune_id in not_runes:
                    idx = next((
                        index for (index, rune) in enumerate(runes_with_api)
                        if int(rune.rune_id) == int(rune_id)
                    ), None)

                    runes.append(runes_with_api[idx])

                session.add_all(runes)
                session.commit()

            status_code = 204
        except Exception as e:
            print(e)
            session.rollback()
            status_code = 500

        return '', status_code

    @rune_ns.response(204, 'Insert runes after Delete items')
    def put(self):
        """After deleting the rune data, insert the rune data."""
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

    @rune_ns.response(204, 'Delete runes success')
    def delete(self):
        """Delete Runes data"""
        try:
            session.query(Rune_model).delete()
            session.commit()

            status_code = 204
        except:
            session.rollback()
            status_code = 400

        return '', status_code


@rune_ns.route('/<string:rune_id>')
@rune_ns.response(500, 'Internal Server Error')
class RuneWithId(Resource):
    @rune_ns.response(200, 'Success', response_model)
    @rune_ns.response(404, 'No Data', response_no_data_model)
    def get(self, rune_id):
        """Get Rune data with rune_id"""
        try:
            rune = [x.serialize for x in session.query(Rune_model).filter_by(rune_id=rune_id)]
            res = response.response_data(rune)

            return res, res['statusCode']
        except:
            return '', 500


# @rune_ns.route('/')
# @rune_ns.response(500, 'Internal Server Error')
# class RuneImgTest(Resource):
#     @rune_ns.response(200, 'Success', response_model)
#     def test(self):
#         try:
#             print("테스뚱")
#         except:
#             print("실빠이")