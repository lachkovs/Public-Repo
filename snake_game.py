import pygame
import random
import sys

# Settings
WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 10

BLACK  = (0, 0, 0)
GREEN  = (0, 200, 0)
DGREEN = (0, 140, 0)
RED    = (200, 0, 0)
WHITE  = (255, 255, 255)
GRAY   = (40, 40, 40)

def random_food(snake):
    while True:
        pos = (
            random.randrange(0, WIDTH // CELL) * CELL,
            random.randrange(0, HEIGHT // CELL) * CELL,
        )
        if pos not in snake:
            return pos

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("consolas", size, bold=True)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    surface.blit(surf, rect)

def game_loop(screen, clock):
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL, 0)
    food = random_food(snake)
    score = 0
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP    and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN  and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT  and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Wall collision
        if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            return score

        # Self collision
        if head in snake:
            return score

        snake.insert(0, head)

        if head == food:
            score += 1
            food = random_food(snake)
        else:
            snake.pop()

        # Draw
        screen.fill(BLACK)

        # Grid
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # Food
        pygame.draw.rect(screen, RED, (*food, CELL, CELL))

        # Snake
        for i, seg in enumerate(snake):
            color = GREEN if i == 0 else DGREEN
            pygame.draw.rect(screen, color, (*seg, CELL, CELL))
            pygame.draw.rect(screen, BLACK, (*seg, CELL, CELL), 1)

        # Score
        draw_text(screen, f"Score: {score}", 20, 60, 14)

        pygame.display.flip()

    return score

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    while True:
        # Start screen
        screen.fill(BLACK)
        draw_text(screen, "SNAKE", 60, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text(screen, "Arrow keys to move", 22, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text(screen, "Press any key to start", 20, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

        score = game_loop(screen, clock)

        # Game over screen
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 54, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text(screen, f"Score: {score}", 30, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text(screen, "Press any key to play again", 20, WIDTH // 2, HEIGHT // 2 + 55)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

if __name__ == "__main__":
    main()
