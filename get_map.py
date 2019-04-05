import os

import requests

from config import YANDEX_API_KEY
from distance import dist

URL_MAP = "http://static-maps.yandex.ru/1.x/"
URL_SEARCH_MAP = "https://search-maps.yandex.ru/v1/"

SEARCH_ORGANIZATION_SPN = '0.001,0.001'


class WritingFileException(BaseException):
    pass


class ResponseCode(BaseException):
    pass


class ResponseContent(BaseException):
    pass


class BadContent(BaseException):
    pass


class Map(object):

    def __init__(self, coordinates, z, pt, layer):
        self.coordinates = coordinates
        self.z = str(z)
        self.pt = pt
        self.layer = layer
        self.name = 'main_map.png'

    def search_org(self, coordinates):
        params = {
            'apikey': YANDEX_API_KEY,
            'll': ','.join(coordinates),
            'lang': 'ru_RU',
            'type': 'biz',
            'spn': SEARCH_ORGANIZATION_SPN,
            'rspn': 1,
            'results': '10'
        }
        response = requests.get(URL_SEARCH_MAP, params)
        self.error_handler(response)
        response = response.json()
        if bool(response.get('features')):
            index_obj = None
            for el in response['features']:
                if dist(el['geometry']['coordinates'], [float(x) for x in coordinates]) <= 50:
                    index_obj = response['features'].index(el)
                    break
            if index_obj is not None:
                org_object = response['features'][index_obj]
                org_coordinates = [str(x) for x in org_object['geometry']['coordinates']]
                org_name = org_object['properties']['name']
                org_address = org_object['properties']['CompanyMetaData']['address']
                return {'coordinates': org_coordinates, 'name': org_name, 'address': org_address}
            return None
        return None

    def get_map(self):
        map_params = {
            'll': ','.join(self.coordinates),
            'z': self.z,
            'pt': '~'.join(self.pt),
            'l': self.layer,
            'size': '600,450'
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


if __name__ == '__main__':
    pass
