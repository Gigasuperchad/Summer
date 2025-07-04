import os
import pygame
import importlib
import random 

clock = pygame.time.Clock()

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("../titles/title.txt", "r") as file:
    title = file.read()
pygame.init()
pygame.mixer.init()
sound1 = pygame.mixer.Sound("../music/Mus_ANOTHER_HIM.oga")
sound1.play(-1).set_volume(0.3)

screen_x, screen_y = 800, 600
screen = pygame.display.set_mode((screen_x, screen_y))
count = 1

def pixel():
    for p in range(0, 900, 3):
        pygame.draw.line(screen, (0, 0, 0), (p, 0), (p, 700), 1)
        pygame.draw.line(screen, (0, 0, 0), (0, p), (900, p), 1)

a = [random.randint(-1000, 1000) for _ in range(2000)]
a_1 = [random.randint(-500, 500) for _ in range(200)]
a_2 = [random.randint(-500, 500) for _ in range(200)]

b = [random.randint(11, 20) for _ in range(2000)]
c = [random.randint(0, 400) for _ in range(2000)]
d = [random.randint(20, 100) for _ in range(200)]
color_BG = [random.randint(54, 180) for _ in range(2000)]

def backgoround():
    for i in range(2000):
        pygame.draw.circle(screen, (0,0,color_BG[i]), (a[i]-z//100, c[i]), 4)
    for i in range(200):
        pygame.draw.rect(screen, (color_BG[i],color_BG[i],color_BG[i]), (a[i]-z//b[i], c[i], d[i], d[i]))
    for i in range(30):
        pygame.draw.polygon(screen, (color_BG[i], 0, color_BG[i]), [(a[i]-z//b[i],600-c[i]-b[i]),(a_1[i]-z//b[i],800),(a_2[i]-z//b[i],800)], 2)
        pygame.draw.polygon(screen, (color_BG[i], 0, color_BG[i]), [(500-a[i]-z//b[i],600-c[i]-b[i]),(500-a_1[i]-z//b[i],800),(500-a_2[i]-z//b[i],800)], 2)
        pygame.draw.polygon(screen, (color_BG[i], 0, color_BG[i]), [(1000+a[i]-z//b[i],600-c[i]-b[i]),(1000+a_1[i]-z//b[i],800),(1000+a_2[i]-z//b[i],800)], 2)

def pixel():
    for p in range(0, 900, 3):
        pygame.draw.line(screen, (0, 0, 0), (p, 0), (p, 700), 1)
        pygame.draw.line(screen, (0, 0, 0), (0, p), (900, p), 1)

def ground3d():
    for i in range(0,30,3):
        pygame.draw.rect(screen, (200-i*5,200-i*5,200-i*5), (0-i,(460+i)-15,800,50))
        
def text():
    font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 105)
    text_surface = font.render(f"{title}", True, (0,0,0))
    text_rect = text_surface.get_rect(center=(400, 105)) 
    screen.blit(text_surface, text_rect)

    font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 100)
    text_surface = font.render(f"{title}", True, (255,255,255))
    text_rect = text_surface.get_rect(center=(400, 100)) 
    screen.blit(text_surface, text_rect)

    font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 50)

    text_surface = font.render("Play", True, "black")
    text_rect = text_surface.get_rect(center=(395, 305))
    screen.blit(text_surface, text_rect)
    text_surface = font.render("Play", True, "green")
    text_rect = text_surface.get_rect(center=(400, 300))
    screen.blit(text_surface, text_rect)

    text_surface = font.render("Exit", True, "black")
    text_rect = text_surface.get_rect(center=(screen_x//2, 400))
    screen.blit(text_surface, text_rect)
    text_surface = font.render("Exit", True, "red")
    text_rect = text_surface.get_rect(center=(screen_x//2+5, 395))
    screen.blit(text_surface, text_rect)
current_level = None

running = True
z = 0
x = 0
y = 0

gravity = 0.98
jump_power = 11
is_jumping = False
velocity = 0
current_level = None
menu = 1
running = True
while running:
    while menu == 1:
        z += 0.5
        x += 2
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (365 <= event.pos[0] <= 435) and (280 <= event.pos[1] <= 330):
                        current_level = "menu"
                        menu = 2
                    if (screen_x//2 - 50 <= event.pos[0] <= screen_x//2 + 60) and (375 <= event.pos[1] <= 400):
                        running = False
                        menu = 0
                if event.button ==5:
                    count -= 50
                if event.button == 4:
                    count += 50
        backgoround()
        ground3d()
        
        if (x > 974):
            x = -10
        if not is_jumping:
            random_jump = random.randint(0, 600)
            if random_jump > 590:
                is_jumping = True
                velocity = -jump_power
        else:
            velocity += gravity
            y += velocity
            if y >= 0:
                y = 0
                is_jumping = False
                velocity = 0

        pygame.draw.rect(screen,(255, 0, 0), (x, 430 + y , 30, 30))

        pygame.draw.ellipse(screen, (0, 0, 0), (screen_x / 2 - 500, screen_y - 100, 1000, 150))
        pygame.draw.ellipse(screen, (0, 0, 0), (screen_x / 2 - 500, screen_y / 2 - 350, 1000, 150))
        pygame.draw.rect(screen, (0, 0, 0), (screen_x - 110, 0, 110, 700))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 110, 700))

        pixel()
        text()

        pygame.display.flip()

    while menu == 2:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (screen_x / 2 - 300 + count <= event.pos[0] <= screen_x / 2 + count + 300) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        current_level = "file_1"
                    if (screen_x + count <= event.pos[0] <= screen_x + count + 600) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        current_level = "file_2"
                    if (screen_x + count + 700 <= event.pos[0] <= screen_x + count + 1300) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        current_level = "file_3"
                    if (screen_x + count + 1300 <= event.pos[0] <= screen_x + count + 1900) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        current_level = "file_4"
                    if (screen_x + count + 1900 <= event.pos[0] <= screen_x + count + 2600) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        current_level = "file_5"
                    if (screen_x + count + 2500 <= event.pos[0] <= screen_x + count + 3200) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        current_level = "file_6"
                    if (screen_x + count + 3100 <= event.pos[0] <= screen_x + count + 3800) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        current_level = "file_7"

                if event.button == 5 and count >= -4200:
                    count -= 54
                if event.button == 4 and count <= 0:
                    count += 54
        pygame.draw.rect(screen, (0, 0, 255), (screen_x / 2 - 300 + count, screen_y / 2 - 250, 600, 500))

        font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 100)

        text_surface = font.render("Level 1", True, "black")
        text_rect = text_surface.get_rect(center=(395 + count, 305))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("Level 1", True, "green")
        text_rect = text_surface.get_rect(center=(400 + count, 300))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 0, 255), (screen_x + count, screen_y / 2 - 250, 600, 500))

        text_surface = font.render("Level 2", True, "black")
        text_rect = text_surface.get_rect(center=(screen_x + 305 + count, 305))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("Level 2", True, "green")
        text_rect = text_surface.get_rect(center=(screen_x + 300 + count, 300))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 0, 255), (screen_x + count + 700, screen_y / 2 - 250, 600, 500))

        text_surface = font.render("Level 3", True, "black")
        text_rect = text_surface.get_rect(center=(screen_x + count + 1005, 305))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("Level 3", True, "green")
        text_rect = text_surface.get_rect(center=(screen_x + count + 1000, 300))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 0, 255), (screen_x + count + 1400, screen_y / 2 - 250, 600, 500))

        text_surface = font.render("Level 4", True, "black")
        text_rect = text_surface.get_rect(center=(screen_x + count + 1705, 305))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("Level 4", True, "yellow")
        text_rect = text_surface.get_rect(center=(screen_x + count + 1700, 300))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 0, 255), (screen_x + count + 2100, screen_y / 2 - 250, 600, 500))

        text_surface = font.render("Level 5", True, "black")
        text_rect = text_surface.get_rect(center=(screen_x + count + 2405, 305))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("Level 5", True, "yellow")
        text_rect = text_surface.get_rect(center=(screen_x + count + 2400, 300))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 0, 255), (screen_x + count + 2800, screen_y / 2 - 250, 600, 500))

        text_surface = font.render("Level 6", True, "black")
        text_rect = text_surface.get_rect(center=(screen_x + count + 3105, 305))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("Level 6", True, "yellow")
        text_rect = text_surface.get_rect(center=(screen_x + count + 3100, 300))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 0, 255), (screen_x + count + 3500, screen_y / 2 - 250, 600, 500))

        text_surface = font.render("Level 7", True, "black")
        text_rect = text_surface.get_rect(center=(screen_x + count + 3805, 305))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("Level 7", True, "red")
        text_rect = text_surface.get_rect(center=(screen_x + count + 3800, 300))
        screen.blit(text_surface, text_rect)

        pygame.draw.ellipse(screen, (0, 0, 0), (screen_x / 2 - 500, screen_y - 100, 1000, 100))
        pygame.draw.ellipse(screen, (0, 0, 0), (screen_x / 2 - 500, screen_y / 2 - 300, 1000, 100))

        font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 50)
        text_surface = font.render("< A   D >", True, "blue")
        text_rect = text_surface.get_rect(center=(400, 550))
        screen.blit(text_surface, text_rect)
        text_surface = font.render("< A   D >", True, "grey")
        text_rect = text_surface.get_rect(center=(398, 552))
        screen.blit(text_surface, text_rect)

        if current_level:
            try:
                sound1.stop()
                module = importlib.import_module(current_level)
                module.main()
            except Exception as e:keys = pygame.key.get_pressed()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and count >= -4200:
            count -= 8
        if keys[pygame.K_a] and count <= 0:
            count += 8
        pixel()
        pygame.display.flip()
        current_level = None


pygame.quit()