import os
import sys
import math

import pygame

from get_map import Map

COORDINATES = ['37.620070', '55.753630']


class MapWindow(object):

    def __init__(self, width, height):
        self.z = 10
        self.w, self.h = width, height
        self.map = Map(COORDINATES, self.z)
        self.get_map()
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.flip()

    def get_point(self, x, y):
        parallel_multiplier = math.cos(float(COORDINATES[0]) * math.pi / 180)
        degrees_per_pixel_x = 360 / math.pow(2, self.z + 8)
        degrees_per_pixel_y = 360 / math.pow(2, self.z + 8) * parallel_multiplier
        point_lat = float(COORDINATES[0]) - degrees_per_pixel_y * (y - self.h / 2)
        point_lng = float(COORDINATES[1]) + degrees_per_pixel_x * (x - self.w / 2)

        return point_lat, point_lng

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    self.z += 1
                    if self.z <= 17:
                        self.map = Map(COORDINATES, self.z)
                        self.get_map()
                    else:
                        self.z = 17
                if event.key == pygame.K_PAGEDOWN:
                    self.z -= 1
                    if self.z >= 2:
                        self.map = Map(COORDINATES, self.z)
                        self.get_map()
                    else:
                        self.z = 2
            if event.type == pygame.MOUSEMOTION:
                point = self.get_point(event.pos[0], event.pos[1])

    def draw(self):
        self.screen.blit(pygame.image.load(os.path.join('map_parts/', self.map.name)), (0, 0))
        pygame.display.flip()
        self.update()

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
