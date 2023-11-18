#Import modules
import pygame
import random
import os

#Initilize pygame
pygame.init()

#Initilize soundtrack
pygame.mixer.init()

#Creating & naming game window
gameWindow=pygame.display.set_mode((900,500))
gameWindow_name=pygame.display.set_caption("My First Game")

#Colors
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
black=(0,0,0)
ass=(96,96,96)

#Images
front_image=pygame.image.load('first.jpg.jpg').convert_alpha()
middle_image=pygame.image.load('second.jpg.jpg').convert_alpha()
last_image=pygame.image.load('final.jpg.jpg').convert_alpha()
pygame.transform.scale(front_image,(900,500))
pygame.transform.scale(middle_image,(900,500))
pygame.transform.scale(last_image,(900,500))

#Initilize time modules
game_clock=pygame.time.Clock()

#Text (Score) function
game_font=pygame.font.SysFont(None, 50)
def text_screen(text, color, x,y):
    screen_text=game_font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

#Snake body function
def mysnake(gamewindow, color, snklist, width, height):
    for x, y in snklist:
        pygame.draw.rect(gamewindow,color, (x, y,width, height))

#Welcome window function
def welcomeWindow():
    #Game specific variables
    game_exit=False
    #Game (welcomeWindow) Loop
    while not game_exit:
        gameWindow.fill(white)
        gameWindow.blit(front_image,[0,0])
        text_screen("WELCOME", black, 150,200)
        text_screen("Press Space bar to Play", black, 69,300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit= True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #Loading (Importing) sound
                    pygame.mixer.music.load("Start.mp3")
                    #Playing sound
                    pygame.mixer.music.play()
                    pygame.time.wait(1000)  #If someone reading this code, in this line, I think here could be another way to implement the logic ( I want to play the "gamesound" sound after the "Start" sound without using 'wait()' function ). If you have any idea to solve this, please solve this and send me Pull Request.
                    pygame.mixer.music.load("gamesound.mp3")
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        game_clock.tick(60)
    pygame.quit()

#Game Loop function
def gameloop():
    #Game specific variables
    game_exit=False
    game_over=False
    snake_x_pos=100
    snake_y_pos=100
    velocity_x=0
    velocity_y=0
    food_x=random.randint(0,850)
    food_y=random.randint(0,450)
    game_score=0
    fps=60
    snk_list=[]
    snk_length=1
    #File ( Highscore ) i/o
    if(not os.path.exists('highscore.txt')):
        with open('highscore.txt','w') as f:
            f.write('0')
    with open('highscore.txt','r') as f:
        high_score=f.read()
    #Game Loop
    while not game_exit:
        if game_over==True:
                with open('highscore.txt','w') as f:
                    f.write(str(high_score))
                gameWindow.fill(white)
                gameWindow.blit(last_image,[0,0])
                text_screen("Game Over!!!", red, 550,100)
                text_screen("Press Enter to Continue", red, 350,375)
                for event in pygame.event.get():
                    #Game Quit Logic
                    if event.type == pygame.QUIT:
                        game_exit= True
                    #Return in Game Logic
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            welcomeWindow()

        else:

            for event in pygame.event.get():
                #Game Quit Logic
                if event.type == pygame.QUIT:
                    game_exit= True
                #Game events handler
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x+=5
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        velocity_x-=5
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y-=5
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y+=5
                        velocity_x=0

            #Velocity initilize
            snake_x_pos+=velocity_x
            snake_y_pos+=velocity_y
            #Food eating & Snake length increasing
            if (snake_x_pos-food_x)<5 and (snake_y_pos-food_y)<5:
                game_score+=10
                food_x=random.randint(0,850)
                food_y=random.randint(0,450)
                snk_length+=5
                if game_score> int(high_score):
                    high_score=game_score             

            gameWindow.fill(green)
            gameWindow.blit(middle_image,[0,0])
            text_screen("Score : "+str(game_score), red, 5,5)
            text_screen("Created by - Mr. KISKU", ass, 500,450)
            text_screen("HighScore : "+str(high_score), blue, 220,5)
            mysnake(gameWindow,black,snk_list,50,40)
            #Snake length increasing & cutting
            snk_head=[]
            snk_head.append(snake_x_pos)
            snk_head.append(snake_y_pos)
            snk_list.append(snk_head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            #Game Over Logic
            if snake_x_pos<0 or snake_x_pos>900 or snake_y_pos<0 or snake_y_pos>500:
                pygame.mixer.music.load("Game over.mp3")
                pygame.mixer.music.play()
                game_over=True

            #Game Over Logic
            '''if snk_head in snk_list[:-1]:
                game_over=True'''

            pygame.draw.rect(gameWindow, blue, (food_x,food_y,50,40))
        pygame.display.update()
        game_clock.tick(fps)

    #Quit pygame 
    pygame.quit()

welcomeWindow()
