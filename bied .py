import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird (Enhanced Version)")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)

# Load bird image
bird_img = pygame.image.load("download.jpg")
bird_img = pygame.transform.scale(bird_img, (60, 60))  # Resize bird

# Bird settings
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 20
gravity = 0.5
jump_strength = -6
bird_velocity = 0

# Pipe settings
pipe_width = 60
pipe_gap = 300
pipe_x = WIDTH
pipe_height = random.randint(100, 400)
pipe_speed = 5

# Game variables
score = 0
font = pygame.font.SysFont(None, 48)
button_font = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()

game_active = False

def draw_start_button():
    button_text = button_font.render("Start", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(button_text, button_rect)
    return button_rect

def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, game_active
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(100, 400)
    score = 0
    game_active = True

# Game loop
running = True
while running:
    screen.fill(BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active:
                if draw_start_button().collidepoint(event.pos):
                    reset_game()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_active:
            bird_velocity = jump_strength

    if game_active:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)
            score += 1

        # Collision detection
        if (bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT or
            (pipe_x < bird_x + bird_radius < pipe_x + pipe_width and 
             (bird_y - bird_radius < pipe_height or bird_y + bird_radius > pipe_height + pipe_gap))):
            game_active = False  # End the game on collision

        # Draw pipes
        pygame.draw.rect(screen, GREEN, (pipe_x, 0, pipe_width, pipe_height))
        pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT))

        # Draw bird
        screen.blit(bird_img, (bird_x - bird_radius, bird_y - bird_radius))

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        start_button_rect = draw_start_button()
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()