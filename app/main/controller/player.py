from json import loads
from urllib import request as url_request
from urllib.error import HTTPError

from app import session


from ..models.player import Player as PlayerModel
from ..util.single_ton import Singleton

from ..util import response, riot_url, version as version_util
from re import compile, sub

from ..util.constants import *
from ..exception.data_not_found import DataNotFound
from ..exception.forbidden import Forbidden
from os import getenv
from datetime import datetime

class PlayerController(metaclass=Singleton):
    @staticmethod
    def insert_player(username):
        duplicated_player = [x.serialize for x in session.query(PlayerModel).filter_by(summoner_name=username)]
        if duplicated_player:
            return CREATED
        player = PlayerModel()
        url = riot_url.user_search_url(username)
        headers = {
            getenv('RIOT_HEADER_KEY'): getenv('RIOT_API_KEY')
        }
        req = url_request.Request(url, None, headers)
        try:
            with url_request.urlopen(req) as res:
                data = loads(res.read().decode())
        except HTTPError as e:
            if e.code == 403:
                raise Forbidden('Wrong Riot URL.')
            else:
                raise Exception
        player.summoner_id = data['id']
        player.puuid = data['puuid']
        player.profile_icon_id = data['profileIconId']
        player.summoner_name = data['name']
        player.level = data['summonerLevel']
        player.created_time = datetime.fromtimestamp(int(str(data['revisionDate'])[:-3]))
        url = riot_url.user_info_url(data['id'])
        req = url_request.Request(url, None, headers)
        try:
            with url_request.urlopen(req) as res:
                data = loads(res.read().decode())
        except HTTPError as e:
            if e.code == 403:
                raise Forbidden('Wrong Riot URL.')
            else:
                raise Exception


        for info in data:
            if info['queueType'] == 'RANKED_SOLO_5x5':
                player.solo_tier = info['tier']
                player.solo_rank = 1 if info['rank'] == 'I' else 2 if info['rank'] == 'II' else 3 if info['rank'] == 'III' else 4 if info['rank'] == 'IV' else 5
                player.solo_point = info['leaguePoints']
            elif info['queueType'] == 'RANKED_FLEX_SR':
                player.flex_tier = info['tier']
                player.flex_rank = 1 if info['rank'] == 'I' else 2 if info['rank'] == 'II' else 3 if info['rank'] == 'III' else 4 if info['rank'] == 'IV' else 5
                player.flex_point = info['leaguePoints']

            if info['queueType'] != 'RANKED_TFT_DOUBLE_UP':
                player.total_win += info['wins']
                player.total_lose += info['losses']
        session.add(player)
        session.commit()
        return CREATED

    @staticmethod
    def get_player(self, username):
        """Get player data with username."""
        players = [x.serialize for x in session.query(PlayerModel).filter_by(summoner_name=username)]

        if players:
            return players
        else:
            raise DataNotFound('Not Found Champion')