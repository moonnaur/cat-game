import pygame
import os
import math
import time
from os import listdir
from os.path import isfile, join
pygame.init()


pygame.display.set_caption("Dungeon Fight!!")

# window size
width, height = 1280,780
fps = 60
player_vel = 5
window = pygame.display.set_mode((width,height))

# background image
background = pygame.transform.scale(pygame.image.load("assets\Background\country-platform.png"), (width,height))

# floor
floor_width = width
floor_height = 120
floor_surface = pygame.Surface((floor_width, floor_height), pygame.SRCALPHA)
floor_surface.fill((0, 0, 0, 0))
floor_rect = floor_surface.get_rect()
floor_rect.topleft = (0, height - floor_height)

# function to put images into our window
def draw(player, fireballs):
    window.blit(background, (0,0))

    player.draw(window)
    window.blit(floor_surface, floor_rect)

    for fireball in fireballs:
        window.blit(fireball.image, fireball.rect)

    pygame.display.update()
    
# function to turn character left and right
def flip(sprites):
    return [pygame.transform.flip(sprite,True, False) for sprite in sprites]

# function to load sprite image into window
def load_sprite_sheets(dir1,dir2,width,height,direction = False):
    path = join("assets",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width,height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites
            all_sprites[image.replace(".png","") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites
    
    return all_sprites

# assigning keys on our keyboard to movemnent of character
def movement(player):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(player_vel)
    if keys[pygame.K_d]:
        player.move_right(player_vel)

# class for our player
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    gravity = 1
    SPRITE = load_sprite_sheets("catsprite", "cat1", 20, 50, True)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fallingcounter = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        self.animation_count += 1

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
        self.animation_count += 1

    def jump(self):
        self.y_vel = -self.gravity * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)
        # gravity
        self.y_vel += min(1, (self.fallingcounter / fps) * self.gravity)
        self.fallingcounter += 1

        # Check for collision with the floor
        if self.rect.colliderect(floor_rect):
            # Adjust the player's position if colliding with the floor
            self.rect.y = floor_rect.y - self.rect.height
            self.lande()

    def draw(self, window):
        self.sprite = self.SPRITE["cat_idle_" + self.direction][0]
        window.blit(self.sprite, (self.rect.x, self.rect.y))

    def lande(self):
        self.fallingcounter = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

# class for Fireball
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__() 
        self.image = pygame.image.load("assets/fireball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction  # Direction of the fireball (left or right)
        self.speed = 22  # Speed of the fireball

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        # Remove the fireball if it goes off-screen
        if self.rect.right < 0 or self.rect.left > width:
            self.kill()

def main(window):
    clock = pygame.time.Clock()
    player = Player(width / 2, height - floor_height, 50, 50)
    fireballs = pygame.sprite.Group()

    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # fireball when space is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                 # Create a fireball when the space key is pressed
                    fireball = Fireball(player.rect.centerx, player.rect.centery, player.direction)
                    fireballs.add(fireball)

            
            # jump when w pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player.jump_count < 2:
                    player.jump()

        player.loop(fps)
        movement(player)
        draw(player, fireballs)

        fireballs.update()
        fireballs.draw(window)
        
        window.blit(floor_surface, floor_rect)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main(window)
