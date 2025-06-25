import pygame
import random
import math
import importlib
from Classes import Block, Triangle, Door, Coin

pygame.init()

screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("6 LVL")
icon = pygame.image.load("../pictures/КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.mixer.init()
pygame.mixer.music.stop()
sound_death = pygame.mixer.Sound("../music/d19c2f47f78098a.mp3")
sound = pygame.mixer.Sound("../music/M.O.O.N. - Crystals.mp3")
sound.play().set_volume(0.3)

# Генерация случайных данных для фона (оставил как у вас)
a = [random.randint(-1000, 1000) for _ in range(2000)]
a_1 = [random.randint(-500, 500) for _ in range(200)]
a_2 = [random.randint(-500, 500) for _ in range(200)]

b = [random.randint(11, 20) for _ in range(2000)]
c = [random.randint(0, 400) for _ in range(2000)]
d = [random.randint(20, 100) for _ in range(200)]

color_BG = [random.randint(0,255) for _ in range(2000)]

jump_force = -17
gravity = 0.9

player_speed = 5

current_level = None

def background():
    for i in range(5):
        points = [
            (random.randint(-10,800), random.randint(0, 600)),  # Точка 1
            (random.randint(-10,800), random.randint(0, 600)),  # Точка 2
            (random.randint(-10,800), random.randint(0, 600))   # Точка 3
        ]
        color = (random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
        pygame.draw.polygon(screen, color, points, 2)
    for j in range(5):
        pygame.draw.rect(screen, color, (random.randint(-10,800),random.randint(0, 600), random.randint(0, 300), random.randint(0, 300)))
    for p in range(0,900,3):
        pygame.draw.line(screen, (0,0,0), (p, 0), (p, 700), 1)
        pygame.draw.line(screen, (0,0,0), (0, p ), (900, p), 1)

def ground3d(scroll_x):
    for i in range(0,30,3):
        for block in blocks:
            rect = block.rect.copy()
            rect.x -= scroll_x
            rect.y += i - 15
            rect.height += 20
            shade = max(0, 200 - i*5)
            pygame.draw.rect(screen, (shade, shade, shade), rect)

def death():
    global running, vertical_momentum, on_ground

    death_screen = pygame.Surface((screen_w, screen_h))
    death_screen.fill((0,0,0))
    font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 100)
    text_surface = font.render("You Died", True, (255,255,255))
    text_rect = text_surface.get_rect(center=(screen_w//2, screen_h//2))

    font_small = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 40)
    hint_surface = font_small.render("Press R to restart or ESC to exit", True, (200,200,200))
    hint_rect = hint_surface.get_rect(center=(screen_w//2, screen_h//2 + 100))

    death_screen.blit(text_surface, text_rect)
    death_screen.blit(hint_surface, hint_rect)

    sound_death.play()
    sound_death.set_volume(0.3)

    dead = True
    while dead:
        screen.blit(death_screen, (0,0))
        for p in range(0, 900, 2):
            pygame.draw.line(screen, (0,0,0), (p, 0), (p, 700), 1)
            pygame.draw.line(screen, (0,0,0), (0, p), (900, p), 1)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_r:
                    reset_game()
                    dead = False

def init_level():
    global blocks, triangles

    blocks = [
        Block(-100, 400, 1200, 200),
        Block(-250, -100, 400, 800),
        Block(1100, -100, 1300, 800),

    ]

    triangles = [
        Triangle(blocks[0], offset_x=1117, offset_y=-45, size=10),
    ]

def init_coins():
    global coins
    coins = [
        Coin(300, 340),
        Coin(400, 340),
        Coin(500, 340),
        Coin(600, 340),
        Coin(700, 340),
        Coin(800, 340),
        Coin(300, 300),
        Coin(400, 300),
        Coin(500, 300),
        Coin(600, 300),
        Coin(700, 300),
        Coin(800, 300),
        Coin(300, 260),
        Coin(400, 260),
        Coin(500, 260),
        Coin(600, 260),
        Coin(700, 260),
        Coin(800, 260),
        Coin(300, 220),
        Coin(400, 220),
        Coin(500, 220),
        Coin(600, 220),
        Coin(700, 220),
        Coin(800, 220),
        Coin(1000, 220),
        Coin(1000, 340),


    ]

player = pygame.Rect(screen_w//2 - 20 - 200, screen_h//2 - 20 , 60, 60)
player_color = (255, 0, 0)
vertical_momentum = 0
on_ground = False

scroll_x = 0
scroll_y = 0

# Параметры "невидимой рамки" (deadzone)
deadzone_width = 20

deadzone_left = screen_w // 2 - deadzone_width // 2
deadzone_right = screen_w // 2 + deadzone_width // 2

# Скорость сглаживания камеры (чем меньше — тем плавнее)
camera_smooth_speed = 0.1

door = Door(900, 400, width=60, height=100, coins_required=25)

# Счетчик собранных монет
coins_collected = 0
font_coin = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 40)

def draw_coin_counter(screen):
    text = font_coin.render(f"Coins: {coins_collected}", True, (255, 170, 0))
    screen.blit(text, (10, 10))

def reset_game():
    global player, vertical_momentum, on_ground, scroll_x, scroll_y, coins_collected
    player.x = screen_w//2 - 20 - 200
    player.y = screen_h//2 - 20
    vertical_momentum = 0
    on_ground = False
    scroll_x = 0
    scroll_y = 0
    coins_collected = 0
    init_level()
    init_coins()

def collisions(dx):
    global vertical_momentum, on_ground

    player.x += dx
    for block in blocks:
        if player.colliderect(block.rect):
            if dx > 0:
                player.right = block.rect.left
            elif dx < 0:
                player.left = block.rect.right

    global gravity
    vertical_momentum += gravity
    player.y += vertical_momentum

    on_ground = False
    for block in blocks:
        if player.colliderect(block.rect):
            if vertical_momentum > 0:
                player.bottom = block.rect.top
                vertical_momentum = 0
                on_ground = True
            elif vertical_momentum < 0:
                player.top = block.rect.bottom
                vertical_momentum = 0

    for triangle in triangles:
        triangle.update()
        if player.colliderect(triangle.hitbox):
            death()
            return

clock = pygame.time.Clock()
running = True

reset_game()

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dx = 0
    if keys[pygame.K_a]:
        dx = -player_speed
    if keys[pygame.K_d]:
        dx = player_speed

    if keys[pygame.K_SPACE] and on_ground:
        vertical_momentum = jump_force
        on_ground = False

    collisions(dx)

    # Проверка столкновения с монетами
    for coin in coins:
        coin.update()
        if not coin.collected and coin.collide(player):
            coin.collected = True
            coins_collected += 1

    # Позиция игрока на экране с учётом сдвига камеры
    player_screen_x = player.x - scroll_x
    player_screen_y = player.y - scroll_y

    target_scroll_x = scroll_x
    target_scroll_y = scroll_y

    # Горизонтальная камера с deadzone
    if player_screen_x < deadzone_left:
        target_scroll_x -= (deadzone_left - player_screen_x)
    elif player_screen_x > deadzone_right:
        target_scroll_x += (player_screen_x - deadzone_right)

    # Плавно приближаемся к целевой позиции камеры
    scroll_x += (target_scroll_x - scroll_x) * camera_smooth_speed
    scroll_y += (target_scroll_y - scroll_y) * camera_smooth_speed

    screen.fill((25,0,25))

    background()

    for block in blocks:
        block.draw(screen, int(scroll_x), int(scroll_y))

    ground3d(int(scroll_x))

    for triangle in triangles:
        triangle.draw(screen, int(scroll_x), int(scroll_y))

    # Рисуем монеты, которые не собраны
    for coin in coins:
        if not coin.collected:
            coin.draw(screen, int(scroll_x), int(scroll_y))

    # Рисуем дверь
    door.draw(screen, coins_collected, scroll_x, scroll_y)

    # Подсказка при соприкосновении с дверью
    if door.collide(player):
        font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 30)
        if door.is_open(coins_collected):
            msg = font.render("Дверь открыта! Нажмите E для перехода", True, (255, 0, 150))
        else:
            coins_needed = door.coins_required - coins_collected
            msg = font.render(f"Нужно собрать ещё {coins_needed} монет для перехода", True, (255, 0, 150))
        screen.blit(msg, (screen_w // 2 - msg.get_width() // 2, 50))

        keys = pygame.key.get_pressed()
        if door.is_open(coins_collected) and keys[pygame.K_e]:
            current_level="file_7"

    player_draw_rect = player.copy()
    player_draw_rect.x -= int(scroll_x)
    player_draw_rect.y -= int(scroll_y)
    pygame.draw.rect(screen, player_color, player_draw_rect)

    draw_coin_counter(screen)
    if current_level:
        sound.stop()
        module = importlib.import_module(current_level)
        module.main()

    if player.y > 900:
        death()

    pygame.display.flip()
    current_level = None

pygame.quit()
