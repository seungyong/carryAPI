from .riot_url import version_url
from urllib import request
from json import loads


def get_version():
    with request.urlopen(version_url()) as res:
        data = loads(res.read().decode())

    return data[0]
