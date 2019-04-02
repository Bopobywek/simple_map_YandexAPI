import pygame


class InfoField(object):

    def __init__(self, address):
        self.kill_state = False
        self.text = address
        self.inner_rect = pygame.Rect((15, 400), (300, 30))
        self.outer_rect = pygame.Rect((10, 395), (310, 40))

    def draw_text(self):
        font_text = pygame.font.Font('Oswald-Regular.ttf', 15)
        search_text = font_text.render(self.text, 1, pygame.Color('black'))
        self.inner_rect.width, self.inner_rect.height = search_text.get_width() + 20, search_text.get_height() + 5
        self.outer_rect.width, self.outer_rect.height = self.inner_rect.width + 10, self.inner_rect.height + 10
        return search_text

    def draw(self, screen):
        if not self.kill_state and self.text != '':
            pygame.draw.rect(screen, pygame.Color('yellow'), self.outer_rect)
            pygame.draw.rect(screen, pygame.Color('white'), self.inner_rect)
            screen.blit(self.draw_text(), (self.inner_rect.x + 5, self.inner_rect.y))

    def change_address(self, address):
        self.text = address

    def kill(self):
        self.kill_state = True

    def alive(self):
        self.kill_state = False
