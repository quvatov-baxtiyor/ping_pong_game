import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 10
PAD_WIDTH, PAD_HEIGHT = 10, 80
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Initialize clock
clock = pygame.time.Clock()

# Initialize game variables
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [4, 4]
paddle1_pos = HEIGHT // 2 - PAD_HEIGHT // 2
paddle2_pos = HEIGHT // 2 - PAD_HEIGHT // 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
goal_limit = 5  # New: Set the goal limit

# Function to respawn the ball
def reset_ball():
    return [WIDTH // 2, HEIGHT // 2], [4 * random.choice([-1, 1]), 4 * random.choice([-1, 1])]

# Main game loop
while True:
    ball_color = WHITE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1_vel = -4
            elif event.key == pygame.K_s:
                paddle1_vel = 4
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                paddle1_vel = 0

    # Move paddles
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    # AI opponent
    if ball_pos[1] < paddle2_pos + PAD_HEIGHT // 2:
        paddle2_vel = -4
    elif ball_pos[1] > paddle2_pos + PAD_HEIGHT // 2:
        paddle2_vel = 4
    else:
        paddle2_vel = 0

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Ball collisions
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # Paddle collisions
    if (
        ball_pos[0] - BALL_RADIUS <= PAD_WIDTH
        and paddle1_pos <= ball_pos[1] <= paddle1_pos + PAD_HEIGHT
    ):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] += ball_vel[0] // 10
        ball_vel[1] += ball_vel[1] // 10
        ball_color = RED  # New: Change ball color to red
    elif (
        ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH
        and paddle2_pos <= ball_pos[1] <= paddle2_pos + PAD_HEIGHT
    ):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] += ball_vel[0] // 10
        ball_vel[1] += ball_vel[1] // 10
        ball_color = GREEN  # New: Change ball color to green
    elif ball_pos[0] - BALL_RADIUS <= 0 or ball_pos[0] + BALL_RADIUS >= WIDTH:
        # Score
        if ball_pos[0] - BALL_RADIUS <= 0:
            score2 += 1
        else:
            score1 += 1

        # New: Change ball color to white
        ball_color = WHITE

        # Respawn ball
        ball_pos, ball_vel = reset_ball()

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (PAD_WIDTH, paddle1_pos, PAD_WIDTH, PAD_HEIGHT))
    pygame.draw.rect(
        screen, WHITE, (WIDTH - 2 * PAD_WIDTH, paddle2_pos, PAD_WIDTH, PAD_HEIGHT)
    )
    pygame.draw.circle(screen, ball_color, (ball_pos[0], ball_pos[1]), BALL_RADIUS)

    # Draw scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 30, 10))

    # New: Check for winner
    if score1 == goal_limit or score2 == goal_limit:
        winner_text = font.render("User Win!" if score1 == goal_limit else "Computer Win!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds
        pygame.quit()
        sys.exit()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
