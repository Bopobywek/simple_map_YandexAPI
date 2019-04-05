import os
import math
import sys

import pygame

from get_map import Map
from buttons import LayersButton, SearchButton, ResetButton, CheckButton
from input_field import InputField
from geocoder_funcs import get_response, get_object_info
from info_field import InfoField


class MapWindow(object):
    LON_STEP, LAT_STEP = 0.02, 0.008

    def __init__(self, width, height):
        self.z = 15
        self.coordinates = ['37.620070', '55.753630']  # Долгота (lon), Широта (lat)
        self.pts = list()
        self.type_layer = 'map'
        self.org = ''
        self.buttons = pygame.sprite.Group()
        self.l_btn = LayersButton(self.buttons, self)
        self.reset_btn = ResetButton(self.buttons, 10, 49, 'Сброс поискового результата', self)
        self.search = InputField(self)
        self.btn_search = SearchButton(self.buttons, self.search.outer_rect.x + 10 + self.search.outer_rect.width,
                                       self.search.outer_rect.y, self, self.search)
        self.postal_code_btn = CheckButton(self.buttons, self)
        self.info = InfoField('')
        self.last_search = ''
        self.map = Map(self.coordinates, self.z, self.pts, self.type_layer)
        self.get_map()
        self.w, self.h = width, height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.flip()

    def update_map(self):
        self.map = Map(self.coordinates, self.z, self.pts, self.type_layer)
        self.get_map()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    self.z = self.z + 1 if self.z < 19 else 19
                    self.update_map()
                if event.key == pygame.K_PAGEDOWN:
                    self.z = self.z - 1 if self.z > 2 else 2
                    self.update_map()
                if event.key == pygame.K_DOWN:
                    lat = self.LAT_STEP * math.pow(2, 15 - self.z)
                    lat = 70 + float(self.coordinates[1]) if float(self.coordinates[1]) - lat < -70 else lat
                    self.coordinates = self.coordinates[0], str(float(self.coordinates[1]) - lat)
                    self.update_map()
                if event.key == pygame.K_UP:
                    lat = self.LAT_STEP * math.pow(2, 15 - self.z)
                    lat = 70 - float(self.coordinates[1]) if float(self.coordinates[1]) + lat > 70 else lat
                    self.coordinates = self.coordinates[0], str(float(self.coordinates[1]) + lat)
                    self.update_map()
                if event.key == pygame.K_LEFT:
                    lon = self.LON_STEP * math.pow(2, 15 - self.z)
                    lon = 160 + float(self.coordinates[0]) if float(self.coordinates[0]) - lon < -160 else lon
                    self.coordinates = str(float(self.coordinates[0]) - lon), self.coordinates[1]
                    self.update_map()
                if event.key == pygame.K_RIGHT:
                    lon = self.LON_STEP * math.pow(2, 15 - self.z)
                    lon = 160 - float(self.coordinates[0]) if float(self.coordinates[0]) + lon > 160 else lon
                    self.coordinates = str(float(self.coordinates[0]) + lon), self.coordinates[1]
                    self.update_map()
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                btns_array = [self.postal_code_btn.rect.collidepoint(event.pos[0], event.pos[1]),
                              self.l_btn.rect.collidepoint(event.pos[0], event.pos[1]),
                              self.search.outer_rect.collidepoint(event.pos[0], event.pos[1]),
                              self.reset_btn.rect.collidepoint(event.pos[0], event.pos[1]),
                              self.btn_search.rect.collidepoint(event.pos[0], event.pos[1])]
                btns_array.extend([x.rect.collidepoint(event.pos[0], event.pos[1]) for x in self.l_btn.layers_buttons])
                if not any(btns_array):
                    step_lon, step_lat, upper_corner_left = self.get_step()
                    coordinates = [str(float(upper_corner_left[0]) + step_lon * event.pos[0]),
                                   str(float(upper_corner_left[1]) - step_lat * event.pos[1])]
                    if event.button == 1:
                        self.reset_search()
                        self.append_pt(coordinates[0], coordinates[1])
                        self.search_object(','.join(x for x in coordinates), type_of_request='click')
                    elif event.button == 3:
                        self.reset_search()
                        data = self.map.search_org(coordinates)
                        if data is not None:
                            self.org = data.get('name', '')
                            org_coordinates = data.get('coordinates')
                            self.append_pt(org_coordinates[0], org_coordinates[1])
                            self.search_object(','.join(data.get('coordinates')), type_of_request='click', org=True)

            self.l_btn.update(event)
            self.search.update(event)
            self.btn_search.update(event)
            self.reset_btn.update(event)
            self.postal_code_btn.update(event)

    def draw(self):
        self.screen.blit(pygame.image.load(os.path.join('map_parts/', self.map.name)), (0, 0))
        self.l_btn.draw(self.screen)
        self.search.draw(self.screen)
        self.btn_search.draw(self.screen)
        self.reset_btn.draw(self.screen)
        self.info.draw(self.screen)
        self.postal_code_btn.draw(self.screen)
        pygame.display.flip()
        self.update()

    def get_step(self):
        lon = self.LON_STEP * math.pow(2, 15 - self.z) / 1.55
        lat = self.LAT_STEP * math.pow(2, 15 - self.z) / 1.47
        upper_corner_right = str(float(self.coordinates[0]) + lon), str(float(self.coordinates[1]) + lat)
        lower_corner_left = str(float(self.coordinates[0]) - lon), str(float(self.coordinates[1]) - lat)
        upper_corner_left = str(float(self.coordinates[0]) - lon), str(float(self.coordinates[1]) + lat)
        step_lon = abs(float(lower_corner_left[0]) - float(upper_corner_right[0])) / self.w
        step_lat = abs(float(lower_corner_left[1]) - float(upper_corner_right[1])) / self.h
        return step_lon, step_lat, upper_corner_left

    def append_pt(self, lon, lat):
        self.pts.append('{},{},round'.format(lon, lat))

    def reset_search(self):
        self.pts.clear()
        self.org = ''
        self.last_search = ''
        self.info.change_address('')
        self.update_map()

    def update_search(self):
        self.search_object(self.last_search)

    def search_object(self, text, type_of_request=None, org=False):
        if text != '':
            self.last_search = text
            if type_of_request is None:
                self.pts.clear()
                self.search.text = ''
                data = get_object_info(get_response(text))
                if data is not None:
                    coords = data.get('coordinates')[0], data.get('coordinates')[1]
                    self.append_pt(coords[0], coords[1])
                    self.coordinates = coords
                    if self.postal_code_btn.state:
                        if org:
                            self.info.change_address('{}, {}. Индекс: {}'.format(data.get('address'),
                                                                                 self.org,
                                                                                 data.get('postal_code')))
                        else:
                            self.info.change_address('{}. Индекс: {}'.format(data.get('address'),
                                                                             data.get('postal_code')))
                    else:
                        if org:
                            self.info.change_address('{}, {}'.format(data.get('address'), self.org))
                        else:
                            self.info.change_address(data.get('address'))
            else:
                data = get_object_info(get_response(text))
                if data is not None:
                    self.coordinates = text.split(',')
                    if self.postal_code_btn.state:
                        if org:
                            self.info.change_address('{}, {}. Индекс: {}'.format(data.get('address'),
                                                                                 self.org,
                                                                                 data.get('postal_code')))
                        else:
                            self.info.change_address('{}. Индекс: {}'.format(data.get('address'),
                                                                             data.get('postal_code')))
                    else:
                        if org:
                            self.info.change_address('{}, {}'.format(data.get('address'), self.org))
                        else:
                            self.info.change_address(data.get('address'))
            self.update_map()

    def get_map(self):
        try:
            self.map.get_map()
        except BaseException as e:
            print('Возникла ошибка при получении карты: {}. Работа программы завершена.'.format(e))
            pygame.quit()
            sys.exit(0)


map_show = MapWindow(600, 450)
while True:
    map_show.draw()
