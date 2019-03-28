import os
import sys

import pygame

from get_map import Map

COORDINATES = ['37.620070', '55.753630']


class MapWindow(object):

    def __init__(self, width, height):
        self.z = 10
        self.map = Map(COORDINATES, self.z)
        self.get_map()
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.flip()

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
                print(self.z)
            if event.type == pygame.MOUSEMOTION:
                print([float(coord) for coord in event.pos])

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
