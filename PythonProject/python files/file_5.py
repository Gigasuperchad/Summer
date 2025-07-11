import pygame
import random
import importlib
from Classes import Block, Triangle, Door, Coin, PauseMenu, Token

pygame.init()

screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("5 LVL")
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
        Block(100, 500, 200, 300),
        Block(100, -50, 200, 100),
        Block(-400, 550, 200, 300),
        Block(-400, -50, 200, 100),
        Block(-900, 550, 200, 300),
        Block(-900, -50, 200, 180),
        Block(-1400, 450, 200, 300),
        Block(-1400, -50, 200, 100),
        Block(-3000, -50, 500, 200),
        Block(-3000, 400, 500, 1000),
        Block(-2600, 550, 130, 1000),
        Block(600, 250, 200, 500),
        Block(600, -50, 200, 100),
        Block(-4000, -50, 1100, 1000),
        Block(-1900, -50, 200, 100),
        Block(-2400, -50, 200, 100),
        Block(1100, -50, 200, 100),
        Block(1900, 550, 200, 300),

    ]

    triangles = [
        # Triangle(blocks[0], offset_x=25, offset_y=-25, size=45),
        Triangle(blocks[8], offset_x=470, offset_y=220, size=40, isInvert=True),
        Triangle(blocks[9], offset_x=470, offset_y=-25, size=40),
        Triangle(blocks[8], offset_x=225, offset_y=220, size=40, isInvert=True),
        Triangle(blocks[9], offset_x=225, offset_y=-25, size=40),
        Triangle(blocks[11], offset_x=35, offset_y=-25, size=40),
        Triangle(blocks[11], offset_x=80, offset_y=-25, size=40),
        Triangle(blocks[11], offset_x=125, offset_y=-25, size=40),
        Triangle(blocks[11], offset_x=170, offset_y=-25, size=40),
        Triangle(blocks[2], offset_x=100, offset_y=-25, size=40),
        Triangle(blocks[4], offset_x=100, offset_y=-25, size=40),
        Triangle(blocks[6], offset_x=100, offset_y=-25, size=40),
        Triangle(blocks[1], offset_x=100, offset_y=120, size=40, isInvert=True),
        Triangle(blocks[3], offset_x=100, offset_y=120, size=40, isInvert=True),
        Triangle(blocks[5], offset_x=100, offset_y=200, size=40, isInvert=True),
        Triangle(blocks[7], offset_x=100, offset_y=120, size=40, isInvert=True),
        Triangle(blocks[14], offset_x=100, offset_y=120, size=40, isInvert=True),
        Triangle(blocks[15], offset_x=100, offset_y=120, size=40, isInvert=True),


    ]

def init_coins():
    global coins
    coins = [
        Coin(185, 120),
        Coin(-2850, 260),
        Coin(-2750, 260,gravity= True),
        Coin(-2050, 500),
        Coin(1400, 150, gravity=True),
        Coin(1440, 350, gravity=True),
        Coin(1560, 200, gravity=True),
        Coin(1600, 300, gravity=True),
        Coin(1720, 250, gravity=True),
        Coin(2000, 350),

    ]

def init_tokens():
    global tokens
    tokens = [
        Token(-1500, 350, color=(255, 0, 0)),
        Token(-2650, 260),
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

door = Door(1990, 550, width=50, height=100, coins_required=4)

coins_collected = 0
font_coin = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 40)

def draw_coin_counter(screen):
    text = font_coin.render(f"Coins: {coins_collected}", True, (255, 170, 0))
    screen.blit(text, (10, 10))

def reset_game():
    global player, vertical_momentum, on_ground, scroll_x, scroll_y, coins_collected, player_speed, jump_force, gravity
    player.x = screen_w//2 - 20 - 200
    player.y = screen_h//2 - 20
    vertical_momentum = 0
    on_ground = False
    scroll_x = 0
    scroll_y = 0
    coins_collected = 0
    gravity = 0.9
    player_speed=5
    jump_force=-15
    init_level()
    init_coins()
    init_tokens()

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

        dx = 0
        if keys[pygame.K_a]:
            dx = -player_speed
        if keys[pygame.K_d]:
            dx = player_speed

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

        for token in tokens:
            token.update()
            if not token.collected and token.collide(player):
                token.collected = True
                if token.color == (255, 0, 0):
                    player_speed = 10
                    gravity = 0.5 * getZnak(gravity)
                elif token.color == (0, 255, 0):
                    player_speed = 5
                    gravity = 0.9 * getZnak(gravity)
                elif token.color == (0, 255, 255):
                    player_speed = 5
                    gravity = 2 * getZnak(gravity)
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

    screen.fill((0,0,0))

    background()

    for block in blocks:
        block.draw(screen, int(scroll_x), int(scroll_y))

    ground3d(int(scroll_x))

    for triangle in triangles:
        triangle.draw(screen, int(scroll_x), int(scroll_y))

    for coin in coins:
        if not coin.collected:
            coin.draw(screen, int(scroll_x), int(scroll_y))

    for token in tokens:
        if not token.collected:
            token.draw(screen, int(scroll_x), int(scroll_y))

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
            current_level = "file_6"

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