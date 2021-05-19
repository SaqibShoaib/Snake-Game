import pygame
pygame.init()
# print(x)
gamewindow = pygame.display.set_mode((1200,500))
pygame.display.set_caption("My First Game")

exit_game = False
game_over = False

while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print("Right arrow key is pressed")
            if event.key == pygame.K_LEFT:
                print("Left arrow key is pressed")
            if event.key == pygame.K_DOWN:
                print("Down arrow key is pressed")
            if event.key == pygame.K_UP:
                print("UP arrow key is pressed")
pygame.quit()
quit()