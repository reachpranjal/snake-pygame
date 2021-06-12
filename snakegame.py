import pygame
import random
import os

pygame.init()
pygame.mixer.init()
try:
    os.environ["DISPLAY"]
except:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

white = (255, 255, 255)
red = (255, 0, 0)
green = (34, 139, 34)
black = (0, 0, 0)
blue = (60, 146, 194)
grey = (219, 219, 219)
yellow = (226, 245, 17)
magenta = (0, 255, 251)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
font1 = pygame.font.SysFont(None, 20)

bgimg = pygame.image.load("bg.jpg")
bgimg = pygame.transform.scale(
    bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
bgimg1 = pygame.image.load("img.png")
bgimg1 = pygame.transform.scale(bgimg1, (200, 200)).convert_alpha()


def print_text(text, color, x, y):
    screenText = font.render(text, True, color)
    gameWindow.blit(screenText, [x, y])

def center_text(text, color):
    screenText = font.render(text, True, color)
    text_rect = screenText.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    gameWindow.blit(screenText, text_rect)

def drawSnake(gameWindow, color, body, SSize):
    for x, y in body:
        # pygame.draw.rect(gameWindow, color, [
        #     x, y, SSize, SSize])
        pygame.draw.circle(gameWindow, color, [
            x, y], 10)


def intro():
    EXIT = False
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as file:
            file.write("0")

    with open("highscore.txt", "r") as file:
        highscore = file.read()

    while not EXIT:
        gameWindow.blit(bgimg, (0, 0))
        gameWindow.blit(bgimg1, (220, 100))
        print_text("Py-Snake Game", grey, 200, 310)
        screenText = font1.render("Press SPACE to Play", True, red)
        gameWindow.blit(screenText, [230, 550])
        print_text("Current High Score: "+str(highscore), green, 160, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        pygame.display.update()
        clock.tick(FPS)


def game_loop():
    SSize = 20
    FSize = 20
    SLength = 1

    vel_x = 0
    vel_y = 0
    vel = 2

    pose_x = random.randint(20, 200)
    pose_y = random.randint(20, 300)
    target_x = random.randint(0, SCREEN_WIDTH//3)
    target_y = random.randint(50, SCREEN_HEIGHT//3)
    
    EXIT = False
    GAME_OVER = False

    score = 0
    body = []

    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as file:
            file.write("0")

    with open("highscore.txt", "r") as file:
        highscore = file.read()

    while not EXIT:
        if GAME_OVER:
            with open("highscore.txt", "w") as file:
                file.write(str(highscore))

            gameWindow.blit(bgimg, (0, 0))
            center_text("Crashed!", red)
            print_text("High Score: "+str(highscore), green, 210, 320)

            screenText = font1.render("Hit ENTER to Continue", True, blue)
            gameWindow.blit(screenText, [227, 550])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        intro()

        else:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        vel_x = vel
                        vel_y = 0

                    if event.key == pygame.K_LEFT:
                        vel_x = -vel
                        vel_y = 0

                    if event.key == pygame.K_UP:
                        vel_x = 0
                        vel_y = -vel

                    if event.key == pygame.K_DOWN:
                        vel_x = 0
                        vel_y = vel

            pose_x += vel_x
            pose_y += vel_y

            if abs(pose_x - target_x) < 15 and abs(pose_y - target_y) < 15:
                score += 10
                if score > int(highscore): highscore = score
                target_x = random.randint(20, SCREEN_WIDTH//2)
                target_y = random.randint(20, SCREEN_HEIGHT//2)
                SLength += 2

                vel = vel*1.03 if score>150 else vel*1.01
                pygame.mixer.music.load('scoreup.wav')
                pygame.mixer.music.play()

            gameWindow.blit(bgimg, (0, 0))
            # pygame.draw.rect(gameWindow, red, [
            #     target_x, target_y, FSize, FSize])
            pygame.draw.circle(gameWindow, red, [
                target_x, target_y], 10)

            head = []
            head.append(pose_x)
            head.append(pose_y)
            body.append(head)

            if len(body) > SLength:
                del body[0]

            if head in body[:-1]:
                GAME_OVER = True

            if pose_x > SCREEN_WIDTH:
                pose_x = pose_x - SCREEN_WIDTH
            elif pose_x < 0:
                pose_x = SCREEN_WIDTH - pose_x

            if pose_y > SCREEN_HEIGHT:
                pose_y = pose_y - SCREEN_HEIGHT
            elif pose_y < 0:
                pose_y = SCREEN_HEIGHT - pose_y

            print_text("Score: " + str(score), grey, 5, 5)
            print_text("Current High Score: " +
                       str(highscore), grey, 300, 5)

            drawSnake(gameWindow, green, body, SSize)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__ == '__main__':
	intro()
