import os
import pygame
import importlib
import random 
from Classes import MenuTriangle

clock = pygame.time.Clock()

os.chdir(os.path.dirname(os.path.realpath(__file__)))
pygame.init()
with open("../titles/title.txt", "r") as file:
    title = file.read()
pygame.display.set_caption(f'{title}')
icon = pygame.image.load("../pictures/КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.mixer.init()
sound1 = pygame.mixer.Sound("../music/Home_-_Resonance_75115125.mp3")
sound1.play(-1).set_volume(0.3)

screen_x, screen_y = 800, 600
screen = pygame.display.set_mode((screen_x, screen_y))
count = 1

animation_active = False
animation_alpha = 10
max_alpha = 255
animation_speed = 3
menu_triangles = []

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
        y_base = 600 - c[i] - b[i]
        if y_base < 0: 
            y_base = 0
        
        pygame.draw.polygon(screen, (color_BG[i], 0, color_BG[i]), 
                           [(a[i]-z//b[i], y_base),
                            (a_1[i]-z//b[i], 800),
                            (a_2[i]-z//b[i], 800)], 2)
        
        pygame.draw.polygon(screen, (color_BG[i], 0, color_BG[i]), 
                           [(500-a[i]-z//b[i], y_base),
                            (500-a_1[i]-z//b[i], 800),
                            (500-a_2[i]-z//b[i], 800)], 2)
        
        pygame.draw.polygon(screen, (color_BG[i], 0, color_BG[i]), 
                           [(1000+a[i]-z//b[i], y_base),
                            (1000+a_1[i]-z//b[i], 800),
                            (1000+a_2[i]-z//b[i], 800)], 2)

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
    
loading_level = None
loading_timer = 0
loading_progress = 0
loading_max = 300

def text2():
    global animation_active, animation_alpha, menu_triangles, loading_level
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

    if animation_active or len(menu_triangles) > 0:
        overlay = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, animation_alpha))
        screen.blit(overlay, (0, 0))
        
        for menu_triangle in menu_triangles[:]:  
            menu_triangle.update()
            pygame.draw.polygon(screen, menu_triangle.color, menu_triangle.points, menu_triangle.thickness)
            
            if (menu_triangle.x < -500 or menu_triangle.x > screen_x + 500) and random.random() < 0.05:
                menu_triangles.remove(menu_triangle)
        
        if animation_active:
            animation_alpha = min(animation_alpha + animation_speed, max_alpha)
        else:
            animation_alpha = max(animation_alpha - animation_speed, 0)
            if animation_alpha == 0 and len(menu_triangles) == 0:
                menu_triangles = []
        
        if animation_active and len(menu_triangles) < 100 and random.random() < 0.9:
            menu_triangles.append(MenuTriangle())
        
      
        if loading_level:
            font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 50)
            progress_text = f'{loading_progress//3}%'
             
            text_surface = font.render(progress_text, True, "black")
            text_rect = text_surface.get_rect(center=(397, 295)) 
            screen.blit(text_surface, text_rect)
            
            text_surface = font.render(progress_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(405, 300)) 
            screen.blit(text_surface, text_rect)
            
            pygame.draw.rect(screen, (255, 255, 255), (250, 400, loading_progress, 5))
            pygame.draw.rect(screen, (255, 255, 255), (243, 392.5, 315, 20), 4)

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

timer1 = False
timer_1 = 0
timer2= False
timer_2 = 0
timer3 = False
timer_3 = 0
current_level = None
click_blocked = False

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = 1 
                   
                    animation_active = False
                    animation_alpha = 10
                    menu_triangles = []
            elif event.type == pygame.MOUSEBUTTONDOWN and not click_blocked:
                if event.button == 1: 
                    if (screen_x / 2 - 300 + count <= event.pos[0] <= screen_x / 2 + count + 300) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        
                        animation_active = True
                        menu_triangles = [MenuTriangle() for _ in range(5)] 
                        click_blocked = True
                        loading_level = "file_1"
                        loading_timer = 0
                        loading_progress = 0
                    
                    elif (screen_x + count <= event.pos[0] <= screen_x + count + 600) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        
                        animation_active = True
                        menu_triangles = [MenuTriangle() for _ in range(5)] 
                        click_blocked = True
                        loading_level = "file_2"
                        loading_timer = 0
                        loading_progress = 0
                    
                    elif (screen_x + count + 700 <= event.pos[0] <= screen_x + count + 1300) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        
                        animation_active = True
                        menu_triangles = [MenuTriangle() for _ in range(5)] 
                        click_blocked = True
                        loading_level = "file_3"
                        loading_timer = 0
                        loading_progress = 0
                    
                    
                    elif (screen_x + count + 1300 <= event.pos[0] <= screen_x + count + 1900) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        animation_active = True
                        menu_triangles = [MenuTriangle() for _ in range(5)] 
                        click_blocked = True
                        loading_level = "file_4"
                        loading_timer = 0
                        loading_progress = 0
                    
                    elif (screen_x + count + 1900 <= event.pos[0] <= screen_x + count + 2600) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        animation_active = True
                        menu_triangles = [MenuTriangle() for _ in range(5)] 
                        click_blocked = True
                        loading_level = "file_5"
                        loading_timer = 0
                        loading_progress = 0
                    
                    elif (screen_x + count + 2500 <= event.pos[0] <= screen_x + count + 3200) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        animation_active = True
                        menu_triangles = [MenuTriangle() for _ in range(5)] 
                        click_blocked = True
                        loading_level = "file_6"
                        loading_timer = 0
                        loading_progress = 0
                    
                    elif (screen_x + count + 3100 <= event.pos[0] <= screen_x + count + 3800) and (
                            screen_y / 2 - 250 <= event.pos[1] <= screen_y / 2 + 250):
                        animation_active = True
                        menu_triangles = [MenuTriangle() for _ in range(5)] 
                        click_blocked = True
                        loading_level = "file_7"
                        loading_timer = 0
                        loading_progress = 0
                if event.button == 5 and count >= -4200:
                    count -= 54
                if event.button == 4 and count <= 0:
                    count += 54
        
        pygame.draw.rect(screen, (0, 0, 255), (screen_x / 2 - 300 + count, screen_y / 2 - 250, 600, 500))
        text2()
        
        if loading_level:
            loading_timer += 1
            sound1.stop()
            loading_progress = min(loading_timer, loading_max)
            
            if loading_progress >= loading_max:
                current_level = loading_level
                loading_level = None
                animation_active = False
        
        if current_level:
            try:
                module = importlib.import_module(current_level)
                module.main()
                current_level = None
                click_blocked = False
                animation_active = False
                animation_alpha = 10
                menu_triangles = []
            except Exception as e:
                current_level = None
                click_blocked = False
                animation_active = False
                animation_alpha = 10
                menu_triangles = []

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and count >= -4200:
            count -= 8
        if keys[pygame.K_a] and count <= 0:
            count += 8
        
        pixel()
        pygame.display.flip()

pygame.quit()