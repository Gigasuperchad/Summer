import pygame
import random
import math

with open("title.txt", "r") as file:
    content = file.read()

pygame.init()

screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h),pygame.FULLSCREEN)
pygame.display.set_caption(content)
icon = pygame.image.load("КАРТИНОЧКА.png")
pygame.display.set_icon(icon)

pygame.mixer.init()
sound_death = pygame.mixer.Sound("d19c2f47f78098a.mp3")
sound = pygame.mixer.Sound("aphex-twin-vordhosbn.mp3")
sound.play().set_volume(0.3)

a = [random.randint(-1000, 1000) for _ in range(2000)]

def backgoround():
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


def death():
    pygame.draw.rect(screen, (0,0,0), (0,0, 800, 700))
    death_screen = pygame.Surface((800, 600))
    death_screen.fill((0,0,0))
    sound.stop()
    font = pygame.font.Font("RuneScape-ENA.ttf", 100)
    text_surface = font.render("You Died", True, (255,255,255))
    text_rect = text_surface.get_rect(center=(400, 300)) 
    font_small = pygame.font.Font("RuneScape-ENA.ttf", 40)
    hint_surface = font_small.render("Press ESC to exit", True, (200,200,200))
    hint_rect = hint_surface.get_rect(center=(400, 400))
    
    death_screen.blit(text_surface, text_rect)
    death_screen.blit(hint_surface, hint_rect)

    sound_death.play()
    sound_death.set_volume(0.3)

    dead = True
    while dead:
        screen.blit(death_screen, (0,0))
        for p in range(0,900,2):    
            pygame.draw.line(screen, (0,0,0), (p, 0), (p, 700), 1)
            pygame.draw.line(screen, (0,0,0), (0, p ), (900, p), 1)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

class Triangle:
    def __init__(self, parent_block, offset_x=0, offset_y=0, size=30, color=(0, 255, 0), is_moving=False):
        self.parent_block = parent_block
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.size = size
        self.color = color
        self.hitbox = pygame.Rect(0, 0, size, size)
        self.animation_offset = 0
        self.is_moving = is_moving

    def update(self):
        if timer >= 371:
            if self.is_moving:
                self.animation_offset = 100 * math.sin(pygame.time.get_ticks() * 0.004)
            else:
                self.animation = 0
        self.x = self.parent_block.rect.x + self.offset_x + self.animation_offset
        self.y = self.parent_block.rect.y + self.offset_y
        self.hitbox.center = (self.x, self.y)
        
    def draw(self, screen):
        points = [
            (self.x - self.size//2, self.y + self.size//2),
            (self.x, self.y - self.size),
            (self.x + self.size//2, self.y + self.size//2)
        ]
        pygame.draw.polygon(screen, self.color, points, 2)

class Block:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255,255,255)
        self.original_y = y

player = pygame.Rect(screen_w//2 - 20 - 200, screen_h//2 - 20 , 60, 60)
player_color = (255, 0, 0)
jump_force = -15
gravity = 0.9
vertical_momentum = 0
on_ground = False

blocks = [
    Block(100, 400, 2000, 500), 
    Block(2100, 300, 300, 500),
    Block(2400, 200, 300, 800),
    Block(2700, 500, 1000, 800),
    Block(3800, 500, 300, 80),
    Block(3700, 900, 1000, 500),
]

triangles = [
    Triangle(blocks[0], offset_x=745, offset_y=-25, size=45, is_moving=True),
    Triangle(blocks[0], offset_x=1005, offset_y=-25, size=45,is_moving=True),
    Triangle(blocks[0], offset_x=1305, offset_y=-25, size=45,is_moving=True),
    Triangle(blocks[0], offset_x=1605, offset_y=-25, size=45,is_moving=True),
    Triangle(blocks[0], offset_x=1945, offset_y=-25, size=45),
    Triangle(blocks[1], offset_x=150, offset_y=-25, size=45,is_moving=True),
    Triangle(blocks[2], offset_x=150, offset_y=-25, size=45,is_moving=True),
    Triangle(blocks[3], offset_x=35, offset_y=-25, size=45),
    Triangle(blocks[3], offset_x=300, offset_y=-25, size=45, is_moving=True),
    Triangle(blocks[3], offset_x=445, offset_y=-25, size=45),
    Triangle(blocks[3], offset_x=965, offset_y=-25, size=45),
    Triangle(blocks[4], offset_x=45, offset_y=-25, size=45),
    Triangle(blocks[4], offset_x=145, offset_y=-25, size=45),
    Triangle(blocks[5], offset_x=240, offset_y=-25, size=45,is_moving=True),
    Triangle(blocks[5], offset_x=385, offset_y=-25, size=45),
    Triangle(blocks[5], offset_x=535, offset_y=-25, size=45,is_moving=True),
]

def ground3d():
    for i in range(0,30,3):
        pygame.draw.rect(screen, (200-i*5,200-i*5,200-i*5), (block.rect[0]-i,(block.rect[1]+i)-15,block.rect[2],block.rect[3]+20))
    
platform_speed = 5

def collisions():
    global vertical_momentum, on_ground
    on_ground = False

    vertical_momentum += gravity
    player.y += vertical_momentum
    
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
count = 0
running = True
clock = pygame.time.Clock()

i = 0
z = 0
w = 0
FPS = 60 
def pixel():
    for p in range(0,900,3):    
        pygame.draw.line(screen, (0,0,0), (p, 0), (p, 700), 1)
        pygame.draw.line(screen, (0,0,0), (0, p ), (900, p), 1)

timer = 0
color1 = (255,255,255)
while running:
    screen.fill((0, 0, 0))

    timer += 1

    for block in blocks: 
        z = -block.rect.x
    w = player.y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    font = pygame.font.Font("RuneScape-ENA.ttf", 40)
    text_surface = font.render("get ready...", True, color1)
    text_rect = text_surface.get_rect(center=(100, 100)) 
    screen.blit(text_surface, text_rect)

    if timer >= 371:
        color1 = (0,0,0)
        backgoround()

        FPS = 100 
        if keys[pygame.K_a]:
            count -= 1
            for block in blocks:
                block.rect.x += platform_speed
        else:
            for block in blocks:
                block.rect.x -= 0

        if keys[pygame.K_d]:
            count += 1
            for block in blocks:
                block.rect.x -= platform_speed
        else:
            for block in blocks:
                block.rect.x -= 0
    if keys[pygame.K_SPACE] and on_ground:
        vertical_momentum = jump_force
        on_ground = False
 
    collisions()

    for triangle in triangles:
        triangle.update()
    
    
    for block in blocks:
        pygame.draw.rect(screen, block.color, block.rect)
        ground3d()

    for triangle in triangles:
        triangle.draw(screen)
    
    # print(count)
    pygame.draw.rect(screen, player_color, player)  
    
    if player.y <= 300:
        if on_ground == False:
            for block in blocks:
                block.rect.y += 3
        else:
            block.rect.y += 0
    else:
        for block in blocks:
            block.rect.y -= 5

    if player.y > 1500:
        death()

    #pixel()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()