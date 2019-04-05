import pygame


class InfoField(object):

    def __init__(self, address):
        self.kill_state = False
        self.text = address
        self.inner_rect = pygame.Rect((15, 380), (300, 30))
        self.outer_rect = pygame.Rect((10, 375), (310, 40))

    def draw_text(self):
        font_text = pygame.font.Font('Oswald-Regular.ttf', 15)
        words = self.text.split()
        search_text, search_text2 = None, None
        for i in range(len(words)):
            search_text = font_text.render(' '.join(words[:i + 1]), 1, pygame.Color('black'))
            if search_text.get_width() > 500:
                if i > 0:
                    search_text = font_text.render(' '.join(words[:i]), 1, pygame.Color('black'))
                    search_text2 = font_text.render(' '.join(words[i:]), 1, pygame.Color('black'))
                    break
        if search_text is not None:
            if search_text2 is not None:
                self.outer_rect.y, self.inner_rect.y = 375, 380
                self.inner_rect.width, self.inner_rect.height = \
                    search_text.get_width() + 20, search_text.get_height() + search_text2.get_height() + 5
                self.outer_rect.width, self.outer_rect.height = self.inner_rect.width + 10, self.inner_rect.height + 10
            else:
                self.outer_rect.y, self.inner_rect.y = 395, 400
                self.inner_rect.width, self.inner_rect.height = \
                    search_text.get_width() + 20, search_text.get_height() + 5
                self.outer_rect.width, self.outer_rect.height = self.inner_rect.width + 10, self.inner_rect.height + 10
        return search_text, search_text2

    def draw(self, screen):
        if not self.kill_state and self.text != '':
            texts = self.draw_text()
            pygame.draw.rect(screen, pygame.Color('yellow'), self.outer_rect)
            pygame.draw.rect(screen, pygame.Color('white'), self.inner_rect)
            if texts[0] is not None:
                screen.blit(texts[0], (self.inner_rect.x + 5, self.inner_rect.y))
            if texts[1] is not None:
                screen.blit(texts[1], (self.inner_rect.x + 5, self.inner_rect.y + 20))

    def change_address(self, address):
        self.text = address

    def kill(self):
        self.kill_state = True

    def alive(self):
        self.kill_state = False
