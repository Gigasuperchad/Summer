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
    def __init__(self, screen_width=1000, screen_height=1000):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = 60 
        self.original_size = 60
        self.rotation = 0
        self.color_phase = 0  
        self.animation_phase = 0 
        self.animation_speed = 0.005  
        self.color_speed = 0.01 
        self.last_time = time.time()
    
    def update(self):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        
        self.animation_phase += self.animation_speed * delta_time * 60
        
        if self.animation_phase >= 2.0:
            self.animation_phase = 0.0
        
        if self.animation_phase < 1.0:
            progress = self.animation_phase
        else:
            progress = 2.0 - self.animation_phase
        
        self.grid_size = self.original_size * (1.0 + 0.5 * math.sin(progress * math.pi))
        
        self.rotation = 10 * math.sin(progress * math.pi * 2)
        
        self.color_phase += self.color_speed * delta_time * 60
        if self.color_phase > 1.0:
            self.color_phase = 0.0
        
       
        hue = self.color_phase * 360  
        r, g, b = self.hsv_to_rgb(hue, 0.8, 0.9)  
        self.color = (int(r * 255), int(g * 255), int(b * 255))
    
    def hsv_to_rgb(self, h, s, v):
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (r + m, g + m, b + m)
    
    def draw(self, screen, scroll_x, scroll_y):
        grid_surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
    
        offset_x = scroll_x % self.grid_size
        offset_y = scroll_y % self.grid_size
        

        grid_size_int = int(round(self.grid_size))
        
       
        for x in range(-grid_size_int, self.screen_width + grid_size_int, grid_size_int):
            line_x = x - offset_x
            pygame.draw.line(grid_surf, self.color, (line_x, 0), (line_x, self.screen_height), 2)
        

        for y in range(-grid_size_int, self.screen_height + grid_size_int, grid_size_int):
            line_y = y - offset_y
            pygame.draw.line(grid_surf, self.color, (0, line_y), (self.screen_width, line_y), 2)
        

        if self.rotation != 0:
            rotated_surf = pygame.transform.rotate(grid_surf, self.rotation)
            rotated_rect = rotated_surf.get_rect(center=(self.screen_width//2, self.screen_height//2))
            screen.blit(rotated_surf, rotated_rect)
        else:
            screen.blit(grid_surf, (0, 0))
class Sphere:
    def __init__(self):
        self.x = screen_w 
        self.y = screen_h // 2
        self.z = 0
        self.radius = 200
        self.latitude = 20
        self.longitude = 24
        self.vertices = []
        self.edges = []
        self.rotation_angle = 0
        self.rotation_speed = 0.002
        self.size = 800
        self.generate_vertices()
        self.generate_edges()
    
    def generate_vertices(self):
        self.vertices = []
        for i in range(self.latitude):
            theta = math.pi * i / self.latitude
            for j in range(self.longitude):
                phi = 2 * math.pi * j / self.longitude
                x = self.radius * math.sin(theta) * math.cos(phi)
                y = self.radius * math.sin(theta) * math.sin(phi)
                z = self.radius * math.cos(theta)
                self.vertices.append([x, y, z])
    
    def generate_edges(self):
        self.edges = []
        for i in range(self.latitude):
            for j in range(self.longitude):
                idx = i * self.longitude + j
                next_j = idx + 1 if j < self.longitude - 1 else idx - self.longitude + 1
                self.edges.append((idx, next_j))
                
                if i < self.latitude - 1:
                    next_i = (i + 1) * self.longitude + j
                    self.edges.append((idx, next_i))
    
    @staticmethod
    def rotate_x(point, angle):
        x, y, z = point
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]

    @staticmethod
    def rotate_y(point, angle):
        x, y, z = point
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return [x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a]
    
    def update(self):
        self.rotation_angle += self.rotation_speed
    
    def project_point(self, vertex):
        x, y, z = vertex
        rotated = self.rotate_y(self.rotate_x(vertex, self.rotation_angle), self.rotation_angle * 0.5)
        x, y, z = rotated
        
        factor = self.size / (self.size + z * 3)
        x_proj = x * factor + self.x
        y_proj = y * factor + self.y
        
        return (x_proj, y_proj, z)
    
    def draw(self, screen):
        """Отрисовка сферы"""
        projected = []
        for vertex in self.vertices:
            projected.append(self.project_point(vertex))
        
        draw_edges = []
        for edge in self.edges:
            start_idx, end_idx = edge
            start = projected[start_idx]
            end = projected[end_idx]
            
            avg_z = (start[2] + end[2]) / 2
            draw_edges.append((avg_z, (start[0], start[1]), (end[0], end[1])))
        
        draw_edges.sort(key=lambda x: x[0], reverse=True)
        
        for edge in draw_edges:
            pygame.draw.line(screen, (200, 0, 200), edge[1], edge[2])

class MenuTriangle:
    def __init__(self):
   
        min_x = min(screen_w, screen_h + 100)
        max_x = max(screen_w, screen_h + 100)
        self.x = random.randint(min_x, max_x)
        
        self.y = -5000  
        self.height = 10000 
        self.width = random.randint(50, 150)  
        self.color = (random.randint(100,138), random.randint(20,50), random.randint(100,230)) 
        self.speed_x = random.uniform(-10, -1)
        self.thickness = random.randint(3,6)
        self.points = [
            (self.x, self.y),  
            (self.x - self.width//2, self.y + self.height),  
            (self.x + self.width//2, self.y + self.height)  
        ]
    
    def update(self):
        self.x += self.speed_x
   
        self.points = [
            (self.x, self.y),
            (self.x - self.width//2, self.y + self.height),
            (self.x + self.width//2, self.y + self.height)
        ]

class PauseMenu:
    def __init__(self, screen, current_volume):
        self.screen = screen
        self.volume = current_volume
        self.width, self.height = screen_w, screen_h
        

        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  
        
        self.title_font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 70)
        self.option_font = pygame.font.Font("../fonts/RuneScape-ENA.ttf", 40)
        
        self.title_pos = (self.width // 2, 100)
        self.volume_pos = (self.width // 2, 200)
        self.slider_rect = pygame.Rect(self.width // 2 - 100, 250, 200, 20)
        self.resume_button = pygame.Rect(self.width // 2 - 100, 350, 200, 60)
        
        self.slider_knob = pygame.Rect(0, 0, 15, 30)
        self.update_slider_knob()
        self.dragging = False
    
    def update_slider_knob(self):
        knob_x = self.slider_rect.left + int(self.volume * self.slider_rect.width)
        self.slider_knob.center = (knob_x, self.slider_rect.centery)
    
    def draw(self):
        self.screen.blit(self.overlay, (0, 0))
        
        title = self.title_font.render("P a u s e E", True, (255,255,255))
        title_rect = title.get_rect(center=self.title_pos)
        self.screen.blit(title, title_rect)
        
        volume_text = self.option_font.render("Volume", True, (255,255,255))
        volume_rect = volume_text.get_rect(center=self.volume_pos)
        self.screen.blit(volume_text, volume_rect)
        
        pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
        pygame.draw.rect(self.screen, (70, 70, 200), 
                        (self.slider_rect.left, self.slider_rect.top, 
                         int(self.volume * self.slider_rect.width), 
                         self.slider_rect.height))
        
        pygame.draw.rect(self.screen, (200, 200, 255), self.slider_knob)
        pygame.draw.rect(self.screen, (150, 150, 200), self.slider_knob, 2)
        
        pygame.draw.rect(self.screen, (50, 180, 50), self.resume_button)
        pygame.draw.rect(self.screen, (30, 150, 30), self.resume_button, 3)
        
        resume_text = self.option_font.render("RESUME", True, (0,0,0))
        resume_rect = resume_text.get_rect(center=self.resume_button.center)
        self.screen.blit(resume_text, resume_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.volume = max(0.0, min(1.0, 
                    (event.pos[0] - self.slider_rect.left) / self.slider_rect.width))
                self.update_slider_knob()
                return "volume_changed"
            
            if self.resume_button.collidepoint(event.pos):
                return "resume"
            
            if self.slider_knob.collidepoint(event.pos):
                self.dragging = True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.volume = max(0.0, min(1.0, 
                    (event.pos[0] - self.slider_rect.left) / self.slider_rect.width))
                self.update_slider_knob()
                return "volume_changed"
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
        
        return None