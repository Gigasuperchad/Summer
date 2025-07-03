import pygame
import math

class Block:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255,255,255)

    def draw(self, screen, scroll_x, scroll_y):
        draw_rect = self.rect.copy()
        draw_rect.x -= scroll_x
        draw_rect.y -= scroll_y
        pygame.draw.rect(screen, self.color, draw_rect)

class Triangle:
    def __init__(self, parent_block, offset_x=0, offset_y=0, size=30, color=(0, 255, 0)):
        self.parent_block = parent_block
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.size = size
        self.color = color
        self.hitbox = pygame.Rect(0, 0, size, size)
        self.x = 0
        self.y = 0

    def update(self):
        self.x = self.parent_block.rect.x + self.offset_x
        self.y = self.parent_block.rect.y + self.offset_y
        self.hitbox.center = (self.x, self.y)

    def draw(self, screen, scroll_x, scroll_y):
        points = [
            (self.x - self.size//2 - scroll_x, self.y + self.size//2 - scroll_y),
            (self.x - scroll_x, self.y - self.size - scroll_y),
            (self.x + self.size//2 - scroll_x, self.y + self.size//2 - scroll_y)
        ]
        pygame.draw.polygon(screen, self.color, points)

class Door:
    def __init__(self, x, y, width=60, height=100, coins_required=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.coins_required = coins_required
        self.rect = pygame.Rect(self.x, self.y - self.height, self.width, self.height)

        self.color = (0, 0,0)  # цвет двери

    def is_open(self, coins_collected):
        return coins_collected >= self.coins_required

    def draw(self, screen, coins_collected, scroll_x=0, scroll_y=0):
        draw_x = self.x - scroll_x
        draw_y = self.y - scroll_y

        # Рисуем прямоугольную дверь
        door_rect = pygame.Rect(draw_x, draw_y - self.height, self.width, self.height)
        pygame.draw.rect(screen, self.color, door_rect)

        # Параметры арки
        center = (draw_x + self.width // 2, draw_y - self.height)
        radius = self.width // 2

        # Рисуем коричневую полукруглую арку (заливка)
        pygame.draw.circle(screen, self.color, center, radius)

        # Вырезаем нижнюю половину круга, чтобы осталась только арка
        cut_rect = pygame.Rect(draw_x, draw_y - self.height, self.width, radius)
        pygame.draw.rect(screen, self.color, cut_rect)

    def collide(self, player_rect):
        return self.rect.colliderect(player_rect)

class Coin:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.base_y = y
        self.size = size
        self.collected = False

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        center = (self.size // 2, self.size // 2)
        outer_radius = self.size // 2 - 4
        thickness = 4  # толщина буквы
        inner_radius = outer_radius - thickness

        pygame.draw.circle(self.image, (255, 215, 0), center, outer_radius)
        pygame.draw.circle(self.image, (255, 255, 150), center, outer_radius - 6)

        c_outer_radius = outer_radius - 10
        c_inner_radius = c_outer_radius - thickness

        start_angle = math.radians(45)
        end_angle = math.radians(315)

        points = []
        steps = 30

        for i in range(steps + 1):
            angle = start_angle + (end_angle - start_angle) * i / steps
            x = center[0] + c_outer_radius * math.cos(angle)
            y = center[1] + c_outer_radius * math.sin(angle)
            points.append((x, y))

        for i in range(steps, -1, -1):
            angle = start_angle + (end_angle - start_angle) * i / steps
            x = center[0] + c_inner_radius * math.cos(angle)
            y = center[1] + c_inner_radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(self.image, (0, 0, 0), points)

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        self.float_offset = 0
        self.float_speed = 0.05
        self.float_amplitude = 5
        self.float_angle = 0

    def update(self):
        self.float_angle += self.float_speed
        if self.float_angle > 2 * math.pi:
            self.float_angle -= 2 * math.pi

        self.float_offset = math.sin(self.float_angle) * self.float_amplitude
        self.rect.y = int(self.base_y + self.float_offset)

    def draw(self, screen, scroll_x=0, scroll_y=0):
        draw_x = self.rect.x - scroll_x
        draw_y = self.rect.y - scroll_y
        screen.blit(self.image, (draw_x, draw_y))

    def collide(self, player_rect):
        return self.rect.colliderect(player_rect)
