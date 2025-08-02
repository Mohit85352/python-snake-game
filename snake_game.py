import pygame
import random
import os

# Initialize
pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

# Screen
screen_width = 700
screen_height = 500
game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("🔥 Mohit's Snake Game Advanced")
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 30)

# Sound
eat_sound = pygame.mixer.Sound('eat.wav')
gameover_sound = pygame.mixer.Sound('gameover.wav')

# Text on screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])

# Draw Snake
def plot_snake(window, color, snk_list, size):
    for x, y in snk_list:
        pygame.draw.rect(window, color, [x, y, size, size])

# Welcome screen
def welcome():
    exit_game = False
    while not exit_game:
        game_window.fill(white)
        text_screen("Welcome to Snake Game!", black, 180, 200)
        text_screen("Press SPACE to Start", green, 210, 250)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_loop()

# Main Game
def game_loop():
    # Variables
    snake_x = 100
    snake_y = 100
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)

    score = 0
    init_velocity = 5
    velocity = init_velocity
    snake_size = 20
    fps = 30

    # High Score
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    game_over = False
    exit_game = False

    while not exit_game:
        if game_over:
            game_window.fill(white)
            text_screen("Game Over! Press Enter to Restart", red, 150, 200)
            text_screen(f"Your Score: {score}  High Score: {highscore}", black, 200, 250)
            pygame.display.update()
            pygame.mixer.Sound.play(gameover_sound)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_loop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Eating food
            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                pygame.mixer.Sound.play(eat_sound)
                score += 10
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_length += 5
                velocity += 0.2  # Increase difficulty

                if score > highscore:
                    highscore = score

            game_window.fill(white)
            text_screen(f"Score: {score}  High Score: {highscore}", black, 5, 5)
            pygame.draw.rect(game_window, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1] or snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                with open("highscore.txt", "w") as f:
                    f.write(str(highscore))

            plot_snake(game_window, black, snk_list, snake_size)
            pygame.display.update()
            clock.tick(fps)

    pygame.quit()
    quit()

# Start
welcome()
