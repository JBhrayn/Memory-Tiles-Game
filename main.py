import random
import time

import pygame

TILE_SIZE = 153
BORDER_SIZE = 40
ROWS, COLUMNS = 3, 3
WIDTH, HEIGHT = 610, 750
TOP_PANEL_HEIGHT = 100

pygame.display.set_caption("Simple Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Tile():
    unclicked_tile_img = pygame.image.load('UNCLICKED_TILE.png').convert_alpha()
    unclicked_tile_img = pygame.transform.scale(unclicked_tile_img, (TILE_SIZE, 165))
    clicked_tile_img = pygame.image.load('CLICKED_TILE.png').convert_alpha()
    clicked_tile_img = pygame.transform.scale(clicked_tile_img, (TILE_SIZE, TILE_SIZE))

    def __init__(self, num, x, y):
        self.y = y
        self.num = num
        self.image = Tile.unclicked_tile_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def turn_on(self):
        self.y = 12
        self.image = Tile.clicked_tile_img

    def turn_off(self):
        self.y = 0
        self.image = Tile.unclicked_tile_img

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y + self.y))

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

def get_tile():
    mousePos = pygame.mouse.get_pos()
    return next((t for t in tiles if t.intersects(mousePos)), None)

def mouse_hovered():
    mousePos = pygame.mouse.get_pos()
    if any(t for t in tiles if t.intersects(mousePos)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

pygame.init()
pygame.font.init()
medium_font = pygame.font.SysFont('bahnschrift', 30)
large_font = pygame.font.SysFont('bahnschrift', 80)

start_text = medium_font.render('START', True, (255, 255, 255))
start_text_rect = start_text.get_rect(center=(WIDTH/2, HEIGHT/2+70))

score_label_text = medium_font.render('SCORE', True, (133, 101, 75))
score_label_text_rect = start_text.get_rect(center=(WIDTH/2, 20))

score_text = large_font.render('0', True, (89, 108, 104))
score_text_rect = score_text.get_rect(center=(WIDTH/2, 80))

level = 0

click_count = 0
correct_count = 0

sequence_time = 0
sequence_time_elapsed = 0

next_level_time = 0
next_level_time_elapsed = 0

current_tile = None
clicked_tile = None
gen = SequenceGenerator()

player_turn = False
generate_new_tile = True
continue_sequence = False
proceed_next_level = False

start = False
menu = True
screen.fill((227, 217, 202))
for tile in tiles:
    if tile.num == 5:
        tile.turn_off()
    else:
        tile.turn_on()
    tile.draw()
    screen.blit(start_text, start_text_rect)

run = True
while run:
    if start:
        screen.fill((227, 217, 202))
        screen.blit(score_label_text, score_label_text_rect)
        score_text = large_font.render(str(level), True, (89, 108, 104))
        screen.blit(score_text, score_text_rect)
        for tile in tiles:
            tile.draw()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION:
            mouse_hovered()

        if event.type == pygame.MOUSEBUTTONDOWN and not start:
            clicked_tile = get_tile()

            if clicked_tile and clicked_tile.num == 5:
                for tile in tiles:
                    if tile.num == 5:
                        tile.turn_on()
                    else:
                        tile.turn_off()
                next_level_time = pygame.time.get_ticks()
                start = True
                menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            print("MOUSEBUTTONDOWN")
            clicked_tile = get_tile()

            if clicked_tile:
                if gen.iter_next()+1 == clicked_tile.num:
                    print("CORRECT")
                    clicked_tile.turn_on()

                    if click_count + 1 < len(gen.sequence):
                        click_count += 1
                    else:
                        proceed_next_level = True
                        print("PROCEED NEXT LEVEL")
                else:
                    print("GAME OVER")
                    run = False

        if event.type == pygame.MOUSEBUTTONUP and clicked_tile:
            clicked_tile.turn_off()
            if proceed_next_level:
                level += 1
                click_count = 0
                correct_count += 1
                gen.iterator = -1
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