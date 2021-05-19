import pygame
import random
pygame.init()

GAME_SOUNDS = {}

# colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)
# screen size and color
screen_width = 600
screen_height = 600
gameWindow = pygame.display.set_mode((screen_height,screen_width))
# name of game
pygame.display.set_caption("Snake++")
# screen color
pygame.display.update()
# text function
def text_score(text,color,x,y,size):
    font = pygame.font.SysFont(None,size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# game variables
def game_loop():
# game variables
    snk_list = []
    snk_length = 1
    snake_x = 45
    snake_y = 45
    snake_size = 10
    velocity_x = 0
    velocity_y = 5
    init_velocity = 10
    food_x = random.randint(30,500)
    food_y = random.randint(30,500)
    clock = pygame.time.Clock()
    fps = 30
    score = 0
    exit_game = False
    game_over = False
    die = pygame.mixer.Sound('gallery/audio/die.wav')
    hit = pygame.mixer.Sound('gallery/audio/point.wav')
    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            text_score("Game Over! Press Enter To Continue", red, 100, 250,35)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if velocity_x == 0:
                            velocity_x = init_velocity
                            velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        if velocity_x == 0:
                            velocity_x = -init_velocity
                            velocity_y = 0
                    if event.key == pygame.K_UP:
                        if velocity_y == 0:
                            velocity_y = -init_velocity
                            velocity_x =0
                    if event.key == pygame.K_DOWN:
                        if velocity_y == 0:
                            velocity_y = init_velocity
                            velocity_x = 0
            
            snake_x+=velocity_x
            snake_y+=velocity_y
            if snake_x<0 or snake_x>590 or snake_y<0 or snake_y>590:
                    die.play()
                    game_over = True 
            if abs(snake_x-food_x) < 10 and abs(snake_y - food_y) < 10:
                score+=1
                hit.play()
                food_x = random.randint(30,500)
                food_y = random.randint(30,500)
                snk_length +=5
            
            
            gameWindow.fill(white)
            text_score("Score : "+str(score*10),blue,5,5,20)
            # pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size],0,50)
            pygame.draw.rect(gameWindow,red,[food_x,food_y,10,10])
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if head in snk_list[:-1]:
                game_over = True
            if len(snk_list)>snk_length:
                del snk_list[0]
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
game_loop()
quit()    