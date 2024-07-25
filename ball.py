# GitHub: Kyle8973
# TikTok Inspired Bouncing Ball Game

# Imports
import pygame # type: ignore
import sys
import random

# Initialize Pygame
pygame.init()

# Set Screen Dimensions
WIDTH, HEIGHT = 800, 600  # Variable For The Width And Height
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Uses Above Variable To Set Width And Height
pygame.display.set_caption("Kyle's Bouncing Ball Game")  # Game Title

# Define Colors
BLACK = (0, 0, 0)  # Black, Background Color
WHITE = (255, 255, 255)  # White, Circle Color
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]  # Ball Color

# Circle Variables
circle_center = (WIDTH // 2, HEIGHT // 2)  # Set The Center Of The Circle
circle_radius = 250  # Set The Radius Of The Circle (Size)

# Ball Variables
ball_radius = 20  # Set The Radius (Size) Of The Ball When Starting The Game
ball_pos = [WIDTH // 2, HEIGHT // 2]  # Set The Ball Position
ball_velocity = [random.choice([-5, 5]), random.choice([-5, 5])]  # Initializes The Ball Velocity With Random Values
ball_color = random.choice(colors)  # Uses The 'Random' Function To Assign A Random Ball Color
speed_increase = 1.015  # Increases Ball Speed (By 1.015x) Every time There Is A Collision

# This Resets The Game If The User Opts To Play Again
def reset_game():
    global ball_radius, ball_pos, ball_velocity, ball_color, bounce_count
    ball_radius = 20
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_velocity = [random.choice([-5, 5]), random.choice([-5, 5])]
    ball_color = random.choice(colors)
    bounce_count = 0

# Warning Screen
def display_initial_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Warning!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    message = pygame.font.Font(None, 36).render("This Game Contains Flashing Images, Do You Want To Continue?", True, WHITE)
    credit = pygame.font.Font(None, 36).render("GitHub: Kyle8973", True, WHITE)  # Credit Text
    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    credit_rect = credit.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))  # Position Credit Text
    yes_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 80, 50)
    no_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 10, 80, 50)

    while True:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        screen.blit(message, message_rect) # Display Message Text
        screen.blit(credit, credit_rect)  # Display Credit Text
        pygame.draw.rect(screen, WHITE, yes_button)
        pygame.draw.rect(screen, WHITE, no_button)

        yes_text = pygame.font.Font(None, 50).render("Yes", True, BLACK)
        no_text = pygame.font.Font(None, 50).render("No", True, BLACK)
        screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))
        screen.blit(no_text, no_text.get_rect(center=no_button.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return  # Start Game
                elif no_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# When The Game Ends This Displays A Prompt Asking The User If They Want To Go Again
def display_end_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Play Again?", True, WHITE)  # Title Text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    yes_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 80, 50)
    no_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 10, 80, 50)

    while True:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, WHITE, yes_button)  # Draws Rectangle For Button
        pygame.draw.rect(screen, WHITE, no_button)  # Draws Rectangle For Button

        yes_text = pygame.font.Font(None, 50).render("Yes", True, BLACK)  # Yes Button
        no_text = pygame.font.Font(None, 50).render("No", True, BLACK)  # No Button
        screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))
        screen.blit(no_text, no_text.get_rect(center=no_button.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):  # If 'Yes' Button Is Pressed
                    reset_game()  # Then Reset Game And Go Again
                    return
                elif no_button.collidepoint(event.pos):  # If 'No' Button Is Pressed
                    pygame.quit()  # Then Exit Game
                    sys.exit()

# Display Warning Screen
display_initial_screen()

# Initialize Bounce Count
bounce_count = 0

# Calculate Max Ball Radius
max_ball_radius = circle_radius - 10

# Loop The Game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ball Movement
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Check for collision with the circle boundary and reflect the velocity
    dist_x = ball_pos[0] - circle_center[0]
    dist_y = ball_pos[1] - circle_center[1]
    distance = (dist_x**2 + dist_y**2)**0.5

    if distance + ball_radius >= circle_radius:
        # Normalize Distance Vector
        normal = [dist_x / distance, dist_y / distance]

        # Calculate Dot Product
        velocity_dot_normal = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]

        # Reflect Ball Velocity Vector
        ball_velocity[0] -= 2 * velocity_dot_normal * normal[0]
        ball_velocity[1] -= 2 * velocity_dot_normal * normal[1]

        # Add Small Random Perturbation To Avoid Repetitive Bounces
        ball_velocity[0] += random.uniform(-1, 2)
        ball_velocity[1] += random.uniform(-1, 2)

        # Increase The Speed Of The Ball
        ball_velocity[0] *= speed_increase
        ball_velocity[1] *= speed_increase

        # Increase Radius Of Ball
        if ball_radius < max_ball_radius:
            ball_radius += 1
            ball_color = random.choice(colors)

        # Set Position To Ensure Ball Stays In The Circle
        ball_pos[0] = circle_center[0] + (circle_radius - ball_radius) * normal[0]
        ball_pos[1] = circle_center[1] + (circle_radius - ball_radius) * normal[1]

        # Increment bounce count
        bounce_count += 1

    # Check If Circle Has Been Filled
    if ball_radius >= max_ball_radius:
        display_end_screen()  # If It Has Then Show End Screen

    # Clear Screen
    screen.fill(BLACK)  # Clears By Filling Screen Black

    # Draw Circle Perimeter
    pygame.draw.circle(screen, WHITE, circle_center, circle_radius, 2)

    # Draw The Ball
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Display Bounce Count
    font = pygame.font.Font(None, 36)
    text = font.render(f"Bounces: {bounce_count}", True, WHITE)
    screen.blit(text, (10, 10))

    # Credits
    font = pygame.font.Font(None, 36)
    text = font.render(f"GitHub: Kyle8973", True, WHITE)
    screen.blit(text, (580, 10))

    # Update Display
    pygame.display.flip()

    # Set Frame Rate
    pygame.time.Clock().tick(60)  # Currently 60 FPS

# Outside Main Loop
pygame.quit()
sys.exit()  # Exit Game
