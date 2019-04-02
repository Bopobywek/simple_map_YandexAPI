import pygame

from buttons import Button

TEXT_COLOR_INACTIVE = '#bfbfbf'
TEXT_COLOR_ACTIVE = 'black'


class InputField(object):

    def __init__(self, main_class):
        self.main_class = main_class
        self.clicked_on_area = False
        self.text = ''
        self.inner_rect = pygame.Rect((15, 10), (300, 30))
        self.outer_rect = pygame.Rect((10, 5), (310, 40))
        self.text_example = 'Поиск мест и адресов'

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('yellow'), self.outer_rect)
        pygame.draw.rect(screen, pygame.Color('white'), self.inner_rect)
        screen.blit(self.draw_text(), (self.inner_rect.x + 5, self.inner_rect.y))

    def draw_text(self):
        printed_text = self.text if self.text != '' else self.text_example
        printed_text = printed_text[len(printed_text) - 34:] if len(printed_text) > 34 else printed_text
        font_text = pygame.font.Font('Oswald-Regular.ttf', 17)
        text_color = TEXT_COLOR_ACTIVE if self.text != '' else TEXT_COLOR_INACTIVE
        search_text = font_text.render(printed_text, 1, pygame.Color(text_color))
        return search_text

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked_on_area = True if self.inner_rect.collidepoint(event.pos[0], event.pos[1]) else False
        if self.clicked_on_area:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[0:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.text != '':
                        self.main_class.search_object(self.text)
                else:
                    self.text += event.unicode
