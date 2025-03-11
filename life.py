import pygame

# This is shows the health bar
class HealthBar:
    def __init__(self, entity, width=50, height=5, max_health=100):

        self.entity = entity  
        self.width = width
        self.height = height
        self.max_health = max_health
        self.health = max_health  

    # Set the max health
    def take_damage(self, amount):

        self.health = max(0, self.health - amount)  

    # 
    def draw(self, surface):

        if self.health > 0:
            # Calculate the position of the health bar relative to the entity's position
            bar_x = self.entity.rect.centerx - self.width // 2
            bar_y = self.entity.rect.top - 10  
            # Draw the health bar as a rectangle filled with the color of the health percentage (red for low health, green for high health)
            fill = int((self.health / self.max_health) * self.width)
            color = (255, 0, 0) if self.health < self.max_health // 3 else (0, 255, 0)  
            pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, self.width, self.height))  
            pygame.draw.rect(surface, color, (bar_x, bar_y, fill, self.height))  

def setup_health(player, zombie):
    #set up the health bar for the player and zombie
    player.health_bar = HealthBar(player)
    zombie.health_bar = HealthBar(zombie)

def update_health(player, zombies):
    # Update the health of the zombie and the player
    player.health_bar.health = max(0, player.health_bar.health)
    
    for zombie in zombies:

        zombie.health_bar.health = max(0, zombie.health_bar.health)
        


def draw_health_bars(surface, player, zombie):
    #draws the health bars
    player.health_bar.draw(surface)
    zombie.health_bar.draw(surface)
