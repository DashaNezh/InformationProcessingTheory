import asyncio
import pygame
import math
import random
import platform

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Underwater World")
clock = pygame.time.Clock()
FPS = 60

# Цвета
BACKGROUND_COLOR = (0, 50, 100)  # Глубокий синий фон
CORAL_COLOR = (255, 150, 150)
BUBBLE_COLOR = (200, 220, 255, 100)

# Параметры сцены
CENTER = (WIDTH // 2, HEIGHT // 2)
SEA_FLOOR_Y = HEIGHT - 100


# Линейная интерполяция для градиентов
def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )


# Текстура рыбы с хвостом
def create_fish_texture(radius, base_color):
    size = radius * 3  # Увеличиваем размер для хвоста
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (radius, radius)
    colors = [
        base_color,
        tuple(max(0, c - 50) for c in base_color),
        tuple(max(0, c - 100) for c in base_color)
    ]
    steps = len(colors) - 1

    # Тело рыбы (эллипс)
    for r in range(radius, 0, -1):
        t = r / radius
        index = int(t * steps)
        frac = (t * steps) - index
        color = lerp_color(colors[index], colors[min(index + 1, steps)], frac)
        pygame.draw.ellipse(surface, color, [radius - r, radius - r // 2, 2 * r, r])

    # V-образный хвост
    tail_length = radius * 2
    tail_width = radius
    tail_color = tuple(max(0, c - 80) for c in base_color)
    # Верхняя лопасть
    pygame.draw.polygon(surface, tail_color, [
        (radius, radius),  # соединение с телом
        (radius - tail_length, radius - tail_width),  # верхний угол хвоста
        (radius - tail_length // 2, radius)  # середина хвоста
    ])
    # Нижняя лопасть
    pygame.draw.polygon(surface, tail_color, [
        (radius, radius),
        (radius - tail_length, radius + tail_width),
        (radius - tail_length // 2, radius)
    ])

    return surface


# Отрисовка коралла
def draw_coral(surface, base_pos, height, sway_angle):
    points = []
    for y in range(0, height, 10):
        sway = math.sin(y / 20 + sway_angle) * 10
        points.append((base_pos[0] + sway, base_pos[1] - y))
    for i in range(len(points) - 1):
        pygame.draw.line(surface, CORAL_COLOR, points[i], points[i + 1], 3)


# Отрисовка пузырька
def draw_bubble(surface, pos, radius):
    temp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(temp, BUBBLE_COLOR, (radius, radius), radius)
    surface.blit(temp, (pos[0] - radius, pos[1] - radius), special_flags=pygame.BLEND_ADD)


# Параметры рыб
FISHES = [
    {"radius": 15, "orbit_a": 150, "orbit_b": 80, "speed": 0.02, "color": (255, 200, 100)},
    {"radius": 10, "orbit_a": 200, "orbit_b": 120, "speed": 0.015, "color": (100, 255, 200)},
    {"radius": 12, "orbit_a": 250, "orbit_b": 150, "speed": 0.01, "color": (200, 100, 255)},
    {"radius": 12, "orbit_a": 300, "orbit_b": 200, "speed": 0.01, "color": (200, 100, 255)}
]
angles = [0] * len(FISHES)


# Основной цикл
async def main():
    global angles
    fish_textures = [create_fish_texture(f["radius"], f["color"]) for f in FISHES]

    # Генерация пузырьков
    bubbles = []
    for _ in range(20):
        x = random.randint(0, WIDTH)
        y = random.randint(SEA_FLOOR_Y, HEIGHT)
        radius = random.randint(3, 8)
        speed = random.uniform(1, 3)
        bubbles.append([x, y, radius, speed])

    # Генерация кораллов
    corals = []
    for _ in range(5):
        x = random.randint(100, WIDTH - 100)
        height = random.randint(50, 150)
        corals.append([x, SEA_FLOOR_Y, height])

    running = True
    time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление пузырьков
        for bubble in bubbles:
            bubble[1] -= bubble[3]  # Поднимаем пузырек
            if bubble[1] < 0:  # Перезапуск пузырька
                bubble[1] = SEA_FLOOR_Y
                bubble[0] = random.randint(0, WIDTH)

        # Отрисовка
        screen.fill(BACKGROUND_COLOR)

        # Морское дно
        pygame.draw.rect(screen, (200, 150, 100), [0, SEA_FLOOR_Y, WIDTH, HEIGHT - SEA_FLOOR_Y])

        # Кораллы
        for coral in corals:
            draw_coral(screen, (coral[0], coral[1]), coral[2], time * 0.1)

        # Пузырьки
        for x, y, radius, _ in bubbles:
            draw_bubble(screen, (x, y), radius)

        # Рыбы
        for i, fish in enumerate(FISHES):
            fish_x = CENTER[0] + fish["orbit_a"] * math.cos(angles[i])
            fish_y = CENTER[1] + fish["orbit_b"] * math.sin(angles[i])
            pos = (int(fish_x), int(fish_y))
            fish_rect = fish_textures[i].get_rect(center=pos)
            screen.blit(fish_textures[i], fish_rect)
            angles[i] += fish["speed"]

        pygame.display.flip()
        clock.tick(FPS)
        time += 1

        # Асинхронная пауза для Pyodide
        if platform.system() == "Emscripten":
            await asyncio.sleep(0)

    pygame.quit()


# Запуск
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())