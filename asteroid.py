import pygame
import random
import math
import time
import sys

# 설정
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Asteroid Game')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

# 우주선
spaceship_img = pygame.image.load('spaceship.png')
spaceship_rect = spaceship_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
spaceship_radius = max(spaceship_rect.width, spaceship_rect.height) // 2

# 소행성: 우주선 주변 150픽셀 이내 금지
def is_far_from_spaceship(x, y, min_distance=150):
    sx, sy = spaceship_rect.center
    return math.hypot(x - sx, y - sy) > (spaceship_radius + min_distance)

asteroids = []
while len(asteroids) < 7:
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    
    if is_far_from_spaceship(x, y):
        dx, dy = random.choice([-3, -2, -1, 1, 2, 3]), random.choice([-3, -2, -1, 1, 2, 3])
        r = random.randint(20, 40)
        asteroids.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'r': r})

start_time = time.time()

def detect_collision(ax, ay, ar, bx, by, br):
    return math.hypot(ax - bx, ay - by) < (ar + br)

# 메인 루프
running = True
while running:
    dt = clock.tick(60)
    screen.fill((0, 0, 30))
    current_time = int(time.time() - start_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 방향 입력 벡터 계산
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    # 대각선 속도 조정 (단위 벡터 사용)
    if dx != 0 or dy != 0:
        length = math.hypot(dx, dy)
        dx, dy = dx / length, dy / length
        speed = 5
        spaceship_rect.x += int(dx * speed)
        spaceship_rect.y += int(dy * speed)

    # 화면 경계 제한
    spaceship_rect.x = max(0, min(spaceship_rect.x, WIDTH - spaceship_rect.width))
    spaceship_rect.y = max(0, min(spaceship_rect.y, HEIGHT - spaceship_rect.height))

    # 우주선 그리기
    screen.blit(spaceship_img, spaceship_rect)
    pygame.draw.circle(screen, WHITE, spaceship_rect.center, spaceship_radius, 1)

    # 소행성 이동 및 충돌
    for asteroid in asteroids:
        asteroid['x'] += asteroid['dx']
        asteroid['y'] += asteroid['dy']
        if asteroid['x'] < 0 or asteroid['x'] > WIDTH:
            asteroid['dx'] *= -1
        if asteroid['y'] < 0 or asteroid['y'] > HEIGHT:
            asteroid['dy'] *= -1

        pygame.draw.circle(screen, WHITE, (int(asteroid['x']), int(asteroid['y'])), asteroid['r'])

        if detect_collision(asteroid['x'], asteroid['y'], asteroid['r'],
            spaceship_rect.centerx, spaceship_rect.centery, spaceship_radius):
            print(f'게임 종료! 생존 시간: {current_time}초')
            running = False

    # 시간 출력
    font = pygame.font.SysFont(None, 30)
    time_surface = font.render(f'Time: {current_time}', True, WHITE)
    screen.blit(time_surface, (WIDTH - 120, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
