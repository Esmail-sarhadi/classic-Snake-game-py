import pygame
import sys
import time
import random

# Difficulty settings
difficulty = 22  # Medium

# Window size
frame_size_x = 1024
frame_size_y = 1024

# Checks for errors encountered
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)



# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
def initialize_game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

initialize_game()

# Game Over
def game_over():
    global score
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times new roman', 20)
    pygame.display.flip()
    time.sleep(3)
    initialize_game()  # Reset game variables
    game_menu()  # Back to menu after game over

# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

# Menu
def game_menu():
    menu_font = pygame.font.SysFont('times new roman', 30)
    options = ['Run Game', 'Exit']
    selected_option = 0
    

    while True:
        game_window.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return  # Start game
                    elif selected_option == 1:
                        pygame.quit()
                        sys.exit()

        for idx, option in enumerate(options):
            if idx == selected_option:
                text = menu_font.render(option, True, red)
            else:
                text = menu_font.render(option, True, white)
            text_rect = text.get_rect(center=(frame_size_x // 2, frame_size_y // 2 + idx * 40))
            game_window.blit(text, text_rect)

        pygame.display.update()
        fps_controller.tick(10)  # Adjust FPS for menu

# Main game loop
def main():
    global direction, change_to, snake_pos, food_pos, food_spawn, score, snake_body


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10


        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        game_window.fill(black)
        pygame.draw.rect(game_window, blue, pygame.Rect(0, 0, frame_size_x, 10))  # Top
        pygame.draw.rect(game_window, blue, pygame.Rect(0, 0, 10, frame_size_y))  # Left
        pygame.draw.rect(game_window, blue, pygame.Rect(0, frame_size_y - 10, frame_size_x, 10))  # Bottom
        pygame.draw.rect(game_window, blue, pygame.Rect(frame_size_x - 10, 0, 10, frame_size_y))  # Right

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 10 or snake_pos[0] > frame_size_x - 20:
            game_over()
        if snake_pos[1] < 10 or snake_pos[1] > frame_size_y - 20:
            game_over()
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()



        show_score(1, white, 'consolas', 20)
        pygame.display.update()
        fps_controller.tick(difficulty)

if __name__ == '__main__':
    game_menu()  # start the game with the menu
    main()  # start the Main game loop
