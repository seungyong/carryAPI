from app import session

from ..models.champion import Champion as ChampionModel
from ..util.single_ton import Singleton
from ..exception.data_not_found import DataNotFound


class ChampionController(metaclass=Singleton):
    @staticmethod
    def get_all_champion_name():
        champions_name = [dict(x) for x in session.query(ChampionModel).with_entities(ChampionModel.champion_id,
                                                                                      ChampionModel.kor_name,
                                                                                      ChampionModel.eng_name)]

        if champions_name:
            return champions_name
        else:
            raise DataNotFound('Not Found Champion')
