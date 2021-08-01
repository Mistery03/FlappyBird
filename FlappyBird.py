import pygame;
import sys;
import os;
import random;

pygame.init();
pygame.font.init();
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512);

#CONSTANT MEASUREMENT
WIDTH, HEIGHT = 576, 690;

screen = pygame.display.set_mode((WIDTH,HEIGHT));
pygame.display.set_caption("Flappy Bird");

#Load images
#Background Surface Images
BGImg = pygame.image.load(os.path.join("sprites","background-day.png"));
floorImg = pygame.image.load(os.path.join("sprites","base.png"));
pipeImg = pygame.image.load(os.path.join("sprites","pipe-green.png"));

#misc images
gameOverImg = pygame.image.load(os.path.join("sprites","message.png"));

#Player image
birdDownFlapImg = pygame.image.load(os.path.join("sprites","bluebird-downflap.png"));
birdMidFlapImg = pygame.image.load(os.path.join("sprites","bluebird-midflap.png"));
birdUpFlapImg = pygame.image.load(os.path.join("sprites","bluebird-upflap.png"));

#scales Images (Main Code)
BG = pygame.transform.scale(BGImg,(WIDTH,HEIGHT));
floor = pygame.transform.scale(floorImg,(WIDTH,200));
pipeS = pygame.transform.scale2x(pipeImg);
gameOver = pygame.transform.scale(gameOverImg,(int(WIDTH/2),330));

birdDownFlap = pygame.transform.scale2x(birdDownFlapImg);
birdMidFlap = pygame.transform.scale2x(birdMidFlapImg);
birdUpFlap = pygame.transform.scale2x(birdUpFlapImg);

#Birb animation
birdIndex = 0;
birdFrames =[birdDownFlap,birdMidFlap,birdUpFlap];
bird = birdFrames[birdIndex];

#Collision shape
birdRect = bird.get_rect(center =(100,HEIGHT/2));

BIRDFLAP = pygame.USEREVENT + 1;
pygame.time.set_timer(BIRDFLAP,200);

SPAWNPIPE = pygame.USEREVENT;
pygame.time.set_timer(SPAWNPIPE,1200);

gameOverRect = gameOver.get_rect(center = (WIDTH/2, HEIGHT/2))

#Sound
flapSound = pygame.mixer.Sound(os.path.join("audio","wing.wav"));
deathSound = pygame.mixer.Sound(os.path.join("audio","die.wav"));
scoreSound = pygame.mixer.Sound(os.path.join("audio","point.wav"));
scoreSoundCountdown = 100;


def updateScore(score,highScore):
    if score > highScore:
        highScore = score;
    return highScore;

def scoreDisplay(gameState):
    if gameState =="mainGame":
        scoreSurface = gameFont.render(str(int(score)),True,(255,255,255));
        scoreRect = scoreSurface.get_rect(center = (WIDTH/2,50));
        screen.blit(scoreSurface,scoreRect);
    if gameState == "gameOver":
        scoreSurface = gameFont.render(f"Score: {int(score)}",True,(255,255,255));
        scoreRect = scoreSurface.get_rect(center = (WIDTH/2,50));
        screen.blit(scoreSurface,scoreRect);

        highscoreSurface = gameFont.render(f"Highscore: {int(highscore)}",True,(255,255,255));
        highscoreRect = highscoreSurface.get_rect(center = (WIDTH/2,550));
        screen.blit(highscoreSurface,highscoreRect);

def birdAnimation():
    newBird = birdFrames[birdIndex];
    newBirdRect = newBird.get_rect(center = (100,birdRect.centery))
    return newBird, newBirdRect;

def rotateBird(birb,mov):
    newBird = pygame.transform.rotozoom(birb,-mov*3,1);
    return newBird;

def checkCollision(pipes):
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play();
            return False;

        if birdRect.top <= -100 or birdRect.bottom >= HEIGHT:
            return False;
        
    return True;

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 660:
            screen.blit(pipeS,pipe);
        else:
            flipPipe = pygame.transform.flip(pipeS,False,True);
            screen.blit(flipPipe,pipe);

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5;
    return pipes;

def createPipe(ranHeight):
    randomPipePos = random.choice(ranHeight)
    botNewPipe = pipeS.get_rect(midtop = (700,randomPipePos));
    topNewPipe = pipeS.get_rect(midbottom = (700,randomPipePos - 200));
    return botNewPipe, topNewPipe;

def drawFloor(x):
    screen.blit(floor,(x,580));
    screen.blit(floor,(x+WIDTH,580));


clock = pygame.time.Clock();
gameFont = pygame.font.Font("04b_19.ttf",40);

#Game Variables
gravity = 0.15;
birdMov = 0;
pipeList = [];
pipeHeight = [300,400,500];
runGame = True;
alive = True;
FPS = 120;
score = 0;
highscore = 0;

floorXPos = 0;

while runGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            exit();
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and alive:
                birdMov = 0;
                birdMov -= 5;
                flapSound.play();
            if event.key == pygame.K_SPACE and alive == False:
                alive = True;
                pipeList.clear();
                birdRect.center = (100,HEIGHT/2);
                birdMov =0;
                score = 0;
            
        if event.type == SPAWNPIPE:
            pipeList.extend(createPipe(pipeHeight));
            print(pipeList);

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1;
            else:
                birdIndex = 0;

            bird,birdRect = birdAnimation();
                
            
    screen.blit(BG,(0,0));

    if alive:
        #birb
        birdMov += gravity;
        rotatedBird = rotateBird(bird,birdMov);
        birdRect.centery += birdMov;
        screen.blit(rotatedBird,(birdRect));
        alive = checkCollision(pipeList);

        #pipes
        pipeList = movePipes(pipeList);
        drawPipes(pipeList);

        score += 0.01;
        scoreDisplay("mainGame");
        scoreSoundCountdown -= 1;
        if scoreSoundCountdown <= 0:
            scoreSound.play();
            scoreSoundCountdown = 100;
    else:
        screen.blit(gameOver,gameOverRect);
        highscore = updateScore(score,highscore);
        scoreDisplay("gameOver");
        

    #floor
    floorXPos -= 1;
    drawFloor(floorXPos);
    if floorXPos <= -WIDTH:
        floorXPos = 0;
    
    
    pygame.display.update();
    clock.tick(FPS);

