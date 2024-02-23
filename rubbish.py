import pygame
import os
import sys
import random
from typing import Any


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_w = max(map(len, level_map))

    return list(map(lambda x: list(x.ljust(max_w, '.')), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y) -> None:
        super().__init__(tile_group, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(
            tile_w * pos_x, tile_h * pos_y
        )
        self.pos = (pos_x, pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(hero_group, all_sprites)
        self.image = player_img
        self.rect = self.image.get_rect().move(
            tile_w * pos_x, tile_h * pos_y
        )
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_w * x, tile_h * y
        )


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['1', '2', '3']
    screen.fill((23, 234, 123))
    font = pygame.font.Font(None, 40)
    text_coords = 50
    for line in intro_text:
        str_render = font.render(line, 1, pygame.Color("white"))
        intro_rect = str_render.get_rect()
        text_coords += 10
        intro_rect.top = text_coords
        intro_rect.x = 10
        text_coords += intro_rect.height
        screen.blit(str_render, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
    return new_player, x + 1, y + 1


def move(movement, hero):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level[y - 1][x] == '.':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < level_y - 1 and level[y + 1][x] == '.':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level[y][x - 1] == '.':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < level_x - 1 and level[y][x + 1] == '.':
            hero.move(x + 1, y)


if __name__ == '__main__':
    FPS = 100
    pygame.init()
    tile_w, tile_h = size = 50, 50

    tile_images = {
        'wall': pygame.transform.scale(load_image('box.png'), size),
        'empty': pygame.transform.scale(load_image('grass.png'), size)
    }
    player_img = pygame.transform.scale(load_image('mar.png', -1), size)

    all_sprites = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()

    player = None

    level = load_level(input())
    player, level_x, level_y = generate_level(level)

    screen = pygame.display.set_mode((level_x * tile_w, level_y * tile_h))

    clock = pygame.time.Clock()

    start_screen()

    running = True
    while running:
        screen.fill((0, 123, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move('up', player)
                elif event.key == pygame.K_DOWN:
                    move('down', player)
                elif event.key == pygame.K_RIGHT:
                    move('right', player)
                elif event.key == pygame.K_LEFT:
                    move('left', player)
        all_sprites.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    terminate()
