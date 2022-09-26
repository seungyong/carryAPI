from urllib import parse


def champions_url(api_version):
    return f"https://ddragon.leagueoflegends.com/cdn/{api_version}/data/ko_KR/champion.json"


def champion_url(api_version, champion_name):
    return f"http://ddragon.leagueoflegends.com/cdn/{api_version}/data/ko_KR/champion/{champion_name}.json"


def item_url(api_version):
    return f"http://ddragon.leagueoflegends.com/cdn/{api_version}/data/ko_KR/item.json"


def version_url():
    return "https://ddragon.leagueoflegends.com/api/versions.json"


def spell_url(api_version):
    return f"https://ddragon.leagueoflegends.com/cdn/{api_version}/data/ko_KR/summoner.json"


def user_search_url(username):
    encode_username = parse.quote(username)
    return f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encode_username}"


def user_info_url(summoner_id):
    return f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"


def matches_url(puuid, start, count, queue=None):
    if queue is None:
        return f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    else:
        return f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&queue={queue}"

def matches_info_url(game_id):
    return f"https://asia.api.riotgames.com/lol/match/v5/matches/{game_id}"

def runes_url(api_version):
    return f"https://ddragon.leagueoflegends.com/cdn/{api_version}/data/ko_KR/runesReforged.json"