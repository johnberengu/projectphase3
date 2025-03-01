import pygame
import os

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def load_images(folder):
    return [pygame.image.load(os.path.join(folder, img)) for img in sorted(os.listdir(folder)) if img.endswith(".png")]

idle_left_frames = load_images("/home/eli/projects/project_phase_3/idleleft")
idle_right_frames = load_images("/home/eli/projects/project_phase_3/idleright")
walk_right_frames = load_images("/home/eli/projects/project_phase_3/moveright")
walk_left_frames = load_images("/home/eli/projects/project_phase_3/moveleft")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = idle_right_frames[0]  
        self.rect = self.image.get_rect(topleft=(300, 250))


        self.frame_index = 0
        self.animation_speed = 10  
        self.counter = 0  


        self.speed = 3
        self.direction = "idleright"  


    def update(self):
        keys = pygame.key.get_pressed()
        moving = False


        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
            moving = True
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = "up"
            moving = True
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = "down"
            moving = True


        #switch to idle if not moving
        if not moving:
            if self.direction in ["left", "idleleft"]:
                self.direction = "idleleft"
            elif self.direction in ["right", "idleright"]:
                self.direction = "idleright"


        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.get_animation_frames())

        self.image = self.get_animation_frames()[self.frame_index]


    def get_animation_frames(self):
        """Returns the correct frame list based on movement direction."""
        if self.direction == "left":
            return walk_left_frames
        elif self.direction == "right":
            return walk_right_frames
        elif self.direction == "idleleft":
            return idle_left_frames
        elif self.direction == "idleright":
            return idle_right_frames
        return idle_right_frames 
    
    
player = Player()
all_sprites = pygame.sprite.Group(player)

run = True
clock = pygame.time.Clock()


while run:
    clock.tick(60)  #limit to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()

    screen.fill((0, 0, 0))  #clear screen

    all_sprites.draw(screen)  
    pygame.display.update() 


pygame.quit()
