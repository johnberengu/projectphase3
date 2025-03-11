import pygame
import json
import os

def load_all_players():

    try:
        with open("db.json", "r") as f:
            data = json.load(f)
            return data  
        
    except FileNotFoundError:
        return []

def delete_player_data(player_name):
    players = load_all_players()

    updated_players = [player for player in players if player["player"]["name"] != player_name]

    with open("db.json", "w") as f:
        json.dump(updated_players, f, indent=4)

def display_player(screen):
    font = pygame.font.Font(None, 36)
    running = True
    players = load_all_players()


    if not players:
        title_text = font.render("No player found!", True, (255, 0, 0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))

    else:
        player_name = players[0]["player"]["name"]
        name_text = font.render(f"Player: {player_name}", True, (255, 255, 255))
        screen.blit(name_text, (screen.get_width() // 2 - name_text.get_width() // 2, 150))

    button_width, button_height = 150, 50
    delete_button = pygame.Rect(200, 400, button_width, button_height)  # left button
    new_player_button = pygame.Rect(450, 400, button_width, button_height)  # right button


    pygame.draw.rect(screen, (255, 0, 0), delete_button)  
    pygame.draw.rect(screen, (0, 255, 0), new_player_button)  


    delete_button_text = font.render("Delete Player", True, (0, 0, 0))
    new_player_button_text = font.render("New Player", True, (0, 0, 0))

    screen.blit(delete_button_text, (delete_button.x + (button_width - delete_button_text.get_width()) // 2, delete_button.y + (button_height - delete_button_text.get_height()) // 2))
    screen.blit(new_player_button_text, (new_player_button.x + (button_width - new_player_button_text.get_width()) // 2, new_player_button.y + (button_height - new_player_button_text.get_height()) // 2))


    pygame.display.update() # update the game 

    # event loop to hundle click
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if delete_button.collidepoint(event.pos):
                   

                    delete_player_data(player_name)
                    print(f"Player {player_name} deleted.")
                    pygame.quit()
                    os.system("python start.py") 
                    running = False

                elif new_player_button.collidepoint(event.pos):
                    pygame.quit()
                    os.system("python start.py")  
                    running = False


    pygame.quit()


if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("Monster Battle - Player")


    display_player(screen)
