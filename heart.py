import math
import random
import pygame
import os
import sys

pygame.init()
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
BACKGROUND_COLOR = (0, 0, 0)
FPS = 9999
SCALE = int(WIDTH / 95)
WORDS = ["Melisa"]
CENTER_TEXT = " Melisa "
COLORS = [
    (255, 105, 180),
    (255, 20, 147),
    (219, 112, 147),
    (255, 182, 193),
    (238, 130, 238)
]

class Particle:
    __slots__ = ('x', 'y', 'order', 'kind', 'word', 'color', 'alpha', 'flicker', 'font', 'delay', 'size_mult')
    def __init__(self, x, y, order, kind):
        self.x = x
        self.y = y
        self.order = order
        self.kind = kind
        self.word = random.choice(WORDS)
        self.color = random.choice(COLORS)
        self.alpha = 0
        self.flicker = random.uniform(0, math.pi * 2)
        self.font = None
        self.delay = 0
        self.size_mult = random.uniform(0.85, 1.15)

def heart_xy(t):
    x = 16 * (math.sin(t) ** 3)
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, -y

def to_screen(x, y):
    return x * SCALE + WIDTH / 2, y * SCALE + HEIGHT / 2

def build_outline_particles(n_outline, min_gap=22):
    particles = []
    placed = []
    for i in range(n_outline):
        t = (i / n_outline) * 2 * math.pi
        bx, by = heart_xy(t)
        sx, sy = to_screen(bx, by)
        if any(math.hypot(sx - px, sy - py) < min_gap for (px, py) in placed):
            continue
        placed.append((sx, sy))
        particles.append(Particle(sx, sy, i, "outline"))
    return particles

def build_fill_particles(n_fill, min_gap=32):
    particles = []
    placed = []
    attempts = 0
    max_attempts = n_fill * 120
    while len(particles) < n_fill and attempts < max_attempts:
        attempts += 1
        t = random.uniform(0, 2 * math.pi)
        r = random.uniform(0.0, 0.85)
        bx, by = heart_xy(t)
        px, py = bx * r, by * r
        sx, sy = to_screen(px, py)
        if any(math.hypot(sx - qx, sy - qy) < min_gap for (qx, qy) in placed):
            continue
        placed.append((sx, sy))
        particles.append(Particle(sx, sy, random.randint(0, 320), "fill"))
    return particles

def draw_glow_text(glow_layer, screen_layer, font, word, color, x, y, alpha, size_mult=1.0):
    if alpha <= 0:
        return
    if size_mult != 1.0:
        scaled_font = pygame.font.SysFont("arial", int(font.get_height() * size_mult), bold=True)
        txt = scaled_font.render(word, True, color)
    else:
        txt = font.render(word, True, color)
    txt.set_alpha(alpha)
    txt_rect = txt.get_rect(center=(x, y))
    
    if alpha > 10:
        glow_big = pygame.transform.smoothscale(txt, (int(txt.get_width() * 2.4), int(txt.get_height() * 2.4)))
        glow_big.set_alpha(max(0, alpha // 8))
        glow_rect = glow_big.get_rect(center=(x, y))
        glow_layer.blit(glow_big, glow_rect)
        
        glow_small = pygame.transform.smoothscale(txt, (int(txt.get_width() * 1.6), int(txt.get_height() * 1.6)))
        glow_small.set_alpha(max(0, alpha // 4))
        glow_rect = glow_small.get_rect(center=(x, y))
        glow_layer.blit(glow_small, glow_rect)
        
    screen_layer.blit(txt, txt_rect)

def show_menu(screen, clock):
    title_font = pygame.font.SysFont("georgia", 36, bold=True)
    btn_font = pygame.font.SysFont("arial", 24, bold=True)
    yes_rect = pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 + 50, 140, 50)
    no_rect = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 + 50, 140, 50)
    
    menu_running = True
    while menu_running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_rect.collidepoint(mouse_pos):
                    return True
                if no_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        screen.fill(BACKGROUND_COLOR)
        title_surf = title_font.render("Melisa'ya Kalp Cizmek Ister Misiniz?", True, (255, 182, 193))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(title_surf, title_rect)
        
        yes_color = (255, 20, 147) if yes_rect.collidepoint(mouse_pos) else (180, 15, 100)
        pygame.draw.rect(screen, yes_color, yes_rect, border_radius=8)
        yes_text = btn_font.render("Evet", True, (255, 255, 255))
        screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        
        no_color = (100, 100, 100) if no_rect.collidepoint(mouse_pos) else (60, 60, 60)
        pygame.draw.rect(screen, no_color, no_rect, border_radius=8)
        no_text = btn_font.render("Hayir", True, (200, 200, 200))
        screen.blit(no_text, no_text.get_rect(center=no_rect.center))
        
        pygame.display.flip()

def main():
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.FULLSCREEN)
    pygame.display.set_caption("Melisa <3")
    clock = pygame.time.Clock()
    
    show_menu(screen, clock)
    
    font_outline = pygame.font.SysFont("arial", 18, bold=True)
    font_fill = pygame.font.SysFont("arial", 15, bold=True)
    font_center = pygame.font.SysFont("georgia", 65, bold=True)
    
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BACKGROUND_COLOR)
    
    outline = build_outline_particles(n_outline=300)
    fill = build_fill_particles(n_fill=250)
    
    outline_span = max(p.order for p in outline) if outline else 0
    frames_per_step = 1.2
    fill_start_frame = int(outline_span * frames_per_step) + 20
    
    for p in fill:
        p.delay = fill_start_frame + p.order
    for p in outline:
        p.delay = int(p.order * frames_per_step)
        
    particles = outline + fill
    for p in particles:
        p.font = font_outline if p.kind == "outline" else font_fill
        
    running = True
    frame = 0
    music_started = False  # Müziğin tekrar tekrar tetiklenmesini engellemek için kontrol
    
    glow_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    text_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                
        screen.blit(background, (0, 0))
        glow_layer.fill((0, 0, 0, 0))
        text_layer.fill((0, 0, 0, 0))
        
        frame += 1
        
        for p in particles:
            if frame > p.delay and p.alpha < 255:
                p.alpha = min(255, p.alpha + 12 + random.randint(0, 4))
            if p.alpha >= 255:
                flick = 0.78 + 0.22 * math.sin(frame * 0.05 + p.flicker)
            else:
                flick = 1.0
            alpha = int(p.alpha * flick)
            if alpha <= 0:
                continue
            draw_glow_text(glow_layer, text_layer, p.font, p.word, p.color, p.x, p.y, alpha, p.size_mult)
            
        screen.blit(glow_layer, (0, 0))
        screen.blit(text_layer, (0, 0))
        
        center_start = fill_start_frame + 120
        if frame > center_start:
            progress = min(1.0, (frame - center_start) / 50)
            center_alpha = int(255 * (1 - math.exp(-progress * 7)))
            pulse = 1.0 + 0.03 * math.sin(frame * 0.06)
            
            center_surf = font_center.render(CENTER_TEXT, True, (255, 230, 240))
            new_width = int(center_surf.get_width() * pulse)
            new_height = int(center_surf.get_height() * pulse)
            
            if new_width > 0 and new_height > 0:
                center_surf = pygame.transform.smoothscale(center_surf, (new_width, new_height))
                center_surf.set_alpha(center_alpha)
                
            if center_alpha > 10:
                glow_center = pygame.transform.smoothscale(
                    center_surf, (int(center_surf.get_width() * 1.5), int(center_surf.get_height() * 1.5))
                )
                glow_center.set_alpha(center_alpha // 6)
                glow_rect = glow_center.get_rect(center=(WIDTH/2, HEIGHT/2))
                screen.blit(glow_center, glow_rect)
                
            text_rect = center_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(center_surf, text_rect)
            
            # --- MÜZİK BURADA BAŞLIYOR ---
            # Kalp dolup ortadaki yazı tamamen parladığı an müzik devreye girer
            if progress >= 1.0 and not music_started:
                if os.path.exists("love_you.mp3"):
                    try:
                        pygame.mixer.music.load("love_you.mp3")
                        pygame.mixer.music.play(-1)  # Döngüsel çalar
                        music_started = True
                    except Exception as e:
                        print("Müzik yükleme hatası:", e)
        
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("HATA OLUSTU:", e)
        import traceback
        traceback.print_exc()
