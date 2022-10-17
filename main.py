import random
import time

import pygame

TILE_SIZE = 150
BORDER_SIZE = 40
ROWS, COLUMNS = 3, 3
WIDTH, HEIGHT = 610, 750
TOP_PANEL_HEIGHT = 100

pygame.display.set_caption("Simple Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Tile():
    unclicked_tile_img = pygame.image.load('UNCLICKED_TILE.png').convert_alpha()
    unclicked_tile_img = pygame.transform.scale(unclicked_tile_img, (TILE_SIZE, TILE_SIZE))
    clicked_tile_img = pygame.image.load('CLICKED_TILE.png').convert_alpha()
    clicked_tile_img = pygame.transform.scale(clicked_tile_img, (TILE_SIZE, TILE_SIZE))

    def __init__(self, num, x, y):
        self.num = num
        self.image = Tile.unclicked_tile_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def turn_on(self):
        self.image = Tile.clicked_tile_img

    def turn_off(self):
        self.image = Tile.unclicked_tile_img

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def intersects(self, mousePos):
        return self.rect.collidepoint(mousePos)

class SequenceGenerator():

    def __init__(self):
        self.iterator = -1
        self.sequence = []
        self.prev_tile_num = random.randint(1, 9)
        self.show_sequence = True

    def generate_next_tile(self):
        adder = random.randint(1, 8) % 8
        new_tile_num = (self.prev_tile_num + adder + 1) % 9
        self.sequence.append(new_tile_num)
        self.prev_tile_num = new_tile_num

    def iter_next(self):
        if self.iterator+1 >= len(self.sequence):
            self.iterator = -1

        self.iterator += 1
        return self.sequence[self.iterator]



num = 1
tiles = []
y = BORDER_SIZE * 2 + TOP_PANEL_HEIGHT
for r in range(ROWS):
    x = BORDER_SIZE
    for c in range(COLUMNS):
        tiles.append(Tile(num, x, y))
        x += 190
        num += 1
    y += 190

def get_clicked_tile():
    mousePos = pygame.mouse.get_pos()
    return next((t for t in tiles if t.intersects(mousePos)), None)

def mouse_hovered():
    mousePos = pygame.mouse.get_pos()
    return any(t for t in tiles if t.intersects(mousePos))

pygame.init()

click_count = 0
correct_count = 0

sequence_time = 0
sequence_time_elapsed = 0

next_level_time = 0
next_level_time_elapsed = 0

current_tile = None
clicked_tile = None
gen = SequenceGenerator()

run = True
player_turn = False
generate_new_tile = True
continue_sequence = False
proceed_next_level = False

start = True
while run:
    screen.fill((0, 162, 232))
    for tile in tiles:
        tile.draw()


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION:
            if mouse_hovered():
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if event.type == pygame.MOUSEBUTTONDOWN and start:
            next_level_time = pygame.time.get_ticks()
            start = False

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            print("MOUSEBUTTONDOWN")
            clicked_tile = get_clicked_tile()

            if clicked_tile:
                if gen.iter_next()+1 == clicked_tile.num:
                    print("CORRECT")
                    clicked_tile.turn_on()

                    if click_count + 1 < len(gen.sequence):
                        click_count += 1
                    else:
                        click_count = 0
                        correct_count += 1
                        proceed_next_level = True
                        gen.iterator = -1
                        print("PROCEED NEXT LEVEL")

                else:
                    print("GAME OVER")

        if event.type == pygame.MOUSEBUTTONUP and clicked_tile:
            clicked_tile.turn_off()
            if proceed_next_level:
                player_turn = False
                generate_new_tile = True
                proceed_next_level = False
                next_level_time = pygame.time.get_ticks()


    if not player_turn:
        if next_level_time != 0:
            next_level_time_elapsed = (pygame.time.get_ticks() - next_level_time) / 1000

        if next_level_time_elapsed >= 1:
            if generate_new_tile:
                generate_new_tile = False
                print("Generating new Tile")
                gen.generate_next_tile()
                print([i + 1 for i in gen.sequence])
                continue_sequence = True
                start_sequence_time = pygame.time.get_ticks()

            if continue_sequence:
                continue_sequence = False
                current_tile = tiles[gen.iter_next()]
                print("Turning on Tile: " + str(current_tile.num))
                current_tile.turn_on()
                sequence_time = pygame.time.get_ticks()
                print("Continuing Sequence")

            if sequence_time != 0:
                sequence_time_elapsed = (pygame.time.get_ticks() - sequence_time) / 1000

            if sequence_time_elapsed >= 0.7:
                current_tile.turn_off()
                if gen.iterator + 1 < len(gen.sequence):
                    continue_sequence = True
                else:
                    print("START NOW")
                    continue_sequence = False
                    player_turn = True

    pygame.display.update()

pygame.quit()