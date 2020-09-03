import pygame
import random
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

#Game Screen
screen = pygame.display.set_mode((800,600))

#Change the title and image in game winow
pygame.display.set_caption("Pencil Invador")

#FOr background
background =pygame.image.load('background.jpeg')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)
#Player
playerImg =pygame.image.load('mainhero.png')
playerX = 370
playerY = 480
playerXchange = 0

#enemy

enemyImg=[]
enemyX =[]
enemyY = []
enemyXchange  =[]
enemyYchange =[]
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyXchange.append(3)
    enemyYchange.append(40)

#Bullet--hero
bulletImg =pygame.image.load('herobullet.png')
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = 8
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freeansbold.ttf',30)
testX = 10
testY = 10

# Game over score
game_Over = pygame.font.Font('freeansbold.ttf', 60)

def show_score(x,y):



    score = font.render("Score :", True, (244,255,26))
    screen.blit(score, (x, y))
def game_over_text():
    over_text= font.render("Game Over :"+ str(score_value), True, (244,255,26))
    screen.blit(over_text, (200, 250))
def player(x,y):
    screen.blit(playerImg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):

    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))
#distance
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance <27:
        return True
    else:
        return  False


# Game Loop
running = True
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #for palyer movement

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerXchange = -3
        if event.key == pygame.K_RIGHT:
            playerXchange = 3
        if event.key == pygame.K_SPACE:
            if bullet_state=="ready":
                bullet_Sound = mixer.Sound("laser.wav")
                bullet_Sound.play()
                bulletX=playerX
                fire_bullet(bulletX,bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerXchange = 0

    playerX += playerXchange

    if playerX <=0:
        playerX=0
    elif(playerX >=736):
        playerX=736

    #enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyXchange[i]

        if enemyX[i] <= 0:
            enemyXchange[i] = 2
            enemyY[i]+=enemyYchange[i]

        elif (enemyX[i] >= 735):
            enemyXchange[i] = -2
            enemyY[i] += enemyYchange[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)

    # Bullet Movement
    if bulletY <=0:
        bulletY = 480
        bullet_state="ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletYchange



    player (playerX, playerY)

    show_score(testX, testY)
    pygame.display.update()