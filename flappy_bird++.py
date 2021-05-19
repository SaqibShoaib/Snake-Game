import random
import sys
import pygame
from pygame.locals import *

# globel variables
FPS =30
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
GROUNDY = SCREEN_HEIGHT*0.8
GAME_SPRITIES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/back.png'
PIPE = 'gallery/sprites/pipe.png'

def WelcomeScreen():
    playerx = int(SCREEN_WIDTH/5)
    playery = int((SCREEN_HEIGHT - GAME_SPRITIES['player'].get_height())/2)
    messagex = int((SCREEN_WIDTH - GAME_SPRITIES['message'].get_width())/2)
    messagey = int(SCREEN_HEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP or event.key == K_RETURN):
                return
            else:
                SCREEN.blit(GAME_SPRITIES['background'],(0,0))
                SCREEN.blit(GAME_SPRITIES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITIES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITIES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_WIDTH/2)
    basex = 0

    newpipe = getRandomPipe()
    newpipe2 = getRandomPipe()

    upperPipe = [
        {'x': SCREEN_WIDTH+200,'y':newpipe[0]['y']},
        {'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2),'y':newpipe2[0]['y']},
    ]
    lowerPipe = [
        {'x': SCREEN_WIDTH+200,'y':newpipe[1]['y']},
        {'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2),'y':newpipe2[1]['y']},
    ]
    pipeVelX = -4
    
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    
    playerFlapAccv = -8
    playerFlapped = False

    # main gameloop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_UP or event.key == K_RETURN or event.key == K_SPACE):
                if playery > 0:
                    playerVelY =  playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isColide(playerx,playery,upperPipe,lowerPipe)
        if crashTest:
            return
        # score updation
        playerMidPos = playerx + GAME_SPRITIES['player'].get_width()/2
        for pipe in upperPipe:
            pipeMidPos = pipe['x'] + GAME_SPRITIES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                GAME_SOUNDS['point'].play()

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False  
        
        playerHeight = GAME_SPRITIES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipes , lowerPipes in zip(upperPipe, lowerPipe):
            upperPipes['x'] += pipeVelX
            lowerPipes['x'] += pipeVelX
        
        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipe[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipe.append(newpipe[0])
            lowerPipe.append(newpipe[1])

        # removing pipe
        if upperPipe[0]['x'] < -GAME_SPRITIES['pipe'][0].get_width():
            upperPipe.pop(0)
            lowerPipe.pop(0)


        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITIES['background'], (0, 0))
        for upperPipes, lowerPipes in zip(upperPipe, lowerPipe):
            SCREEN.blit(GAME_SPRITIES['pipe'][0], (upperPipes['x'], upperPipes['y']))
            SCREEN.blit(GAME_SPRITIES['pipe'][1], (lowerPipes['x'], lowerPipes['y']))
        SCREEN.blit(GAME_SPRITIES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITIES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITIES['numbers'][digit].get_width()
        Xoffset = (SCREEN_WIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITIES['numbers'][digit], (Xoffset, SCREEN_HEIGHT*0.12))
            Xoffset += GAME_SPRITIES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isColide(playerx,playery,upperPipe,lowerPipe):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipe:
        pipeHeight = GAME_SPRITIES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITIES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipe:
        if (playery + GAME_SPRITIES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITIES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False
def getRandomPipe():
    pipeHeight = GAME_SPRITIES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT/3
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - GAME_SPRITIES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird++")
    GAME_SPRITIES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITIES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITIES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITIES['pipe'] =(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), 
        pygame.image.load(PIPE).convert_alpha()
    )
    
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


    GAME_SPRITIES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITIES['player'] = pygame.image.load(PLAYER).convert_alpha()
    while True:
        WelcomeScreen()
        mainGame()
