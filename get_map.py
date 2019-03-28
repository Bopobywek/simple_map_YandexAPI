import os

import requests

from config import YANDEX_API_KEY

URL_GEOCODE = "http://geocode-maps.yandex.ru/1.x/"
URL_MAP = "http://static-maps.yandex.ru/1.x/"
URL_SEARCH_MAP = "https://search-maps.yandex.ru/v1/"


class WritingFileException(BaseException):
    pass


class ResponseCode(BaseException):
    pass


class ResponseContent(BaseException):
    pass


class Map(object):

    def __init__(self, coordinates, spn):
        self.coordinates = coordinates
        self.spn = spn
        self.name = 'main_map.png'

    def get_map(self):
        map_params = {
            'll': ','.join(self.coordinates),
            'spn': ','.join(self.spn),
            'l': 'map'
        }
        response = requests.get(URL_MAP, map_params)
        self.error_handler(response)
        self.save_map(response)

    def save_map(self, content):
        try:
            file = os.path.join('map_parts/', self.name)
            with open(file, mode='wb') as fout:
                fout.write(content.content)
        except IOError:
            raise WritingFileException('Ошибка записи файла')
        except Exception as e:
            raise WritingFileException('Ошибка при записи файла: {}'.format(e))

    @staticmethod
    def error_handler(response):
        if response is None:
            raise ResponseContent('Response content is empty')
        elif response.status_code != 200:
            raise ResponseCode('Response status code is {}'.format(response.status_code))
