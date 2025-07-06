import pygame
import random
import importlib
import sys
from Classes import Block, Triangle, Door, Coin, GridBackground, PauseMenu

pygame.init()

screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("4 LVL")
icon = pygame.image.load("../pictures/КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.mixer.init()
pygame.mixer.music.stop()
sound_death = pygame.mixer.Sound("../music/d19c2f47f78098a.mp3")
sound = pygame.mixer.Sound("../music/M.O.O.N. - Hydrogen.mp3")
sound.play().set_volume(0.3)

jump_force = -17
gravity = 0.9

maxJumpCount = 2
jumpCounter = maxJumpCount

def getZnak(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    return 0

player_speed = 5
current_level = None

def ground3d(scroll_x):
    for i in range(0, 30, 3):
        for block in blocks:
            rect = block.rect.copy()
            rect.x -= scroll_x
            rect.y += i - 15
            rect.height += 15 - i
            shade = max(0, 200 - i * 5)
            pygame.draw.rect(screen, (shade, shade, shade), rect)

def death():
    global running, vertical_momentum, on_ground

    death_screen = pygame.Surface((screen_w, screen_h))
    death_screen.fill((0, 0, 0))
    font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 100)
    text_surface = font.render("You Died", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_w // 2, screen_h // 2))

    font_small = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 40)
    hint_surface = font_small.render("Press R to restart or ESC to exit", True, (200, 200, 200))
    hint_rect = hint_surface.get_rect(center=(screen_w // 2, screen_h // 2 + 100))

    death_screen.blit(text_surface, text_rect)
    death_screen.blit(hint_surface, hint_rect)

    sound_death.play()
    sound_death.set_volume(0.3)

    dead = True
    while dead:
        screen.blit(death_screen, (0, 0))
        for p in range(0, 900, 2):
            pygame.draw.line(screen, (0, 0, 0), (p, 0), (p, 700), 1)
            pygame.draw.line(screen, (0, 0, 0), (0, p), (900, p), 1)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    reset_game()
                    dead = False

def init_level():
    global blocks, triangles

    blocks = [
        Block(-100, 400, 1200, 200),
        Block(-250, -100, 400, 800),
        Block(1100, 400, 1300, 800),
        Block(1100, 300, 1100, 5),
        Block(2300, -100, 400, 800),
        Block(1100, -200, 30, 500)
    ]

    triangles = [
        Triangle(blocks[0], offset_x=870, offset_y=-5, size=15),
        Triangle(blocks[0], offset_x=770, offset_y=-5, size=15),
        Triangle(blocks[0], offset_x=670, offset_y=-5, size=15),
        Triangle(blocks[0], offset_x=570, offset_y=-5, size=15),
        Triangle(blocks[0], offset_x=470, offset_y=-5, size=15),
        Triangle(blocks[0], offset_x=370, offset_y=-5, size=15)
    ]

def init_coins():
    global coins
    coins = [
        Coin(300, 340),
        Coin(400, 340),
        Coin(500, 340),
        Coin(600, 340),
        Coin(700, 340),
        Coin(1150, 240)
    ]

player = pygame.Rect(screen_w // 2 - 20 - 200, screen_h // 2 - 20, 60, 60)
player_color = (255, 0, 0)
vertical_momentum = 0
on_ground = False

scroll_x = 0
scroll_y = 0
grid_bg = GridBackground(screen_h, screen_w)
deadzone_width = 20

deadzone_left = screen_w // 2 - deadzone_width // 2
deadzone_right = screen_w // 2 + deadzone_width // 2

camera_smooth_speed = 0.1

door = Door(900, 400, width=60, height=100, coins_required=6)

coins_collected = 0
font_coin = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 40)

def draw_coin_counter(screen):
    text = font_coin.render(f"Coins: {coins_collected}", True, (255, 170, 0))
    screen.blit(text, (10, 10))

def reset_game():
    global player, vertical_momentum, on_ground, scroll_x, scroll_y, coins_collected, jumpCounter
    player.x = screen_w // 2 - 20 - 200
    player.y = screen_h // 2 - 20
    vertical_momentum = 0
    on_ground = False
    scroll_x = 0
    scroll_y = 0
    coins_collected = 0
    jumpCounter = maxJumpCount
    init_level()
    init_coins()

def collisions(dx):
    global vertical_momentum, jumpCounter, on_ground

    player.x += dx
    on_ground = False
    
    for block in blocks:
        if player.colliderect(block.rect):
            if dx > 0:
                player.right = block.rect.left
            elif dx < 0:
                player.left = block.rect.right

    global gravity
    vertical_momentum += gravity
    player.y += vertical_momentum

    for block in blocks:
        if player.colliderect(block.rect):
            if vertical_momentum > 0:
                player.bottom = block.rect.top
                vertical_momentum = 0
                jumpCounter = maxJumpCount
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

grid_bg = GridBackground(screen_w, screen_h)

a = [random.randint(-1000, 1000) for _ in range(5000)]
c = [random.randint(0, 400) for _ in range(5000)]
d = [random.randint(20, 100) for _ in range(5000)]

color_BG = [random.randint(0, 255) for _ in range(2000)]

def background(scroll_x, scroll_y):
    for i in range(5000):
        pygame.draw.circle(screen, (100, 100, 155 + d[i]), (a[i] - scroll_x // d[i], c[i] * 2), 1)

paused = False
current_volume = 1.0
pause_menu = PauseMenu(screen, current_volume)
f = True

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
        grid_bg.update()

        collisions(dx)

        for coin in coins:
            coin.update()
            if not coin.collected and coin.collide(player):
                coin.collected = True
                coins_collected += 1

        if keys[pygame.K_SPACE] and on_ground:
            vertical_momentum = jump_force
            on_ground = False
            jumpCounter -= 1
            f = False
        elif keys[pygame.K_SPACE] and jumpCounter > 0 and f:
            vertical_momentum = jump_force
            jumpCounter -= 1
            f = False

        if not keys[pygame.K_SPACE]:
            f = True

        door_collision = door.collide(player)
        if door_collision:
            font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 30)
            if door.is_open(coins_collected):
                msg = font.render("Дверь открыта! Нажмите E для перехода", True, (255, 0, 150))
                screen.blit(msg, (screen_w // 2 - msg.get_width() // 2, 50))

                if keys[pygame.K_e]:
                    current_level = "file_5"
                    sound.stop()
                    try:
                        module = importlib.import_module(current_level)
                        module.main()
                        reset_game()
                        sound.play().set_volume(0.3)
                    except ImportError:
        
                        current_level = None
            else:
                coins_needed = door.coins_required - coins_collected
                msg = font.render(f"Нужно собрать ещё {coins_needed} монет для перехода", True, (255, 0, 150))
                screen.blit(msg, (screen_w // 2 - msg.get_width() // 2, 50))

    screen.fill((0, 0, 0))
    background(scroll_x, scroll_y)
    grid_bg.draw(screen, scroll_x, scroll_y)

    for block in blocks:
        block.draw(screen, int(scroll_x), int(scroll_y))

    ground3d(int(scroll_x))

    for triangle in triangles:
        triangle.draw(screen, int(scroll_x), int(scroll_y))

    for coin in coins:
        if not coin.collected:
            coin.draw(screen, int(scroll_x), int(scroll_y))

    door.draw(screen, coins_collected, scroll_x, scroll_y)

    player_draw_rect = player.copy()
    player_draw_rect.x -= int(scroll_x)
    player_draw_rect.y -= int(scroll_y)
    pygame.draw.rect(screen, player_color, player_draw_rect)

    draw_coin_counter(screen)

    if paused:
        pause_menu.draw()

    if not paused and player.y > 900:
        death()

    pygame.display.flip()

pygame.quit()