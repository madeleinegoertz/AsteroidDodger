import sys, pygame, random, pandas as pd
from ship import Ship
from asteroid import Asteroid
import matplotlib.pyplot as plt
import numpy as np
from pygame.locals import *

pygame.init()
screen_info = pygame.display.Info()

# set width and height to half of size of screen
size = (width, height) = (int(screen_info.current_w * 0.5), int(screen_info.current_h * 0.5))

# read in levels
df = pd.read_csv("game_info.csv")

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

SPEED_STEP = 10

# setup game variables
num_levels = df['LevelNum'].max()
level = df['LevelNum'].min()
level_data = df.iloc[level]

asteroid_count = level_data["AsteroidCount"]
player = Ship((level_data["PlayerX"], level_data["PlayerY"]))
asteroids = pygame.sprite.Group()
tries = 0
total_tries = []

color = (level_data["ColorR"], level_data["ColorG"], level_data["ColorB"])
screen.fill(color)


def init():
    global asteroids, asteroid_count, level_data, tries, total_tries
    level_data = df.iloc[level]
    player.reset((level_data["PlayerX"], level_data["PlayerY"]))
    asteroids.empty()
    asteroid_count += level_data["AsteroidCount"]
    for i in range(asteroid_count):
        asteroids.add(
            Asteroid((random.randint(50, width - 50), random.randint(50, height - 50)), random.randint(15, 60)))
    tries = 1
    total_tries.append(tries)


def win():
    font = pygame.font.SysFont(None, 70)
    text = font.render("You Escaped!", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 2)

    index = np.arange(len(total_tries))
    plt.bar(index, total_tries)
    plt.xlabel("Level Num", fontsize=20)
    plt.ylabel("No. of Tries", fontsize=20)
    plt.xticks(index, total_tries, fontsize=20, rotation=5)
    plt.title("Tries per Level")
    plt.show()

    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


def main():
    global level_data, level, color, tries, total_tries
    init()
    while level <= num_levels:
        level_data = df.iloc[level]
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player.speed[1] = -SPEED_STEP
                if event.key == K_DOWN:
                    player.speed[1] = SPEED_STEP
                if event.key == K_LEFT:
                    player.speed[0] = -SPEED_STEP
                if event.key == K_RIGHT:
                    player.speed[0] = SPEED_STEP
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    player.speed[1] = 0
                if event.key == K_LEFT or event.key == K_RIGHT:
                    player.speed[0] = 0
        color = (level_data["ColorR"], level_data["ColorG"], level_data["ColorB"])
        screen.fill(color)
        player.update()
        asteroids.update()
        gets_hit = pygame.sprite.spritecollide(player, asteroids, False)
        asteroids.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.flip()

        if player.check_reset(width):
            total_tries.append(tries)
            if level == num_levels:
                break
            else:
                level += 1
                init()
        elif gets_hit:
            player.reset((level_data["PlayerX"], level_data["PlayerY"]))
            tries += 1
    win()


if __name__ == "__main__":
    main()
