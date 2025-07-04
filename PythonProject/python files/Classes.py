import pygame
import math
import random 
import time
screen_w, screen_h = 800, 600

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
        # self.hitbox.center = (self.x, self.y)

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
        self.color = (0, 0, 0) 
        self.outline_color = (255, 255, 255)  
        self.outline_thickness = 2  

    def is_open(self, coins_collected):
        return coins_collected >= self.coins_required

    def draw(self, screen, coins_collected, scroll_x=0, scroll_y=0):
        draw_x = self.x - scroll_x
        draw_y = self.y - scroll_y
        radius = self.width // 2
        
        outline_rect = pygame.Rect(
            draw_x - self.outline_thickness,
            draw_y - self.height - self.outline_thickness,
            self.width + self.outline_thickness * 2,
            self.height + self.outline_thickness
        )
        pygame.draw.rect(screen, self.outline_color, outline_rect)
        
        outline_center = (draw_x + self.width // 2, draw_y - self.height - self.outline_thickness)
        pygame.draw.circle(screen, self.outline_color, outline_center, radius + self.outline_thickness)
        
        outline_cut_rect = pygame.Rect(
            draw_x - self.outline_thickness,
            draw_y - self.height - self.outline_thickness,
            self.width + self.outline_thickness * 2,
            radius + self.outline_thickness
        )

        pygame.draw.rect(screen, self.outline_color, outline_cut_rect)

      
        door_rect = pygame.Rect(draw_x, draw_y - self.height, self.width, self.height)
        pygame.draw.rect(screen, self.color, door_rect)
        
       
        center = (draw_x + self.width // 2, draw_y - self.height)
        pygame.draw.circle(screen, self.color, center, radius)
       
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
    
class Cube:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.angle_x = random.uniform(0, 2 * math.pi)
        self.angle_y = random.uniform(0, 2 * math.pi)
        self.angle_z = random.uniform(0, 2 * math.pi)
        self.speed_x = random.uniform(0.0001, 0.03)
        self.speed_y = random.uniform(0.0001, 0.002)
        self.speed_z = random.uniform(0.0001, 0.002)
        self.size = random.randint(20, 50)
        self.color = (random.randint(0, 10), random.randint(0, 20), random.randint(0, 9))
        self.velocity_x = 0
        
        self.vertices = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1)
        ]
        
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  
            (4, 5), (5, 6), (6, 7), (7, 4),  
            (0, 4), (1, 5), (2, 6), (3, 7)   
        ]
        
        self.faces = [
            (0, 1, 2, 3), 
            (4, 5, 6, 7), 
            (0, 1, 5, 4),  
            (2, 3, 7, 6),  
            (0, 3, 7, 4),  
            (1, 2, 6, 5)   
        ]
        
        self.face_colors = [
            (max(0, self.color[0]-50), max(0, self.color[1]-50), max(0, self.color[2]-50)),
            self.color,
            (max(0, self.color[0]-30), max(0, self.color[1]-30), max(0, self.color[2]-30)),
            (min(255, self.color[0]+30), min(255, self.color[1]+30), min(255, self.color[2]+30)),
            (max(0, self.color[0]-20), max(0, self.color[1]-20), max(0, self.color[2]-20)),
            (min(255, self.color[0]+20), min(255, self.color[1]+20), min(255, self.color[2]+20))
        ]
    
    def project_point(self, vertex):
        x, y, z = vertex
        
        y_rot = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)
        z_rot = y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
        y, z = y_rot, z_rot
        
        x_rot = x * math.cos(self.angle_y) + z * math.sin(self.angle_y)
        z_rot = -x * math.sin(self.angle_y) + z * math.cos(self.angle_y)
        x, z = x_rot, z_rot
        
        x_rot = x * math.cos(self.angle_z) - y * math.sin(self.angle_z)
        y_rot = x * math.sin(self.angle_z) + y * math.cos(self.angle_z)
        x, y = x_rot, y_rot
        
        scale = self.size
        factor = 400 / (400 + z * 3)
        x_proj = x * scale * factor + self.x
        y_proj = y * scale * factor + self.y
        
        return (x_proj, y_proj, z)
    
    def update(self):
        self.angle_x += self.speed_x
        self.angle_y += self.speed_y
        self.angle_z += self.speed_z
        
        self.x += self.velocity_x
        
        if self.x < -100:
            self.x = screen_w + 100
        elif self.x > screen_w + 100:
            self.x = -100
    
    def draw(self, screen):
        projected = []
        for vertex in self.vertices:
            projected.append(self.project_point(vertex))
        
        sorted_faces = []
        for i, face in enumerate(self.faces):
            z_avg = sum(projected[v][2] for v in face) / len(face)
            sorted_faces.append((z_avg, i))
        
        sorted_faces.sort()
        
        for depth, face_idx in sorted_faces:
            face = self.faces[face_idx]
            color = self.face_colors[face_idx]
            
            points = [projected[v][:2] for v in face]
            pygame.draw.polygon(screen, color, points)
        
        for edge in self.edges:
            start = projected[edge[0]]
            end = projected[edge[1]]
            pygame.draw.line(screen, (200, 230, 255), start[:2], end[:2], 1)

class GridBackground:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = 60 
        self.original_size = 60
        self.rotation = 0
        self.original_rotation = 0
        self.color = (80, 120, 200)  
        self.original_color = (80, 120, 200)
        self.animation_phase = 0 
        self.animation_speed = 0.01
        self.last_time = time.time()
    
    def update(self):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        
        self.animation_phase += self.animation_speed * delta_time * 60
        
        if self.animation_phase >= 2.0:
            self.animation_phase = 0.0
            self.grid_size = self.original_size
            self.rotation = self.original_rotation
            self.color = self.original_color
        
        if self.animation_phase < 1.0:
            progress = self.animation_phase
        else:
            progress = 2.0 - self.animation_phase

        self.grid_size = self.original_size * (1.0 + 0.5 * math.sin(progress * math.pi))
        self.rotation = 10 * math.sin(progress * math.pi * 2)
        

        r = int(80 + 80 * math.sin(progress * math.pi))
        g = int(120 - 40 * math.sin(progress * math.pi))
        b = int(200 + 55 * math.sin(progress * math.pi * 0.5))
        self.color = (r, g, b)
    
    def draw(self, screen, scroll_x, scroll_y):
        grid_surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        offset_x = scroll_x % self.grid_size
        offset_y = scroll_y % self.grid_size
        

        grid_size_int = int(round(self.grid_size))
        
  
        for x in range(-grid_size_int, self.screen_width + grid_size_int, grid_size_int):
            line_x = x - offset_x
            pygame.draw.line(grid_surf, self.color, (line_x, 0), (line_x, self.screen_height), 1)
        

        for y in range(-grid_size_int, self.screen_height + grid_size_int, grid_size_int):
            line_y = y - offset_y
            pygame.draw.line(grid_surf, self.color, (0, line_y), (self.screen_width, line_y), 1)
        
        if self.rotation != 0:
            rotated_surf = pygame.transform.rotate(grid_surf, self.rotation)
            rotated_rect = rotated_surf.get_rect(center=(self.screen_width//2, self.screen_height//2))
            screen.blit(rotated_surf, rotated_rect)
        else:
            screen.blit(grid_surf, (0, 0))