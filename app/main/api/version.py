from urllib import request, parse
from json import loads

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

VERSION_URL = 'https://ddragon.leagueoflegends.com/api/versions.json'

version_bp = Blueprint('version_bp', __name__)
version_ns = Namespace(
    'Version',
    'Version 관련 API입니다.',
    path='/version'
)

response_model = version_ns.model('Version Response Model', {
    'results': fields.List(fields.String('12.5.1')),
    'statusCode': fields.Integer(200)
})


@version_ns.route('/')
@version_ns.response(500, 'Internal Server Error')
class Version(Resource):
    @version_ns.response(200, 'Success', response_model)
    def post(self):
        """Get League Of Legends Version."""
        try:
            with request.urlopen(VERSION_URL) as url:
                data = loads(url.read().decode())

            if len(data) > 0:
                res = {
                    'results': [data[0]],
                    'statusCode': 200
                }
        except:
            res = {
                'statusCode': 503
            }

        return res, res['statusCode']
