import pygame
from GameScreen import GameScreen
from HomeScreen import HomeScreen

def launch_game():
    pygame.init()
    pygame.mixer.init()

    myHomeScreen = HomeScreen()
    myGameScreen = GameScreen()

    #startGame
    #while in game
    #if lose, run lose function

    myGameScreen.startGame()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    launch_game()
