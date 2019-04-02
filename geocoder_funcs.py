import requests

URL_GEOCODE = "http://geocode-maps.yandex.ru/1.x/"


class StatusCodeException(BaseException):
    pass


class ResponseContent(BaseException):
    pass


def get_response(input_object):
    request_params = {
        'geocode': input_object,
        'format': 'json'
    }
    response = requests.get(URL_GEOCODE, request_params)
    if response:
        if response.status_code != 200:
            raise StatusCodeException
        else:
            return response
    else:
        raise ResponseContent


def get_object_info(response):
    try:
        data = response.json()
        toponym = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        toponym_spn = [str(abs(float(toponym['boundedBy']['Envelope']['lowerCorner'].split()[x])
                           - float(toponym['boundedBy']['Envelope']['upperCorner'].split()[x]))) for x in range(2)]
        return {'coordinates': toponym_coodrinates, 'spn': toponym_spn}
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    print(get_object_info(get_response('лицей 1581')))
