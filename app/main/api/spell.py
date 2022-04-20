from urllib import request
from json import loads
from re import compile, sub

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

from app import session
from ..models.spell import Spell as Spell_model, response_model

from ..util import response, riot_url, version as version_util

spell_bp = Blueprint('spell_bp', __name__)
spell_ns = Namespace(
    'Spell',
    'Spell 관련 API입니다.',
    path='/spells'
)

response_model = spell_ns.model('Spell Response Model', {
    'results': fields.List(fields.String(response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = spell_ns.model('Spell No Data', {
    'statusCode': fields.Integer(404)
})


@spell_ns.route('/')
@spell_ns.response(500, 'Internal Server Error')
class AllItem(Resource):
    @spell_ns.response(200, 'Success', response_model)
    @spell_ns.response(404, 'No Data', response_no_data_model)
    def get(self):
        """Get All spell data."""
        try:
            items = [x.serialize for x in session.query(Spell_model).all()]
            res = response.response_data(items)

            return res, res['statusCode']
        except:
            session.rollback()

    @spell_ns.response(204, 'Insert spells success')
    def post(self):
        """Insert data for spells that do not exist."""
        try:
            version = version_util.get_version()
            url = riot_url.spell_url(version)

            with request.urlopen(url) as res:
                data = loads(res.read().decode())

            # No data items
            if 'data' not in data:
                return {
                    'statusCode': 503
                }

            spells_with_api = []

            for key, spell in data['data'].items():
                spells_with_api.append(Spell_model(
                    spell_id=spell['id'],
                    name=spell['name'],
                    description=spell['description'],
                    cooldown=int(spell['cooldownBurn'])
                ))

            spells_with_db = [x.serialize for x in session.query(Spell_model).all()]

            set1 = set([x.spell_id for x in spells_with_api])
            set2 = set([x['spell_id'] for x in spells_with_db])

            not_spells = list(set1 - set2)
            spells = []

            if not_spells:
                for spell_id in not_spells:
                    idx = next((
                        index for (index, spell) in enumerate(spells_with_api)
                        if spell.spell_id == spell_id
                    ), None)

                    spells.append(spells_with_api[idx])

                session.add_all(spells)
                session.commit()

            status_code = 204
        except Exception as e:
            print(e)
            session.rollback()
            status_code = 500

        return '', status_code

    @spell_ns.response(204, 'Insert spells after Delete items')
    def put(self):
        """After deleting the spell data, insert the spell data."""
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
            session.query(Spell_model).delete()
            session.commit()

            status_code = 204
        except:
            session.rollback()
            status_code = 500

        return '', status_code


@spell_ns.route('/<string:spell_id>')
@spell_ns.response(500, 'Internal Server Error')
class SpellWithId(Resource):
    @spell_ns.response(200, 'Success', response_model)
    @spell_ns.response(404, 'No Data', response_no_data_model)
    def get(self, spell_id):
        """Get Spell data with spell_id"""
        try:
            spell = [x.serialize for x in session.query(Spell_model).filter_by(spell_id=spell_id)]
            res = response.response_data(spell)

            return res, res['statusCode']
        except:
            return '', 500
