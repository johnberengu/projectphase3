import pygame
import json
import os


pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monster Battle")

font = pygame.font.Font(None, 36)
input_box = pygame.Rect(300, 250, 200, 40)
input_box2 = pygame.Rect(300, 300, 200, 40)
button = pygame.Rect(350, 400, 100, 50)


color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
input_color = color_inactive
input_color2 = color_inactive
active = False
active2 = False
name = ''
age = ''

# save to db.json file
def save_to_db(name, age):
    try:
        with open("db.json", "r") as f:
            data = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        data = [] 


    # create a new dictionary for players
    new_player = {"player": {"name": name, "age": age}}

   
    data.append(new_player)

   

    with open("db.json", "w") as f:
        json.dump(data, f, indent=4)


def main():
    global active, input_color, name, active2, input_color2, age
    running = True


    while running:
        screen.fill((0, 0, 0))
        title = font.render("Welcome to Monster Battle", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))


        pygame.draw.rect(screen, input_color, input_box, 2)
        pygame.draw.rect(screen, input_color2, input_box2, 2)
        pygame.draw.rect(screen, (0, 255, 0), button)


        name_text = font.render(name if name else 'Name', True, (255, 255, 255))
        age_text = font.render(age if age else 'Age', True, (255, 255, 255))
        screen.blit(name_text, (input_box.x+5, input_box.y+5))
        screen.blit(age_text, (input_box2.x+5, input_box2.y+5))


        enter_text = font.render("Enter", True, (0, 0, 0))
        screen.blit(enter_text, (button.x + 20, button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    input_color = color_active
                    if name == '':
                        name = ''

                else:
                    active = False
                    input_color = color_inactive
                
                if input_box2.collidepoint(event.pos):
                    active2 = True
                    input_color2 = color_active
                    if age == '':
                        age = ''

                else:
                    active2 = False
                    input_color2 = color_inactive

                if button.collidepoint(event.pos) and name and age.isdigit():
                    save_to_db(name, age)
                    pygame.quit()
                    os.system("python monsterbattle.py")
                    return


            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]

                    else:
                        name += event.unicode

                if active2:
                    if event.key == pygame.K_BACKSPACE:
                        age = age[:-1]
                    elif event.unicode.isdigit():
                        age += event.unicode


        pygame.display.update()

    pygame.quit()


# executes the main function on the main window
if __name__ == "__main__":
    main()
