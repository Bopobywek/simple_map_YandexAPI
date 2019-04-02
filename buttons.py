import os

import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, group, x, y, text, color, class_with_layer, func=None):
        super().__init__(group)
        self.layer_class = class_with_layer
        pygame.font.init()
        self.text = text
        self.font_button = pygame.font.Font('Oswald-Regular.ttf', 20)
        self.text_button = self.font_button.render(text, 1, pygame.Color('black'))
        self.image = pygame.Surface((80, 25))
        self.image.fill(color)
        self.func = func
        self.image.set_alpha(25)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text_button, (self.rect.x + self.rect.width // 2 - self.text_button.get_width() // 2,
                                       self.rect.y - 5))

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.image.set_alpha(1000)
            else:
                self.image.set_alpha(50)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.image.set_alpha(1000)
                self.text_button.set_alpha(1000)
                self.text_button = self.font_button.render(self.text, 1, pygame.Color('grey'))
                if self.func is not None:
                    self.layer_class.type_layer = self.func
                    self.layer_class.update_map()
            else:
                self.image.set_alpha(0)
                self.text_button = self.font_button.render(self.text, 1, pygame.Color('black'))


class LayersButton(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load(os.path.join('images/', 'layers.png')), (40, 40))

    def __init__(self, group, map_class):
        super().__init__(group)
        self.layers_buttons = [Button(group, 510, 50, 'схема', pygame.Color('white'), map_class, 'map'),
                               Button(group, 510, 80, 'спутник', pygame.Color('white'), map_class, 'sat'),
                               Button(group, 510, 110, 'гибрид', pygame.Color('white'), map_class, 'sat,skl')]
        self.rect = self.image.get_rect()
        self.open = False
        self.rect.x, self.rect.y = 540, 5

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.open:
            for btn in self.layers_buttons:
                btn.draw(screen)

    def update(self, event):
        if self.open:
            for btn in self.layers_buttons:
                btn.update(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.open = True if self.open is False else False


class SearchButton(pygame.sprite.Sprite):
    image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('images/', 'search.png')),
                                                         (35, 33)), True, False)

    def __init__(self, group, x, y, main_class, i_field_class):
        super().__init__(group)
        self.i_field_class = i_field_class
        self.main_class = main_class
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                text = self.i_field_class.text
                if text != '':
                    self.main_class.search_object(text)


class ResetButton(pygame.sprite.Sprite):

    def __init__(self, group, x, y, text, color, main_class):
        super().__init__(group)
        self.main_class = main_class
        pygame.font.init()
        self.text = text
        self.font_button = pygame.font.Font('Oswald-Regular.ttf', 15)
        self.text_button = self.font_button.render(text, 1, pygame.Color('black'))
        self.image = pygame.Surface((80, 15), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text_button, (self.rect.x + self.rect.width // 2 - self.text_button.get_width() // 2,
                                       self.rect.y - 5))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.main_class.reset_search()
