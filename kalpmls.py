import pygame
import sys
import math
import random

def run_heart_animation():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Melisa")

    font = pygame.font.SysFont("Arial", 15, bold=True)
    center_font = pygame.font.SysFont("Arial", 48, bold=True)

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((0, 0, 0))

    particles = []
    text = "Melisa "
    text_len = len(text)
    char_index = 0

    def get_heart_point(t):
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        return x * 15, -y * 15

    # Videodaki dolgunluğu ve kontur kalınlığını yakalamak için çok sıkı mikro katmanlar
    layers = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.05]
    delay_accumulator = 0

    for scale in layers:
        # Harfler arası boşluğu tamamen sıfırlamak için nokta yoğunluğunu maksimuma çıkardık
        num_points = int(320 * scale)
        for i in range(num_points):
            t = (i / num_points) * 2 * math.pi
            hx, hy = get_heart_point(t)
            
            hx *= scale
            hy *= scale
            
            target_x = WIDTH // 2 + hx
            target_y = HEIGHT // 2 + hy
            
            # Tam videodaki canlı pembe-eflatun ton matrisi
            r = random.randint(245, 255)
            g = random.randint(120, 150)
            b = random.randint(190, 220)
            color = (r, g, b)
            
            particles.append({
                "char": text[char_index],
                "target_x": target_x,
                "target_y": target_y,
                "color": color,
                "alpha": 0,
                "delay": delay_accumulator,
                "p_flicker": random.uniform(0.04, 0.07)
            })
            char_index = (char_index + 1) % text_len
        # Katmanların içten dışa doğru bir sıvı gibi akarak büyüme gecikmesi
        delay_accumulator += 25

    clock = pygame.time.Clock()
    running = True
    frame = 0

    center_text_alpha = 0
    center_start_frame = delay_accumulator + 20

    while running:
        clock.tick(60)
        frame += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.blit(background, (0, 0))
        
        for p in particles:
            if frame > p["delay"]:
                # Videodaki o yumuşak belirme (fade-in) geçiş hızı
                if p["alpha"] < 255:
                    p["alpha"] = min(255, p["alpha"] + 10)
                
                # Videonun alametifarikası olan dinamik neon parıltı efekti
                flicker = 0.82 + 0.18 * math.sin(frame * p["p_flicker"])
                current_alpha = int(p["alpha"] * flicker)
                
                text_surf = font.render(p["char"], True, p["color"])
                text_surf.set_alpha(current_alpha)
                
                text_rect = text_surf.get_rect(center=(p["target_x"], p["target_y"]))
                screen.blit(text_surf, text_rect)

        # Kalp tamamlandığı an merkezde parıldayarak beliren büyük yazı
        if frame > center_start_frame:
            if center_text_alpha < 255:
                center_text_alpha = min(255, center_text_alpha + 5)
                
            c_flicker = 0.88 + 0.12 * math.sin(frame * 0.06)
            c_alpha = int(center_text_alpha * c_flicker)
            
            center_surf = center_font.render("Love You", True, (255, 185, 225))
            center_surf.set_alpha(c_alpha)
            center_rect = center_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(center_surf, center_rect)

        pygame.display.flip()

    pygame.quit()

while True:
    print("\n\n\n\n")
    secim = input("Kalbi çizmek ister misiniz? (e/h): ").strip().lower()
    
    if secim == 'e':
        print("\nPygame penceresi açılıyor...")
        run_heart_animation()
    elif secim == 'h':
        print("\nProgram sonlandırıldı.")
        input("CMD penceresini kapatmak için Enter'a basın...")
        break
    else:
        print("Lütfen sadece 'e' veya 'h' giriniz.")
