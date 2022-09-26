from app import session

from ..models.champion import Champion as ChampionModel

from ..util.response import response_data


class ChampionController:
    @staticmethod
    def get_all_champion_name():
        try:
            champions_name = [dict(x) for x in session.query(ChampionModel).with_entities(ChampionModel.champion_id,
                                                                                          ChampionModel.champion_name,
                                                                                          ChampionModel.eng_name)]

            result = response_data(champions_name)

            return result
        except Exception:
            return {'message': 'Internal Server Error', 'statusCode': 500}
