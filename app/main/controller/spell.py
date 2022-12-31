from json import loads
from urllib import request as url_request, parse

from app import session


from ..models.spell import Spell as SpellModel
from ..util.single_ton import Singleton

from ..util import response, riot_url, version as version_util
from re import compile, sub

from ..util.constants import *
from ..exception.data_not_found import DataNotFound

class SpellController(metaclass=Singleton):
    @staticmethod
    def spell_get():
        items = [x.serialize for x in session.query(SpellModel).all()]
        res = response.response_data(items)
        return res;

    @staticmethod
    def spell_post():
        version = version_util.get_version()
        url = riot_url.spell_url(version)

        with url_request.urlopen(url) as res:
            data = loads(res.read().decode())

        # No data items
        if 'data' not in data:
            return {
                'statusCode': 503
            }

        spells_with_api = []

        for key, spell in data['data'].items():
            spells_with_api.append(SpellModel(
                spell_id=spell['id'],
                name=spell['name'],
                description=spell['description'],
                cooldown=int(spell['cooldownBurn'])
            ))

        spells_with_db = [x.serialize for x in session.query(SpellModel).all()]

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

        return CREATED

    @staticmethod
    def spell_delete():
        session.query(SpellModel).delete()
        session.commit()
        return OK

    @staticmethod
    def spell_get_with_id(spell_id):
        spell = [x.serialize for x in session.query(SpellModel).filter_by(spell_id=spell_id)]
        res = response.response_data(spell)
        return res;