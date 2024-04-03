import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 7
PADDLE_SPEED = 7
FPS = 60

# Create window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Classes
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 80
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect)

    def move_up(self):
        if self.rect.top > 0:
            self.y -= PADDLE_SPEED
            self.rect.y = self.y

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.y += PADDLE_SPEED
            self.rect.y = self.y

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.speed = BALL_SPEED

    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect)

    def move(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def bounce(self):
        self.direction[1] *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

# Function to detect collisions
def detect_collision(ball, paddle):
    return ball.rect.colliderect(paddle.rect)

# Function to handle bot player movement
def bot_move(ball, paddle):
    if ball.rect.y < paddle.rect.y + paddle.height / 2:
        paddle.move_up()
    elif ball.rect.y > paddle.rect.y + paddle.height / 2:
        paddle.move_down()

# Initialize objects
player_paddle = Paddle(20, HEIGHT // 2 - 40)
bot_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - 40)
ball = Ball(WIDTH // 2 - 5, HEIGHT // 2 - 5)

clock = pygame.time.Clock()

# Show start prompt
font = pygame.font.Font(None, 36)
prompt_text = font.render("Press SPACE to start", True, WHITE)
prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

retry_prompt = font.render("Missed! Press SPACE to retry or ESC to quit", True, WHITE)
retry_prompt_rect = retry_prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

game_started = False
game_over = False

# Main game loop
running = True
while running:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                elif game_over:
                    game_over = False
                    player_paddle.rect.y = HEIGHT // 2 - 40
                    ball.reset()
            elif event.key == pygame.K_ESCAPE:
                if game_over:
                    running = False

    if game_started and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move_up()
        if keys[pygame.K_DOWN]:
            player_paddle.move_down()

        bot_move(ball, bot_paddle)

        ball.move()

        # Ball collision with walls
        if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
            ball.bounce()

        # Ball collision with paddles
        if detect_collision(ball, player_paddle) or detect_collision(ball, bot_paddle):
            ball.direction[0] *= -1

        # Ball out of bounds
        if ball.rect.left <= 0:
            game_over = True
            retry_prompt = font.render("Missed! Press SPACE to retry or ESC to quit", True, WHITE)
            retry_prompt_rect = retry_prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        if ball.rect.right >= WIDTH:
            game_over = True
            retry_prompt = font.render("Missed! Press SPACE to retry or ESC to quit", True, WHITE)
            retry_prompt_rect = retry_prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Draw objects
        player_paddle.draw()
        bot_paddle.draw()
        ball.draw()
    elif not game_over:
        win.blit(prompt_text, prompt_rect)
    else:
        win.blit(retry_prompt, retry_prompt_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
