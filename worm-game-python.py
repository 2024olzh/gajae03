import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("귀여운 지렁이 식품 미션 게임")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)

# Font
font = pygame.font.Font(None, 36)

# Worm
class Worm:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.segments = [(self.x, self.y)]
        self.max_length = 20
        self.speed = 5

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > self.speed:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        else:
            self.x = target_x
            self.y = target_y

        self.segments.insert(0, (self.x, self.y))
        if len(self.segments) > self.max_length:
            self.segments.pop()

    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.circle(screen, PINK, segment, 18)
        
        # Draw eyes
        pygame.draw.circle(screen, BLACK, (int(self.x - 6), int(self.y - 3)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 6), int(self.y - 3)), 2)
        
        # Draw mouth
        pygame.draw.arc(screen, BLACK, (self.x - 8, self.y - 5, 16, 16), 0.2 * 3.14, 0.8 * 3.14, 2)

# Food
class Food:
    def __init__(self, x, y, food_type):
        self.x = x
        self.y = y
        self.type = food_type

# Game variables
worm = Worm()
foods = []
current_mission = ''
score = 0

missions = [
    {"type": "곡류", "foods": ['밥', '떡', '빵', '국수', '면', '옥수수', '감자', '고구마', '보리', '귀리', '밀가루', '스파게티']},
    {"type": "고기, 생선, 달걀, 콩류", "foods": ['두부', '콩', '소고기', '닭고기', '돼지고기', '달걀', '완두콩', '연어', '참치', '고등어']},
    {"type": "우유, 유제품류", "foods": ['우유', '치즈', '요구르트', '요플레']},
    {"type": "채소류와 과일류", "foods": ['사과', '바나나', '당근', '브로콜리', '토마토', '오렌지', '포도', '딸기', '수박', '배추', '시금치', '오이', '파프리카', '키위']},
]

def generate_food():
    mission = random.choice(missions)
    food_type = random.choice(mission["foods"])
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    return Food(x, y, food_type)

def set_new_mission():
    global current_mission
    current_mission = random.choice(missions)["type"]

def update_food_count():
    base_count = 20
    additional_count = score // 125
    total_count = base_count + additional_count
    
    while len(foods) < total_count:
        foods.append(generate_food())

def check_food_collision():
    global score
    for food in foods[:]:
        for segment in worm.segments:
            if ((segment[0] - food.x) ** 2 + (segment[1] - food.y) ** 2) ** 0.5 < 30:
                food_mission_type = next(m["type"] for m in missions if food.type in m["foods"])
                if food_mission_type == current_mission:
                    worm.max_length += 5
                    score += worm.max_length
                else:
                    worm.max_length = max(10, worm.max_length - 3)
                    score = max(0, score - 50)
                foods.remove(food)
                foods.append(generate_food())
                break

# Game loop
clock = pygame.time.Clock()
set_new_mission()
update_food_count()
mission_timer = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    worm.move(mouse_x, mouse_y)
    check_food_collision()
    update_food_count()

    screen.fill(WHITE)

    # Draw foods
    for food in foods:
        food_text = font.render(food.type, True, BLACK)
        screen.blit(food_text, (food.x - food_text.get_width() // 2, food.y - food_text.get_height() // 2))

    worm.draw(screen)

    # Draw score
    score_text = font.render(f"점수: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Draw mission
    mission_text = font.render(f"미션: {current_mission} 먹기", True, BLACK)
    screen.blit(mission_text, (10, 10))

    pygame.display.flip()

    # Update mission every 15 seconds
    mission_timer += clock.get_time()
    if mission_timer >= 15000:
        set_new_mission()
        mission_timer = 0

    clock.tick(60)

pygame.quit()
sys.exit()
