import sys

import pygame
import random
import math
import importlib
from Classes import Block, Triangle, Door, Coin, Sphere

pygame.init()

screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("7 LVL")
icon = pygame.image.load("../pictures/КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.mixer.init()
pygame.mixer.music.stop()
sound_death = pygame.mixer.Sound("../music/d19c2f47f78098a.mp3")
sound = pygame.mixer.Sound("../music/aphex-twin-xtal.mp3")
sound.play().set_volume(0.3)


a = [random.randint(-1000, 1000) for _ in range(5000)]
c = [random.randint(0, 400) for _ in range(5000)]
color_BG = [random.randint(0,255) for _ in range(5000)]

def background(scroll_x, scroll_y):
    for i in range(5000):
        pygame.draw.circle(screen, (color_BG[i],color_BG[i],color_BG[i]), (a[i]-scroll_x//100, c[i]*2), 1)
    for p in range(0,900,3):    
        pygame.draw.line(screen, (0,0,0), (p, 0), (p, 700), 1)
        pygame.draw.line(screen, (0,0,0), (0, p ), (900, p), 1)

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

sphere = Sphere()

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
        Block(0, 400, 800, 500),
        Block(800, 300, 200, 3000),
        Block(1000, 200, 150, 3000),
        Block(1200, 300, 250, 3000),
        Block(1600, 450, 500, 3000),
        Block(2100, 500, 500, 300),
        Block(2500, 350, 200, 3000),
        Block(2750, 350, 200, 3000),
        Block(2850, 350, 200, 3000),
        Block(3100, 300, 180, 3000),
        Block(3330, 250, 150, 3000),
        Block(3530, 200, 120, 3000),
        Block(3700, 250, 200, 50),
        Block(3950, 300, 250, 3000),
        Block(4250, 350, 300, 3000),
        Block(4600, 400, 400, 3000),
        Block(5050, 350, 100, 20),
        Block(5200, 300, 200, 3000),
        Block(5450, 250, 250, 3000),
        Block(5750, 300, 180, 3000),
        Block(5980, 350, 150, 3000),
        Block(6180, 400, 200, 3000),
        Block(6430, 450, 250, 3000),
        Block(6730, 500, 300, 300),
        Block(7080, 450, 150, 3000),
        Block(7280, 400, 200, 3000),
        Block(7530, 350, 180, 3000),
        Block(7760, 300, 120, 3000),
        Block(7880, 450, 1000, 3000),
        Block(8880, 350, 180, 3000),
        Block(9060, 350, 220, 3000),
        Block(9280, 300, 1000, 3000),
        Block(10280, 500, 150, 3000),
        Block(10430, 350, 300, 3000),
        Block(10730, 350, 1000, 3000),
        Block(11730, 400, 180, 3000),
        Block(11910, 300, 220, 3000),
        Block(12130, 450, 1000, 3000),
        Block(13130, 400, 150, 3000),
        Block(13280, 350, 300, 3000),
        Block(13580, 500, 1000, 3000),
        Block(14580, 450, 180, 3000),
        Block(14760, 300, 220, 3000),
        Block(14980, 450, 1000, 3000),
        Block(15980, 350, 150, 3000),
        Block(16130, 300, 300, 3000),
        Block(16430, 500, 1000, 3000),
        Block(17430, 400, 180, 3000),
        Block(17610, 350, 220, 3000),
        Block(17830, 300, 1000, 3000)
    ]

    triangles = [
        Triangle(blocks[0], offset_x=745, offset_y=-25, size=45),
        Triangle(blocks[1], offset_x=145, offset_y=-25, size=45),
        Triangle(blocks[2], offset_x=110, offset_y=-25, size=45),
        Triangle(blocks[5], offset_x=200, offset_y=-25, size=45),
        Triangle(blocks[3], offset_x=100, offset_y=-25, size=45),
        Triangle(blocks[7], offset_x=200, offset_y=-25, size=45),
        Triangle(blocks[10], offset_x=50, offset_y=-25, size=45),
        Triangle(blocks[15], offset_x=200, offset_y=-25, size=45),
        Triangle(blocks[20], offset_x=80, offset_y=-25, size=45),
        Triangle(blocks[25], offset_x=150, offset_y=-25, size=45),
        Triangle(blocks[28], offset_x=400, offset_y=-25, size=45),
        Triangle(blocks[28], offset_x=800, offset_y=-25, size=45),
        Triangle(blocks[31], offset_x=300, offset_y=-25, size=45),
        Triangle(blocks[33], offset_x=200, offset_y=-25, size=45),
        Triangle(blocks[34], offset_x=400, offset_y=-25, size=45),
        Triangle(blocks[39], offset_x=100, offset_y=-25, size=45)
]
def init_coins():
    global coins
    coins = [
        Coin(-140, 220),
        Coin(840, 200),
        Coin(1640, 300),
        Coin(2100, 300),
        Coin(2750, 300),
        Coin(3100, 230),
        Coin(3700, 180),
        Coin(4250, 280),
        Coin(5050, 310),
        Coin(6430, 400),
        Coin(7280, 350),
        Coin(9060, 300),
        Coin(10430, 280),
        Coin(11730, 330),
        Coin(13280, 310),
        Coin(14980, 310),
        Coin(16430, 460),
        Coin(17830, 260),
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

door = Door(17900, 300, width=60, height=100, coins_required=18)

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

    screen.fill((0,0,0))
    background(scroll_x, scroll_y)
    sphere.update()
    sphere.draw(screen)
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
            current_level="1"

    player_draw_rect = player.copy()
    player_draw_rect.x -= int(scroll_x)
    player_draw_rect.y -= int(scroll_y)
    pygame.draw.rect(screen, player_color, player_draw_rect)

    draw_coin_counter(screen)
    if current_level:
        sound.stop()
        sys.exit()

    if player.y > 900:
        death()

    pygame.display.flip()
    current_level = None

pygame.quit()
