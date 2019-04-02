import os
import sys

import pygame

from get_map import Map
from buttons import LayersButton, SearchButton, ResetButton
from input_field import InputField
from geocoder_funcs import get_response, get_object_info


class MapWindow(object):
    SCALE_POSITIONS = ['0.0001', '0.001', '0.005', '0.01', '0.02', '0.03', '0.05', '0.1', '0.5', '1', '3', '6']

    def __init__(self, width, height):
        self.spn = ['0.01', '0.01']  # Долгота, широта
        self.coordinates = ['37.620070', '55.753630']  # Долгота (lon), Широта (lat)
        self.pts = list()
        self.type_layer = 'map'
        self.buttons = pygame.sprite.Group()
        self.l_btn = LayersButton(self.buttons, self)
        self.reset_btn = ResetButton(self.buttons, 51, 49, 'Сброс поискового результата', pygame.Color('white'), self)
        self.search = InputField(self)
        self.btn_search = SearchButton(self.buttons, self.search.outer_rect.x + 10 + self.search.outer_rect.width,
                                       self.search.outer_rect.y, self, self.search)
        self.map = Map(self.coordinates, self.spn, self.pts, self.type_layer)
        self.get_map()
        self.w, self.h = width, height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.flip()

    def update_map(self):
        self.map = Map(self.coordinates, self.spn, self.pts, self.type_layer)
        self.get_map()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if self.spn[0] not in self.SCALE_POSITIONS:
                        s_index = self.nearest_spn()
                        self.spn = [self.SCALE_POSITIONS[s_index] for _ in range(2)]
                    self.spn = [self.SCALE_POSITIONS[self.SCALE_POSITIONS.index(self.spn[i]) - 1]
                                for i in range(2)] if self.SCALE_POSITIONS.index(self.spn[0]) - 1 >= 0 else self.spn
                    self.update_map()
                if event.key == pygame.K_PAGEDOWN:
                    if self.spn[0] not in self.SCALE_POSITIONS:
                        s_index = self.nearest_spn()
                        self.spn = [self.SCALE_POSITIONS[s_index] for _ in range(2)]
                    self.spn = [self.SCALE_POSITIONS[self.SCALE_POSITIONS.index(self.spn[i]) + 1]
                                for i in range(2)] if self.SCALE_POSITIONS.index(self.spn[0]) + 1 < \
                                                      len(self.SCALE_POSITIONS) else self.spn
                    self.update_map()
                if event.key == pygame.K_DOWN:
                    if float(self.coordinates[1]) - float(self.spn[1]) < -82:
                        self.coordinates = [self.coordinates[0], str(-82 + float(self.spn[1]))]
                    self.coordinates = self.coordinates[0], str(float(self.coordinates[1]) - float(self.spn[1]))
                    self.update_map()
                if event.key == pygame.K_UP:
                    if float(self.coordinates[1]) + float(self.spn[1]) > 85:
                        self.coordinates = [self.coordinates[0], str(85 - float(self.spn[1]))]
                    self.coordinates = self.coordinates[0], str(float(self.coordinates[1]) + float(self.spn[1]))
                    self.update_map()
                if event.key == pygame.K_LEFT:
                    if float(self.coordinates[0]) - float(self.spn[1]) < -172:
                        self.coordinates = [str(-172 + float(self.spn[1])), self.coordinates[1]]
                    self.coordinates = str(float(self.coordinates[0]) - float(self.spn[0])), self.coordinates[1]
                    self.update_map()
                if event.key == pygame.K_RIGHT:
                    if float(self.coordinates[0]) + float(self.spn[1]) > 178:
                        self.coordinates = [str(178 - float(self.spn[1])), self.coordinates[1]]
                    self.coordinates = str(float(self.coordinates[0]) + float(self.spn[0])), self.coordinates[1]
                    self.update_map()
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            self.l_btn.update(event)
            self.search.update(event)
            self.btn_search.update(event)
            self.reset_btn.update(event)

    def draw(self):
        self.screen.blit(pygame.image.load(os.path.join('map_parts/', self.map.name)), (0, 0))
        self.l_btn.draw(self.screen)
        self.search.draw(self.screen)
        self.btn_search.draw(self.screen)
        self.reset_btn.draw(self.screen)
        pygame.display.flip()
        self.update()

    def append_pt(self, lon, lat):
        self.pts.append('{},{},round'.format(lon, lat))

    def search_object(self, text):
        self.pts.clear()
        self.search.text = ''
        data = get_object_info(get_response(text))
        if data is not None:
            coords = data['coordinates'][0], data['coordinates'][1]
            self.append_pt(coords[0], coords[1])
            self.coordinates = coords
            self.spn = data['spn']
            self.update_map()

    def nearest_spn(self):
        list_index = 0
        best_res = 100
        for el in self.SCALE_POSITIONS:
            if float(el) - float(self.spn[0]) < best_res:
                best_res = abs(float(el) - float(self.spn[0]))
                list_index = self.SCALE_POSITIONS.index(el)
        return list_index

    def pixels_in_lon_lat(self, x, y):
        left_corner = [str(float(self.coordinates[0]) - float(self.spn[0]) / 2),
                       str(float(self.coordinates[1]) + float(self.spn[1]) / 2)]
        lon_px, lat_px = float(self.spn[0]) / self.w, float(self.spn[1]) / self.h
        lon = float(left_corner[0]) + lon_px * float(x)
        lat = float(left_corner[1]) + lat_px * float(y)
        return lon, lat

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
