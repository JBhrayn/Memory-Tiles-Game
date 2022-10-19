import random
import pygame

TILE_SIZE = 153
BORDER_SIZE = 40
ROWS, COLUMNS = 3, 3
WIDTH, HEIGHT = 610, 750
TOP_PANEL_HEIGHT = 100
pygame.display.set_caption("Simple Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Tile:
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

    def intersects(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class SequenceGenerator:

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
        if self.iterator + 1 >= len(self.sequence):
            self.iterator = -1

        self.iterator += 1
        return self.sequence[self.iterator]


tile_num = 1
tiles = []
tile_y = BORDER_SIZE * 2 + TOP_PANEL_HEIGHT
for r in range(ROWS):
    tile_x = BORDER_SIZE
    for c in range(COLUMNS):
        tiles.append(Tile(tile_num, tile_x, tile_y))
        tile_x += 190
        tile_num += 1
    tile_y += 190

pygame.init()
pygame.font.init()
medium_font = pygame.font.SysFont('bahnschrift', 30)
large_font = pygame.font.SysFont('bahnschrift', 80)

title_text_1 = large_font.render('Sequence', True, (89, 108, 104))
title_text_2 = large_font.render('Memory Game', True, (89, 108, 104))
title_text_rect_1 = title_text_1.get_rect(center=(WIDTH / 2, 50))
title_text_rect_2 = title_text_2.get_rect(center=(WIDTH / 2, 50 + 80))
start_text = medium_font.render('START', True, (255, 255, 255))
start_text_rect = start_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 70))
score_label_text = medium_font.render('SCORE', True, (133, 101, 75))
score_label_text_rect = start_text.get_rect(center=(WIDTH / 2, 20))
score_text = large_font.render('0', True, (89, 108, 104))
score_text_rect = score_text.get_rect(center=(WIDTH / 2, 80))
back_text = medium_font.render(' BACK', True, (255, 255, 255))
back_text_rect = start_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 70))


def display_menu():
    screen.fill((227, 217, 202))
    for t in tiles:
        if t.num == 5:
            t.turn_off()
        else:
            t.turn_on()
        t.draw()
        screen.blit(title_text_1, title_text_rect_1)
        screen.blit(title_text_2, title_text_rect_2)
        screen.blit(start_text, start_text_rect)


def display_start_game():
    global score_text

    screen.fill((227, 217, 202))
    screen.blit(score_label_text, score_label_text_rect)
    score_text = large_font.render(str(level), True, (89, 108, 104))
    screen.blit(score_text, score_text_rect)
    for t in tiles:
        t.draw()


def display_game_over():
    global score_text

    screen.fill((227, 217, 202))
    game_over_text = large_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 300)))
    screen.blit(score_label_text, score_label_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 180)))
    score_text = large_font.render(str(level), True, (89, 108, 104))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 130)))

    for t in tiles:
        if t.num == 5:
            t.draw()

    screen.blit(back_text, back_text_rect)


def get_tile():
    mousePos = pygame.mouse.get_pos()
    return next((t for t in tiles if t.intersects(mousePos)), None)


def mouse_hovered():
    mousePos = pygame.mouse.get_pos()
    if any(t for t in tiles if t.intersects(mousePos)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def reset_all_data():
    global level, click_count, correct_count, sequence_time, next_level_time, sequence_time_elapsed
    global menu, start, game_over, player_turn, generate_new_tile, continue_sequence, proceed_next_level
    global next_level_time_elapsed, current_tile, clicked_tile, gen
    level = click_count = correct_count = sequence_time = 0
    next_level_time = sequence_time_elapsed = next_level_time_elapsed = 0
    menu = generate_new_tile = True
    start = game_over = player_turn = continue_sequence = proceed_next_level = False
    current_tile = clicked_tile = None
    gen = SequenceGenerator()


level = 0
click_count = 0
correct_count = 0
sequence_time = 0
next_level_time = 0
sequence_time_elapsed = 0
next_level_time_elapsed = 0

run = True
menu = True
start = False
game_over = False
player_turn = False
generate_new_tile = True
continue_sequence = False
proceed_next_level = False

current_tile = None
clicked_tile = None

gen = SequenceGenerator()

while run:
    if menu:
        display_menu()
    if start:
        display_start_game()
    if game_over:
        display_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION:
            mouse_hovered()

        if event.type == pygame.MOUSEBUTTONDOWN and menu:
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

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                clicked_tile = get_tile()
                if clicked_tile:
                    if gen.iter_next() + 1 == clicked_tile.num:
                        clicked_tile.turn_on()
                        if click_count + 1 < len(gen.sequence):
                            click_count += 1
                        else:
                            proceed_next_level = True
                    else:
                        game_over = True
                        clicked_tile = None

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
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_tile = get_tile()
                if clicked_tile and clicked_tile.num == 5:
                    clicked_tile.turn_on()

            if event.type == pygame.MOUSEBUTTONUP and clicked_tile:
                if clicked_tile.num == 5:
                    clicked_tile.turn_off()
                    reset_all_data()

    if not player_turn:
        if next_level_time != 0:
            next_level_time_elapsed = (pygame.time.get_ticks() - next_level_time) / 1000

        if next_level_time_elapsed >= 1:
            if generate_new_tile:
                generate_new_tile = False
                gen.generate_next_tile()
                continue_sequence = True
                start_sequence_time = pygame.time.get_ticks()

            if continue_sequence:
                continue_sequence = False
                current_tile = tiles[gen.iter_next()]
                current_tile.turn_on()
                sequence_time = pygame.time.get_ticks()

            if sequence_time != 0:
                sequence_time_elapsed = (pygame.time.get_ticks() - sequence_time) / 1000

            if sequence_time_elapsed >= 0.7:
                current_tile.turn_off()
                if gen.iterator + 1 < len(gen.sequence):
                    continue_sequence = True
                else:
                    continue_sequence = False
                    player_turn = True

    pygame.display.update()

pygame.quit()
