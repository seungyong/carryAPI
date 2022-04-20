import urllib.error
from os import getenv
from urllib import request
from json import loads

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

from app import session
from ..models.player import Player as Player_model, response_model

from ..util import response, riot_url, version as version_util

player_bp = Blueprint('player_bp', __name__)
player_ns = Namespace(
    'Player',
    'Player 관련 API입니다.',
    path='/players'
)

response_model = player_ns.model('Player Response Model', {
    'results': fields.List(fields.String(response_model())),
    'statusCode': fields.Integer(200)
})

response_no_data_model = player_ns.model('Player No Data', {
    'statusCode': fields.Integer(404)
})


@player_ns.route('/<string:username>')
@player_ns.response(500, 'Internal Server Error')
class GameWithUsername(Resource):
    @player_ns.response(200, 'Success', response_model)
    @player_ns.response(404, 'No Data', response_no_data_model)
    def get(self, username):
        """Get player data with username."""
        players = [x.serialize for x in session.query(Player_model).filter_by(username=username)]
        res = response.response_data(players)

        return res, res['statusCode']

    @player_ns.response(200, 'Success Insert User Data', response_model)
    @player_ns.response(400, 'Already User Data')
    @player_ns.response(404, 'No Search User Data')
    def post(self, username):
        """Insert player data with username."""
        duplicated_player = [x.serialize for x in session.query(Player_model).filter_by(username=username)]

        if duplicated_player:
            return '', 400

        player = Player_model()

        url = riot_url.user_search_url(username)
        headers = {
            getenv('RIOT_HEADER_KEY'): getenv('RIOT_API_KEY')
        }
        req = request.Request(url, None, headers)
        data = {}

        try:
            with request.urlopen(req) as res:
                data = loads(res.read().decode())
        except urllib.error.HTTPError as error:
            # User Not Found
            if error.status == 404:
                return '', 404

        player.summoner_id = data['id']
        player.puuid = data['puuid']
        player.profile_icon_id = data['profileIconId']
        player.username = data['name']
        player.level = data['summonerLevel']

        url = riot_url.user_info_url(data['id'])
        req = request.Request(url, None, headers)
        data = {}

        try:
            with request.urlopen(req) as res:
                data = loads(res.read().decode())
        except urllib.error.HTTPError as error:
            # Bad Request with summoner_id
            if error.status == 400:
                return '', 404

        total_win = 0
        total_lose = 0

        for info in data:
            if info['queueType'] == 'RANKED_SOLO_5x5':
                player.solo_tier = info['tier']
                player.solo_rank = info['rank']
                player.solo_point = info['leaguePoints']
            elif info['queueType'] == 'RANKED_FLEX_SR':
                player.flex_tier = info['tier']
                player.flex_rank = info['rank']
                player.flex_point = info['leaguePoints']

            total_win += info['wins']
            total_lose += info['losses']

        player.total_win = total_win
        player.total_lose = total_lose

        session.add(player)
        session.commit()

        res = response.response_data([player.serialize])

        return res, 200
