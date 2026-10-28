import pygame
import random
import json
import os

pygame.init()



WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20

BOARD_X = 60
BOARD_Y = 150
BOARD_WIDTH = 680
BOARD_HEIGHT = 400

COLS = BOARD_WIDTH // CELL_SIZE
ROWS = BOARD_HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nokia Snake - Neon Edition")

clock = pygame.time.Clock()



BACKGROUND = (13, 12, 30)
BOARD_COLOR = (0, 0, 0)
NEON_GREEN = (0, 255, 145)
SNAKE_GREEN = (0, 220, 115)
HEAD_GREEN = (100, 255, 180)
PINK = (255, 0, 255)
WHITE = (240, 245, 255)
MUTED = (145, 155, 175)
BUTTON_COLOR = (0, 100, 60)
GRID_COLOR = (0, 55, 38)



title_font = pygame.font.Font(None, 48)
score_font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 25)
game_over_font = pygame.font.Font(None, 60)



SAVE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "highscore.json"
)


def load_best_score():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return max(0, int(data.get("best_score", 0)))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def save_best_score(score):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump({"best_score": score}, file, indent=4)
    except OSError:
        print("Could not save the best score.")


best_score = load_best_score()




def create_food(snake_body):
    empty_cells = [
        (x * CELL_SIZE, y * CELL_SIZE)
        for x in range(COLS)
        for y in range(ROWS)
        if (x * CELL_SIZE, y * CELL_SIZE) not in snake_body
    ]

    return random.choice(empty_cells) if empty_cells else None


def reset_game():
    snake_body = [
        (200, 200),
        (180, 200),
        (160, 200)
    ]

    direction = "RIGHT"
    food = create_food(snake_body)
    score = 0
    lives = 3

    return snake_body, direction, food, score, lives


snake_body, direction, food, score, lives = reset_game()

running = True
paused = False
game_over = False



pause_button = pygame.Rect(620, 65, 120, 42)
restart_button = pygame.Rect(290, 365, 220, 48)



while running:

    

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE and not game_over:
                paused = not paused

            if event.key == pygame.K_r and game_over:
                snake_body, direction, food, score, lives = reset_game()
                game_over = False
                paused = False

            if not paused and not game_over:

                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"

                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"

                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if pause_button.collidepoint(event.pos) and not game_over:
                paused = not paused

            if game_over and restart_button.collidepoint(event.pos):
                snake_body, direction, food, score, lives = reset_game()
                game_over = False
                paused = False

    

    if not paused and not game_over:

        head_x, head_y = snake_body[0]

        if direction == "UP":
            head_y -= CELL_SIZE

        elif direction == "DOWN":
            head_y += CELL_SIZE

        elif direction == "LEFT":
            head_x -= CELL_SIZE

        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        ate_food = new_head == food

        body_to_check = snake_body if ate_food else snake_body[:-1]

        hit_wall = (
            head_x < 0
            or head_x >= BOARD_WIDTH
            or head_y < 0
            or head_y >= BOARD_HEIGHT
        )

        hit_body = new_head in body_to_check

        if hit_wall or hit_body:

            lives -= 1

            if lives <= 0:
                game_over = True

            else:
                snake_body = [
                    (200, 200),
                    (180, 200),
                    (160, 200)
                ]

                direction = "RIGHT"
                food = create_food(snake_body)

        else:

            snake_body.insert(0, new_head)

            if ate_food:

                score += 1

                if score > best_score:
                    best_score = score
                    save_best_score(best_score)

                food = create_food(snake_body)

                if food is None:
                    game_over = True

            else:
                snake_body.pop()

    

    screen.fill(BACKGROUND)

    title = title_font.render(
        "Nokia Snake - Neon Edition",
        True,
        NEON_GREEN
    )

    subtitle = small_font.render(
        "Neon Edition",
        True,
        MUTED
    )

    screen.blit(title, (60, 25))
    screen.blit(subtitle, (63, 70))

    

    screen.blit(
        score_font.render(f"Score: {score}", True, WHITE),
        (60, 105)
    )

    screen.blit(
        score_font.render(f"Best: {best_score}", True, NEON_GREEN),
        (260, 105)
    )

    screen.blit(
        score_font.render(f"Lives: {lives}", True, WHITE),
        (480, 105)
    )

    

    pygame.draw.rect(
        screen,
        BUTTON_COLOR,
        pause_button,
        border_radius=10
    )

    button_label = small_font.render(
        "RESUME" if paused else "PAUSE",
        True,
        WHITE
    )

    screen.blit(
        button_label,
        button_label.get_rect(center=pause_button.center)
    )

    

    board_rect = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_WIDTH,
        BOARD_HEIGHT
    )

    pygame.draw.rect(screen, BOARD_COLOR, board_rect)

    # Vertical grid lines
    for x in range(0, BOARD_WIDTH + 1, CELL_SIZE):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (BOARD_X + x, BOARD_Y),
            (BOARD_X + x, BOARD_Y + BOARD_HEIGHT)
        )

    # Horizontal grid lines
    for y in range(0, BOARD_HEIGHT + 1, CELL_SIZE):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (BOARD_X, BOARD_Y + y),
            (BOARD_X + BOARD_WIDTH, BOARD_Y + y)
        )

    pygame.draw.rect(
        screen,
        NEON_GREEN,
        board_rect,
        3,
        border_radius=3
    )

    

    if food is not None:

        food_rect = pygame.Rect(
            BOARD_X + food[0] + 4,
            BOARD_Y + food[1] + 4,
            CELL_SIZE - 8,
            CELL_SIZE - 8
        )

        pygame.draw.circle(
            screen,
            PINK,
            food_rect.center,
            CELL_SIZE // 2 - 3
        )

    

    for index, segment in enumerate(snake_body):

        segment_rect = pygame.Rect(
            BOARD_X + segment[0] + 2,
            BOARD_Y + segment[1] + 2,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        )

        color = HEAD_GREEN if index == 0 else SNAKE_GREEN

        pygame.draw.rect(
            screen,
            color,
            segment_rect,
            border_radius=5
        )

    

    if paused and not game_over:

        overlay = pygame.Surface(
            (BOARD_WIDTH, BOARD_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (BOARD_X, BOARD_Y))

        pause_text = title_font.render(
            "PAUSED",
            True,
            NEON_GREEN
        )

        screen.blit(
            pause_text,
            pause_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 35)
            )
        )

    

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            NEON_GREEN
        )

        final_score_text = score_font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        record_text = score_font.render(
            f"Best Score: {best_score}",
            True,
            NEON_GREEN
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(center=(WIDTH // 2, 270))
        )

        screen.blit(
            final_score_text,
            final_score_text.get_rect(center=(WIDTH // 2, 320))
        )

        screen.blit(
            record_text,
            record_text.get_rect(center=(WIDTH // 2, 350))
        )

        pygame.draw.rect(
            screen,
            BUTTON_COLOR,
            restart_button,
            border_radius=10
        )

        restart_label = small_font.render(
            "PLAY AGAIN (R)",
            True,
            WHITE
        )

        screen.blit(
            restart_label,
            restart_label.get_rect(center=restart_button.center)
        )

    

    pygame.display.flip()
    clock.tick(10)

pygame.quit()