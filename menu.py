import pygame
import importlib

with open("title.txt", "r") as file:
    content = file.read()
pygame.display.set_caption(content)

icon = pygame.image.load("КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.init()
pygame.mixer.init()


screen_x, screen_y = 800, 600
screen = pygame.display.set_mode((screen_x, screen_y),pygame.FULLSCREEN) 
count = 0
count_1 = 0

def pixel():
    for p in range(0,900,3):    
        pygame.draw.line(screen, (0,0,0), (p, 0), (p, 700), 1)
        pygame.draw.line(screen, (0,0,0), (0, p ), (900, p), 1)

color1 = (255,255,255)
color2 = (255,255,255)
current_level = None

running = True
while running:

    screen.fill((0,0,0))

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (screen_x/2-300 + count <= event.pos[0] <= screen_x/2 + count + 300) and (screen_y/2-250 <= event.pos[1] <= screen_y/2 + 250):
                color1 = (247,255,33)
                current_level = "proj"
            if (screen_x + count <= event.pos[0] <= screen_x + count + 600) and (screen_y/2-250 <= event.pos[1] <= screen_y/2 + 250):
                color2 = (247,255,33)
                current_level = "proj_1"
            if (screen_x + count + 700 <= event.pos[0] <= screen_x + count + 1300) and (screen_y/2-250 <= event.pos[1] <= screen_y/2 + 250):
                color2 = (247,255,33)
                current_level = "proj_2"
               
    pygame.draw.rect(screen, (0,0,255), (screen_x/2-300 + count, screen_y/2-250, 600, 500))

    font = pygame.font.Font("RuneScape-ENA.ttf", 100)

    text_surface = font.render("Level 1", True, (0,0,0))
    text_rect = text_surface.get_rect(center=(395 + count, 305)) 
    screen.blit(text_surface, text_rect)
    text_surface = font.render("Level 1", True, color1)
    text_rect = text_surface.get_rect(center=(400 + count, 300)) 
    screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, (0,0,255), (screen_x + count, screen_y/2-250, 600, 500))

    text_surface = font.render("Level 2", True, (0,0,0))
    text_rect = text_surface.get_rect(center=(screen_x + 305 + count, 305))
    screen.blit(text_surface, text_rect)
    text_surface = font.render("Level 2", True, color2)
    text_rect = text_surface.get_rect(center=(screen_x + 300 + count, 300)) 
    screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, (0,0,255), (screen_x + count + 700, screen_y/2-250, 600, 500))

    text_surface = font.render("########", True, (0,0,0))
    text_rect = text_surface.get_rect(center=(screen_x + count + 1005, 305))
    screen.blit(text_surface, text_rect)
    text_surface = font.render("########", True, color2)
    text_rect = text_surface.get_rect(center=(screen_x + count + 1000, 300)) 
    screen.blit(text_surface, text_rect)

    pygame.draw.ellipse(screen, (0,0,0), (screen_x/2-500, screen_y-100, 1000,100))
    pygame.draw.ellipse(screen, (0,0,0), (screen_x/2-500, screen_y/2-300, 1000,100))

    if current_level:
        try:
            module = importlib.import_module(current_level)
            module.main()  
        except Exception as e:
            print(f"Ошибка загрузки уровня: {e}")
        current_level = None
        color1 = color2 = (255, 255, 255)


    keys = pygame.key.get_pressed()
    if -1407 <= count <= 0:
        if keys[pygame.K_a]:
            count += 3
        if keys[pygame.K_d]:
            count -= 3
    else:
        if count < -1300:
            count = -1404
        else: 
            count = 0
    print(count)
    pixel()
 
    pygame.display.flip()

pygame.quit()

