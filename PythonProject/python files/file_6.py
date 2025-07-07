import pygame
import random
import math
import importlib
from Classes import Block, Triangle, Door, Coin, PauseMenu

pygame.init()

screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("6 LVL")
icon = pygame.image.load("../pictures/КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.mixer.init()
pygame.mixer.music.stop()
sound_death = pygame.mixer.Sound("../music/geometry-dash-death-sound-effect.mp3")
sound = pygame.mixer.Sound("../music/Forever Bound - Stereo Madness (Geometry Dash).mp3")
sound.play().set_volume(0.3)

napr=1
jump_force = -15
gravity = 0.9

maxJumpCount = 2
jumpCounter = maxJumpCount

def getZnak(num):
    if (num > 0):
        return 1
    elif num < 0:
        return -1
    return 0

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
            rect.x -= scroll_x + i - 15
            if (i > 15):
                rect.x += i - 15
                rect.width -= i - 15
            rect.y += i - 15
            rect.height += 15 - i
            if (i < 15):
                rect.height -= (15 - i)
            shade = max(0, 200 - i * 5)
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
        sound.stop()
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

                    sound.play().set_volume(0.3)

def init_level():
    global blocks, triangles

    blocks = [
        Block(-1000, 500, 10000, 300),
        Block(-1000, -50, 10000, 50),
        Block(-1000, -50, 900, 4800),
        Block(-1000, 350, 1620, 400),
        Block(1560, 400, 50, 400),
        Block(1760, 300, 50, 400),
        Block(1960, 200, 50, 400),
        Block(2900, 450, 200, 400),
        Block(3300, 450, 400, 400),
        Block(3900, 400, 400, 400),
        Block(4500, 370, 100, 50),
        Block(4700, 340, 100, 50),
        Block(4900, 310, 100, 50),
        Block(5100, 280, 100, 50),
        Block(5300, 370, 100, 50),
        Block(5500, 340, 100, 50),
        Block(5700, 310, 100, 50),
        Block(5900, 280, 100, 50),
        Block(8400, -100, 1000, 1000),
        Block(5900, 50, 100, 50),
        Block(5700, 80, 100, 50),
        Block(5500, 110, 100, 50),
        Block(5300, 140, 100, 50),
        Block(5100, 50, 100, 50),
        Block(4900, 80, 100, 50),
        Block(4700, 110, 100, 50),
        Block(4500, 140, 100, 50),
        Block(-1000, -50, 1620, 200),
        Block(1560, -50, 50, 300),
        Block(1760, -50, 50, 200),
        Block(1960, -50, 500, 100),
        Block(2900, -50, 200, 200),
        Block(3300, -50, 400, 200),
        Block(3900, -50, 400, 200),
        Block(600, -50, 710, 200),
    ]

    triangles = [
    Triangle(blocks[3], offset_x=1600, offset_y=-25, size=40),
    Triangle(blocks[3], offset_x=1100, offset_y=-45, size=90),
    Triangle(blocks[0], offset_x=2060, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2100, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2540, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2640, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2690, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2740, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2840, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2890, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=2940, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=3830, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=3880, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4130, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4180, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4230, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4280, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4730, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4780, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4830, offset_y=-25, size=40),
    Triangle(blocks[0], offset_x=4880, offset_y=-25, size=40),
    Triangle(blocks[8], offset_x=200, offset_y=-25, size=40),
    Triangle(blocks[17], offset_x=85, offset_y=-15, size=20),
    Triangle(blocks[22], offset_x=10, offset_y=60, size=20,isInvert=True),
    Triangle(blocks[26], offset_x=10, offset_y=60, size=20, isInvert=True),
    Triangle(blocks[1], offset_x=2340, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2460, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2420, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2380, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2500, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2540, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2640, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2690, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2740, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2840, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2890, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=2940, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=3830, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=3880, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4130, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4180, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4230, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4280, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4730, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4780, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4830, offset_y=70, size=40, isInvert=True),
    Triangle(blocks[1], offset_x=4880, offset_y=70, size=40, isInvert=True),

    ]

    for i in range(7):
        triangles.append(Triangle(blocks[0], offset_x=3040 + i * 45, offset_y=-25, size=40))
    for i in range(40):
        triangles.append(Triangle(blocks[0], offset_x=5330 + i * 45, offset_y=-25, size=40))
    for i in range(5):
        triangles.append(Triangle(blocks[0], offset_x=7640 + i * 45, offset_y=-25, size=40))
    for i in range(5):
        triangles.append(Triangle(blocks[0], offset_x=8040 + i * 45, offset_y=-25, size=40))
    for i in range(5):
        triangles.append(Triangle(blocks[0], offset_x=8440 + i * 45, offset_y=-25, size=40))
    for i in range(5):
        triangles.append(Triangle(blocks[1], offset_x=7640 + i * 45, offset_y=70, size=40,isInvert=True))
    for i in range(5):
        triangles.append(Triangle(blocks[1], offset_x=8040 + i * 45, offset_y=70, size=40,isInvert=True))
    for i in range(5):
        triangles.append(Triangle(blocks[1], offset_x=8440 + i * 45, offset_y=70, size=40,isInvert=True))
    for i in range(70):
        triangles.append(Triangle(blocks[0], offset_x=9040 + i * 45, offset_y=-25, size=40))
    for i in range(70):
        triangles.append(Triangle(blocks[1], offset_x=9040 + i * 45, offset_y=70, size=40,isInvert=True))
    for i in range(40):
        triangles.append(Triangle(blocks[1], offset_x=5330 + i * 45, offset_y=70, size=40,isInvert=True))

def init_coins():
    global coins
    coins = [
        Coin(8000, 300, gravity=True),
        Coin(40, 160, gravity=True),
    ]

player = pygame.Rect(screen_w//2 - 20 - 200, screen_h//2 - 20 , 60, 60)
player_color = (255, 0, 0)
vertical_momentum = 0
on_ground = False

scroll_x = 0
scroll_y = 0

deadzone_width = 20

deadzone_left = screen_w // 2 - deadzone_width // 2
deadzone_right = screen_w // 2 + deadzone_width // 2

camera_smooth_speed = 0.1

door = Door(-100, 350, width=60, height=100, coins_required=0)

# Счетчик собранных монет
coins_collected = 0
font_coin = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 40)

def draw_coin_counter(screen):
    text = font_coin.render(f"Coins: {coins_collected}", True, (255, 170, 0))
    screen.blit(text, (10, 10))

def reset_game():
    global player, vertical_momentum, on_ground, scroll_x, scroll_y, coins_collected,napr, gravity
    player.x = screen_w//2 - 20 - 200
    player.y = screen_h//2 - 20
    vertical_momentum = 0
    on_ground = False
    scroll_x = 0
    scroll_y = 0
    coins_collected = 0
    gravity = 0.9
    napr=1
    init_level()
    init_coins()


def collisions(dx):
    global vertical_momentum, on_ground, jumpCounter

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
            if vertical_momentum * getZnak(gravity) > 0:
                if getZnak(gravity) > 0:
                    player.bottom = block.rect.top
                else:
                    player.top = block.rect.bottom
                vertical_momentum = 0
                jumpCounter = maxJumpCount
                on_ground = True
            elif vertical_momentum * getZnak(gravity) < 0:
                if getZnak(gravity) > 0:
                    player.top = block.rect.bottom
                else:
                    player.bottom = block.rect.top
                vertical_momentum = 0

    for triangle in triangles:
        triangle.update()
        if player.colliderect(triangle.hitbox):
            death()
            return

clock = pygame.time.Clock()
running = True
f = True

reset_game()

paused = False
current_volume = 1.0 
pause_menu = PauseMenu(screen, current_volume)

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pygame.mixer.pause()
                else:
                    pygame.mixer.unpause()
        
        if paused:
            result = pause_menu.handle_event(event)
            
            if result == "volume_changed":
                sound.set_volume(pause_menu.volume * 0.3)
                sound_death.set_volume(pause_menu.volume * 0.3)
            
            elif result == "resume":
                paused = False
                pygame.mixer.unpause()

    if not paused:
        keys = pygame.key.get_pressed()
        if napr:
            dx = 0
            dx = player_speed
        else:
            dx = -player_speed
        if scroll_x>7500:
            napr=0

        if keys[pygame.K_SPACE] and jumpCounter > 0 and f:
            vertical_momentum = jump_force * getZnak(gravity)
            on_ground = False
            jumpCounter -= 1
            f = False

        if not keys[pygame.K_SPACE]:
            f = True

        collisions(dx)

        for coin in coins:
            coin.update()
            if not coin.collected and coin.collide(player):
                coin.collected = True
                if coin.gravity:
                    gravity *= -1
                else:
                    coins_collected += 1

        player_screen_x = player.x - scroll_x
        player_screen_y = player.y - scroll_y
        target_scroll_x = scroll_x
        target_scroll_y = scroll_y

        if player_screen_x < deadzone_left:
            target_scroll_x -= (deadzone_left - player_screen_x)
        elif player_screen_x > deadzone_right:
            target_scroll_x += (player_screen_x - deadzone_right)

        scroll_x += (target_scroll_x - scroll_x) * camera_smooth_speed
        scroll_y += (target_scroll_y - scroll_y) * camera_smooth_speed

    screen.fill((25,0,25))
    background()

    for block in blocks:
        block.draw(screen, int(scroll_x), int(scroll_y))

    ground3d(int(scroll_x))

    for triangle in triangles:
        triangle.draw(screen, int(scroll_x), int(scroll_y))

    for coin in coins:
        if not coin.collected:
            coin.draw(screen, int(scroll_x), int(scroll_y))

    door.draw(screen, coins_collected, scroll_x, scroll_y)

    if not paused and door.collide(player):
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
    
    if paused:
        pause_menu.draw()
    
    if current_level:
        sound.stop()
        module = importlib.import_module(current_level)
        module.main()

    if not paused and player.y > 900 or player.y < -300:
        death()

    pygame.display.flip()
    current_level = None

pygame.quit()