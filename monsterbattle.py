import pygame
import os

from life import HealthBar, setup_health, update_health, draw_health_bars

# initialize the game object
pygame.init()

# defines the color of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def load_images(folder, size=(50, 50)):

    try:
        images = [pygame.transform.scale(pygame.image.load(os.path.join(folder, img)).convert_alpha(), size)
                  for img in sorted(os.listdir(folder)) if img.endswith(".png")]
        
        if not images:
            print(f" No images found in {folder}. using fallback images.")
            images = [pygame.Surface(size)]
        print(f" Loaded {len(images)} images from {folder}")
        return images
    except Exception as e:
        print(f" Error loading images from {folder}: {e}")
        return [pygame.Surface(size)]

idle_left_frames = load_images("playeridleleft")
idle_right_frames = load_images("playeridleright")
walk_right_frames = load_images("playerwalkright")
walk_left_frames = load_images("playerwalkleft")
shoot_right_frames = load_images("playershootright")
shoot_left_frames = load_images("playershootleft")


zombie_walk_right = load_images("zombiewalkright")
zombie_walk_left = load_images("zombiewalkleft")
zombie_attack_right = load_images("zombieattackright")
zombie_attack_left = load_images("zombieattackleft")


def load_texture(image_path, colorkey=(0, 255, 0)):
    try:
        image = pygame.image.load(image_path).convert_alpha()
        image.set_colorkey(colorkey)

        return image
    
    except Exception as e:
        print(f"error loading texture : {e}")
        return pygame.Surface((50, 50))

texture = load_texture("P3.png")

def draw_textured_rectangle(surface, texture, rect):
    # draw the textured rect
    scaled_texture = pygame.transform.scale(texture, (rect.width, rect.height))
    surface.blit(scaled_texture, rect.topleft)

obstacles = [
    pygame.Rect(SCREEN_WIDTH - 710, 10, 900, 200),
    pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 300, 600, 50),
    pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 150, 800, 150)
]


class Player(pygame.sprite.Sprite):
    # players class initialization
    def __init__(self):

        super().__init__()

        self.name = "eli" 
        self.image = idle_right_frames[0]
        self.rect = self.image.get_rect(topleft=(300, 250))
        self.frame_index = 0
        self.animation_speed = 10 
        self.counter = 0  
        self.speed = 6
        self.direction = "idleright"
        self.shooting = False
        self.moving = False
        self.health_bar = HealthBar(self)
        self.kills = 0

    # Settin g the direction of the player
    def update(self):
        keys = pygame.key.get_pressed()
        self.moving = False
        dx, dy = 0, 0  

         # a = to go left
        if keys[pygame.K_a] and self.rect.left > 0:  
            dx = -self.speed
            self.direction = "left"
            self.moving = True

        # d = to go right
        elif keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:  
            dx = self.speed
            self.direction = "right"
            self.moving = True

        # w = to go up
        if keys[pygame.K_w] and self.rect.top > 0:  
            dy = -self.speed
            self.moving = True

            # s = to go down
        elif keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:  
            dy = self.speed
            self.moving = True

        # l = to shoot
        self.shooting = keys[pygame.K_l]

        new_rect = self.rect.move(dx, dy)
        if not any(new_rect.colliderect(ob) for ob in obstacles):  
            self.rect = new_rect


        self.counter += 1
        frames = self.get_animation_frames()

        if not frames:
            print("no frames found, using default image")
            self.image = pygame.Surface((50, 50))  
            return  

        self.frame_index %= len(frames)

        if self.counter >= self.animation_speed:
            self.counter = 0
            self.frame_index = (self.frame_index + 1) % len(frames)


        self.image = frames[self.frame_index]

    def get_animation_frames(self):
        if self.shooting:
            return shoot_left_frames if self.direction == "left" else shoot_right_frames
        elif self.moving:
            return walk_left_frames if self.direction == "left" else walk_right_frames
        else:
            return idle_left_frames if self.direction == "left" else idle_right_frames  

    def shoot(self, zombies):

        if not zombies:
            return False

        # determine the direction the player is phasing
        facing_right = self.direction == "right"

        # Filter zombies based on shooting direction and Y-coordinate match
        if facing_right:
            target_zombies = [z for z in zombies if z.rect.centerx > self.rect.centerx and abs(z.rect.centery - self.rect.centery) < 30]
        else:
            target_zombies = [z for z in zombies if z.rect.centerx < self.rect.centerx and abs(z.rect.centery - self.rect.centery) < 30]


        if target_zombies:
            # Sort target zombies by X-coordinate to find the closest one in the direction of the shot
            target_zombies.sort(key=lambda z: z.rect.centerx, reverse=facing_right)


            closest_zombie = target_zombies[0]

            # Reduce the health of the closest zombie
            closest_zombie.health_bar.health -= 1
            print(f"Shot zombie at {closest_zombie.rect.topleft}, health: {closest_zombie.health_bar.health}")

            # Remove zombie if health reaches 0
            

        return False

class Zombie(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = zombie_walk_right[0]  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.animation_speed = 15
        self.counter = 0
        self.speed = 1.2 
        self.attacking = False 
        self.health_bar = HealthBar(self)
        self.spawn_time = pygame.time.get_ticks()


    def update(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        distance = abs(dx) + abs(dy)


        if distance < 30:  # the zombie start attacking when it is close enough
            self.attacking = True
            frames = zombie_attack_left if dx < 0 else zombie_attack_right


            # applies damage to the player when zombie attacks
            if self.attacking:
                player.health_bar.take_damage(1)  # Reduce player's health by 1 when attacked
                print(f"Player hit! Player's health: {player.health_bar.health}")


        else:
            self.attacking = False
            # check if player is attacking
            move_x = self.speed if dx > 0 else -self.speed if dx < 0 else 0
            move_y = self.speed if dy > 0 else -self.speed if dy < 0 else 0

            new_rect_x = self.rect.move(move_x, 0)
            new_rect_y = self.rect.move(0, move_y)


            if any(new_rect_x.colliderect(ob) for ob in obstacles):
                move_x = 0
                if not any(new_rect_y.colliderect(ob) for ob in obstacles):
                    self.rect.y += move_y

        
            elif any(new_rect_y.colliderect(ob) for ob in obstacles):
                move_y = 0
                if not any(new_rect_x.colliderect(ob) for ob in obstacles):
                    self.rect.x += move_x

            else:
                self.rect.x += move_x
                self.rect.y += move_y


            # updates animation frames
            frames = zombie_walk_left if dx < 0 else zombie_walk_right

        if not frames:
            print("no frames found, using default")
            self.image = pygame.Surface((50, 50))  # if no images are available use default images
            return


        self.counter += 1 # counter
        self.frame_index %= len(frames) #number of frames to process per frame


        if self.counter >= self.animation_speed:
            self.counter = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        self.image = frames[self.frame_index]

        # Checks of zombie health is 0 and if true it is removed
        if self.health_bar.health <= 0:
            print(f"Zombie at {self.rect.topleft} died.")
            all_sprites.remove(self)  
            zombies.remove(self)      

player = Player()
zombies = [Zombie(0, 0)]
zombies_killed = 0
zombie_spawn_time = 0
delayed_zombies = []

setup_health(player, zombies[0])


all_sprites = pygame.sprite.Group(player, zombies)


run = True
clock = pygame.time.Clock()

def display_game_over(player_name, player_kills, zombies_killed, screen):
    font = pygame.font.SysFont(None, 55)  # define font size
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # text color for game over red
    kills_text = font.render(f"Zombies Killed: {zombies_killed}", True, (255, 255, 255))  # text color for kills white
    player_name_text = font.render(f"Player: {player_name}", True, (255, 255, 255))

    # make the text to apper at the center
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    player_name_rect = player_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))


    screen.fill((0, 0, 0))  # places a black background
    screen.blit(game_over_text, game_over_rect)
    screen.blit(kills_text, kills_rect)
    screen.blit(player_name_text, player_name_rect)



    pygame.display.update()  # updates the game over screen
    pygame.time.wait(4000)  # Wait for 4 second and then close game


# game loop starts here
while run:
    clock.tick(60) # timer for game loop to start
    
    zombie_killed = False  # initialize the zombie_killed to false

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit the game
            run = False

    player.update()

    if player.shooting:
        zombie_killed = player.shoot(zombies)

    if zombie_killed:
        zombies_killed += 1

    for zombie in zombies:
        zombie.update(player)

    update_health(player, zombies)

    if player.health_bar.health <= 0:
        display_game_over(player.name, player.kills, zombies_killed, screen) 
        run = False


    if len(zombies) < 1:
        zombies_killed += 1  
        print(f"Zombies killed: {zombies_killed}") # shows the number of zombies killed

        if zombies_killed < 2:
            zombies.append(Zombie(0, 0))
        

        elif zombies_killed < 4:
            zombies.append(Zombie(0, 0))
            zombies.append(Zombie(0, SCREEN_HEIGHT - 50))
        

        else:  # after killing 4 zombies spawn 4 and delay new ones
            zombie_spawn_time = pygame.time.get_ticks()  # Get current time

            # spawn first batch imidiatly
            zombies.append(Zombie(0, 0))
            zombies.append(Zombie(0, SCREEN_HEIGHT - 50))

            # delay the second batch
            delayed_zombies.append(("left", zombie_spawn_time + 2000))  # Delay 2 seconds
            delayed_zombies.append(("right", zombie_spawn_time + 2000))
        

    # chech if is time to spown the delayd zombies
    current_time = pygame.time.get_ticks()
    for side, spawn_time in delayed_zombies[:]:  

        if current_time >= spawn_time:
            if side == "left":
                zombies.append(Zombie(0, 0))
            else:
                zombies.append(Zombie(0, SCREEN_HEIGHT - 50))
            
            delayed_zombies.remove((side, spawn_time))  # Remove from delayed list


    screen.fill((0, 128, 0))  

    for ob in obstacles:
        draw_textured_rectangle(screen, texture, ob)

    all_sprites = pygame.sprite.Group([player] + zombies)
    all_sprites.draw(screen)
    
    
    for zombie in zombies:
        draw_health_bars(screen, player, zombie)  

    pygame.display.update()

pygame.quit() # exit the window

