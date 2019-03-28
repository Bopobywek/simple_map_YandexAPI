import os
import sys

import pygame

from get_map import Map

COORDINATES = ['37', '55']
SPN = ['0.05', '0.05']


class MapWindow(object):

    def __init__(self, width, height):
        self.map = Map(COORDINATES, SPN)
        self.get_map()
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

    def draw(self):
        self.screen.blit(pygame.image.load(os.path.join('map_parts/', self.map.name)), (0, 0))
        pygame.display.flip()
        self.update()

    def get_map(self):
        try:
            self.map.get_map()
        except Exception as e:
            print('Возникла ошибка: {}. Работа программы завершена.'.format(e))
            pygame.quit()
            sys.exit(0)


map_show = MapWindow(600, 450)
while True:
    map_show.draw()
