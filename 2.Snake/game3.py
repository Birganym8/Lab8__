import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up screen dimensions and colors
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up clock for controlling frame rate
clock = pygame.time.Clock()

# Set up snake speed and initial values
snake_block = 10
snake_speed = 15  # Speed in pixels per frame
snake_length = 1
snake_position = [[100, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction
score = 0
level = 1

# Font for displaying score and level
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


# Function to draw the snake
def draw_snake(snake_block, snake_position):
    for block in snake_position:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], snake_block, snake_block))


# Function to display score and level
def display_score_level(score, level):
    value = score_font.render("Score: " + str(score), True, BLACK)
    screen.blit(value, [0, 0])

    level_value = font_style.render("Level: " + str(level), True, BLACK)
    screen.blit(level_value, [SCREEN_WIDTH - 120, 0])


# Function to generate food position
def random_food(snake_position):
    food_position = [random.randrange(1, (SCREEN_WIDTH // snake_block)) * snake_block,
                     random.randrange(1, (SCREEN_HEIGHT // snake_block)) * snake_block]

    while food_position in snake_position:  # Avoid food spawning on the snake
        food_position = [random.randrange(1, (SCREEN_WIDTH // snake_block)) * snake_block,
                         random.randrange(1, (SCREEN_HEIGHT // snake_block)) * snake_block]
    
    return food_position


# Game loop function
def gameLoop():
    global score, snake_speed, snake_length, snake_position, snake_direction, change_to, level
    
    game_over = False
    game_close = False

    # Initial snake position
    snake_position = [[100, 50]]
    food_position = random_food(snake_position)
    
    # Main game loop
    while not game_over:
        while game_close:
            screen.fill(WHITE)
            message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
            screen.blit(message, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])
            display_score_level(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Handling key press for controlling snake direction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'

        # If snake moves in opposite direction, make it invalid
        if change_to == 'LEFT' and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        if change_to == 'RIGHT' and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'
        if change_to == 'UP' and snake_direction != 'DOWN':
            snake_direction = 'UP'
        if change_to == 'DOWN' and snake_direction != 'UP':
            snake_direction = 'DOWN'

        # Move the snake in the direction
        if snake_direction == 'LEFT':
            snake_position[0][0] -= snake_block
        if snake_direction == 'RIGHT':
            snake_position[0][0] += snake_block
        if snake_direction == 'UP':
            snake_position[0][1] -= snake_block
        if snake_direction == 'DOWN':
            snake_position[0][1] += snake_block

        # Check for wall collision (snake leaving screen)
        if snake_position[0][0] >= SCREEN_WIDTH or snake_position[0][0] < 0 or snake_position[0][1] >= SCREEN_HEIGHT or snake_position[0][1] < 0:
            game_close = True

        # Snake body growing mechanism
        snake_head = []
        snake_head.append(snake_position[0][0])
        snake_head.append(snake_position[0][1])
        snake_position.insert(0, snake_head)

        # Check if snake collides with itself
        for block in snake_position[1:]:
            if block == snake_head:
                game_close = True

        # Check if snake eats food
        if snake_position[0] == food_position:
            food_position = random_food(snake_position)  # Generate new food
            score += 1
            snake_length += 1  # Increase snake length
            if score % 3 == 0:  # Increase level and speed after 3 foods
                level += 1
                snake_speed += 3  # Increase speed as the level increases

        # Remove the last block of the snake (if snake didn't eat food)
        if len(snake_position) > snake_length:
            del snake_position[-1]

        # Draw everything
        screen.fill(WHITE)
        draw_snake(snake_block, snake_position)
        pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], snake_block, snake_block))

        # Display score and level
        display_score_level(score, level)

        # Update the screen
        pygame.display.update()

        # Control the speed of the snake
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game loop
gameLoop()
