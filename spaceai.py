# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 17:00:55 2020

@author: prudh
"""

import pygame
import random
import math
import os
import neat
from pygame import mixer
import time
import visualize
import pickle
import threading



#Initializing pygame
pygame.init()

#initializing the screen
screen = pygame.display.set_mode((800,600))

#Titile & Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',45)

textX = 300
textY = 20

game_over = pygame.font.Font('freesansbold.ttf',65)

def display_font(x,y):
    score = font.render("Score:" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
    
def display_gameover():
    over = game_over.render("Game Over",True,(255,255,255))
    screen.blit(over,(250,280))

#Background
background = pygame.image.load("background.png")

#Background sound
#mixer.music.load("background.wav")
#mixer.music.play(-1)

#player
playerimg = pygame.image.load("space-invaders.png")
playerimg = pygame.transform.scale(playerimg, (45, 45))

playerX = 350
playerY = 500
playerX_change = 0

def player(x,y):
    screen.blit(playerimg,(x,y))
    
#Enemy
enemyimg = []
enemyimgT =  []    
enemyX  = []
enemyY  = []
enemyX_change  = []
enemyY_change  = []

for i in range(0,6):
    enemyimg.append(pygame.image.load("alien.png"))
    enemyimgT.append(pygame.transform.scale(enemyimg[i], (45, 45)))
    enemyX.append(random.randint(0,755))
    enemyY.append(random.randint(50,200))
    enemyX_change.append(4)
    enemyY_change.append(45)

def enemy(x,y,i):
    screen.blit(enemyimgT[i],(x,y))
    

#Bullet
bulletimg = pygame.image.load("bullet.png")
bulletimg = pygame.transform.scale(bulletimg, (35, 35))

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg,(x+5,y+16))
    
    
def Collusion(aX,aY,bX,bY):
    distance = math.sqrt(math.pow((aX-bX),2)+math.pow((aY-bY),2))
    if distance <= 25:
        return True
    else:
        return False
    
def run(config_file):
    
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
     # Run for up to 300 generations.
    winner = p.run(eval_genomes, 100)

if __name__ == '__main__':

    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)


def printit():
  threading.Timer(1.0, printit).start()
  genomes.fitness += 0.5


def eval_genomes(genomes, config):
    
    net = neat.nn.FeedForwardNetwork.create(genomes, config)
    genmoes.fitness = 0
    


    while True:
        
        #increase fitness 0.5 every sec
        printit()
        
        screen.fill((0,0,0))
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)
                        mixer.music.load("laser.wav")
                        mixer.music.play()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
        
                    
        #Player Boundry & Movement
        
        if playerX <= 0:
            playerX = 0
        elif playerX >= 750:
            playerX = 750
            
        playerX += playerX_change
        
           #Neural net
        output = net.activate((playerX,math.sqrt(math.pow((enemyX[0]-playerX[0]),2)+math.pow((enemyY[0]-playerY[0]),2))))
        
        if output >0.5:
            if bullet_state is "ready":
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
                mixer.music.load("laser.wav")
                mixer.music.play()
        
        #Bullet Movement
        if bullet_state is "fire":
            fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change
        
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = 480
        
        #Enemy Boundary & Movement
        
        for i in range(0,6):
            
            if enemyY[i]>=480:
                for j in range(0,6):
                    enemyY[j]= 2000
                display_gameover()
                break            
                
            enemyX[i] += enemyX_change[i] 
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 750:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[0]
            
            colide = Collusion(enemyX[i],enemyY[i],bulletX,bulletY)
            
            enemy(enemyX[i],enemyY[i],i)
        
            if colide:
                bullet_state = "ready"
                bulletY = 480
                enemyX[i] = random.randint(0,755)
                enemyY[i]= random.randint(50,200)
                score_value +=1
                genome.fitness +=3
                mixer.music.load("explosion.wav")
                mixer.music.play()
            
    
        display_font(textX,textY)
        player(playerX,playerY)       
        pygame.display.update()
