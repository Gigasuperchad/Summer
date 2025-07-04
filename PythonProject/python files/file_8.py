import pygame
import random
import math
import importlib
from Classes import Block, Triangle, Door, Coin

pygame.init()

screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("LVL 8")
icon = pygame.image.load("../pictures/КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.mixer.init()
pygame.mixer.music.stop()
sound_death = pygame.mixer.Sound("../music/d19c2f47f78098a.mp3")
sound = pygame.mixer.Sound("../music/aphex-twin-xtal.mp3")
sound.play().set_volume(0.3)

a = [random.randint(-1000, 1000) for _ in range(2000)]
a_1 = [random.randint(-500, 500) for _ in range(200)]
a_2 = [random.randint(-500, 500) for _ in range(200)]

b = [random.randint(11, 20) for _ in range(2000)]
c = [random.randint(0, 400) for _ in range(2000)]
d = [random.randint(20, 100) for _ in range(200)]

color_BG = [random.randint(0,255) for _ in range(2000)]

jump_force = -17
gravity = 0.9

def getZnak(num):
    if (num > 0):
        return 1
    elif num < 0:
        return -1
    return 0

player_speed = 5

current_level = None


def background(scroll_x, scroll_y):
    for i in range(30):
        points1 = [(a[i] - scroll_x // b[i], 600 - c[i] - scroll_y // b[i]),
                   (a_1[i] - scroll_x // b[i], 800),
                   (a_2[i] - scroll_x // b[i], 800)]
        points2 = [(500 - a[i] - scroll_x // b[i], 600 - c[i] - scroll_y // b[i]),
                   (500 - a_1[i] - scroll_x // b[i], 800),
                   (500 - a_2[i] - scroll_x // b[i], 800)]
        points3 = [(1000 + a[i] - scroll_x // b[i], 600 - c[i] - scroll_y // b[i]),
                   (1000 + a_1[i] - scroll_x // b[i], 800),
                   (1000 + a_2[i] - scroll_x // b[i], 800)]
        pygame.draw.polygon(screen, (0, 0, 0), points1, 1)
        pygame.draw.polygon(screen, (0, 0, 0), points2, 1)
        pygame.draw.polygon(screen, (0, 0, 0), points3, 1)

def ground3d(scroll_x):
    for i in range(0,30,3):
        for block in blocks:
            rect = block.rect.copy()
            rect.x -= scroll_x
            rect.y += i - 15
            rect.height += 15 - i
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
        Block(0, 400, 800, 500),  # 0
        Block(800, 300, 200, 3000),  # 1
        Block(1000, 200, 150, 3000),  # 2
        Block(1200, 300, 250, 3000),  # 3
        Block(1600, 450, 500, 3000),  # 4
        Block(2100, 500, 300, 3000),  # 5
        Block(2400, 400, 200, 3000),  # 6
        Block(2700, 400, 1000, 3000),  # 7
        Block(3000, 325, 1000, 3000),  # 8
    ]

    triangles = [
        Triangle(blocks[0], offset_x=745, offset_y=-25, size=45),
        Triangle(blocks[1], offset_x=145, offset_y=-25, size=45),
        Triangle(blocks[2], offset_x=110, offset_y=-25, size=45),
        Triangle(blocks[5], offset_x=10, offset_y=-25, size=45),
        Triangle(blocks[5], offset_x=200, offset_y=-25, size=45),
        Triangle(blocks[7], offset_x=250, offset_y=-25, size=45),
        Triangle(blocks[7], offset_x=205, offset_y=-25, size=45),
        Triangle(blocks[8], offset_x=215, offset_y=-10, size=15),
        Triangle(blocks[8], offset_x=230, offset_y=-15, size=25),
        Triangle(blocks[8], offset_x=255, offset_y=-15, size=25),
        Triangle(blocks[8], offset_x=270, offset_y=-10, size=15),
        Triangle(blocks[8], offset_x=390, offset_y=-10, size=15),
        Triangle(blocks[8], offset_x=405, offset_y=-15, size=25),
        Triangle(blocks[8], offset_x=430, offset_y=-15, size=25),
        Triangle(blocks[8], offset_x=445, offset_y=-10, size=15),
        Triangle(blocks[8], offset_x=565, offset_y=-10, size=15),
        Triangle(blocks[8], offset_x=580, offset_y=-15, size=25),
        Triangle(blocks[8], offset_x=605, offset_y=-15, size=25),
        Triangle(blocks[8], offset_x=620, offset_y=-10, size=15),
    ]

def init_coins():
    global coins
    coins = [
        Coin(-140, 220),
        Coin(840, 200),
        Coin(1640, 300),

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

door = Door(17830, 300, width=60, height=100, coins_required=18)

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

    screen.fill((255,255,255))

    background(int(scroll_x), int(scroll_y))

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
            current_level="file_8"

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
