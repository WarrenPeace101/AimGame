import pygame
import sys
import random

class GameScreen:
    def __init__(self):
        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BLOOD_RED = (138, 3, 3, 180)

        # fonts
        self.BIG_HEADER_FONT = pygame.font.SysFont(None, 35)
        self.MINI_HEADER_FONT = pygame.font.SysFont(None, 23)
        self.GAME_OVER_FONT = pygame.font.SysFont(None, 80)

        # screen information
        self.WIDTH = 800
        self.HEIGHT = 600
        self.score = 0

        # header information
        self.HEADER_OFFSET_FROM_TOP = 90

        #target circle information
        self.TARGET_CIRCLE_VISIBLE_TIME = 1200
        self.TARGET_CIRCLE_RADIUS = 20
        self.TARGET_CIRCLE_BORDER_RADIUS = 2
        self.targetCircleLocation = (random.randint(self.TARGET_CIRCLE_RADIUS, self.WIDTH - self.TARGET_CIRCLE_RADIUS),
                      random.randint(self.TARGET_CIRCLE_RADIUS + self.HEADER_OFFSET_FROM_TOP, self.HEIGHT - self.TARGET_CIRCLE_RADIUS))
        self.targetCircleTime = pygame.time.get_ticks()

        # Level information
        self.currentLevel = 1

        # Lives information
        self.livesLeft = 3
        self.flashUntil = 0

        # Time to click info
        self.timeToClick = 10000
        self.lastClickTime = 0
        self.elapsedTime = 0
        self.remainingRatio = 0

        # Music
        self.backgroundMusic = None



    def startGame(self):

        self.backgroundMusic = pygame.mixer.Sound("AimTrainNewMusic.mp3")
        self.backgroundMusic.set_volume(0.3)
        self.backgroundMusic.play(loops=-1)

        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Aim Game")

        self.runGame(screen)


    def runGame(self, screen):
        clock = pygame.time.Clock()
        running = True
        while running:

            if self.livesLeft == 0:
                running = False

            current_time = pygame.time.get_ticks()
            self.elapsedTime = current_time - self.lastClickTime
            self.remainingRatio = max(0, 1 - (self.elapsedTime / self.timeToClick))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClickLogic(event, current_time)

            # Check if circle time expired - spawn new circle
            if current_time - self.targetCircleTime > self.TARGET_CIRCLE_VISIBLE_TIME:
                self.targetCircleLocation = (
                random.randint(self.TARGET_CIRCLE_RADIUS, self.WIDTH - self.TARGET_CIRCLE_RADIUS),
                random.randint(self.TARGET_CIRCLE_RADIUS + self.HEADER_OFFSET_FROM_TOP,
                               self.HEIGHT - self.TARGET_CIRCLE_RADIUS))
                self.targetCircleTime = current_time

            # Check if time to click is expired, if so lower lives and reset time to click
            if current_time - self.lastClickTime > self.timeToClick:
                self.livesLeft -= 1
                self.lastClickTime = current_time
                self.flashUntil = pygame.time.get_ticks() + 50

                lostLifeSound = pygame.mixer.Sound("Miss.mp3")
                lostLifeSound.set_volume(0.3)
                lostLifeSound.play(loops=0)

            self.drawGameScreen(screen, current_time)

            clock.tick(60)

        self.gameOver(screen)

    def drawGameScreen(self, screen, currentTime):
        if currentTime < self.flashUntil:
            self.drawFlash(screen)
        else:
            # clear screen
            self.drawWhiteBackground(screen)

            # draw the health bar and header
            self.drawHealthBar(screen)
            self.drawHeader(screen)

            # Draw the circle
            pygame.draw.circle(screen, self.GREEN, self.targetCircleLocation, self.TARGET_CIRCLE_RADIUS)
            pygame.draw.circle(screen, self.BLACK, self.targetCircleLocation, self.TARGET_CIRCLE_RADIUS,
                                self.TARGET_CIRCLE_BORDER_RADIUS)

        pygame.display.flip()

    def drawFlash(self, screen):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.BLOOD_RED)
        screen.blit(overlay, (0, 0))

    def drawWhiteBackground(self, screen):
        screen.fill(self.WHITE)

    def drawHealthBar(self, screen):
        BAR_X = 50
        BAR_Y = 64
        BAR_WIDTH = 700
        BAR_HEIGHT = 15

        # Background (full bar outline)
        pygame.draw.rect(screen, self.BLACK, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), width=2)

        # Filled portion, shrinking as time decreases
        fill_width = int(BAR_WIDTH * self.remainingRatio)

        pygame.draw.rect(screen, self.GREEN, (BAR_X, BAR_Y, fill_width, BAR_HEIGHT))
        pygame.draw.rect(screen, self.BLACK, (BAR_X, BAR_Y, fill_width, BAR_HEIGHT), width=2)

    def drawHeader(self, screen):
        # Draw the blue lines for top border
        pygame.draw.line(screen, self.BLUE, (0, 90), (799, 90), width=2)
        pygame.draw.line(screen, self.BLUE, (0, 0), (799, 0), width=2)
        pygame.draw.line(screen, self.BLUE, (0, 90), (0, 0), width=2)
        pygame.draw.line(screen, self.BLUE, (799, 0), (799, 90), width=2)

        # Display instructions
        instruction_text = self.BIG_HEADER_FONT.render("Click the Green Circle!", True, self.BLACK)
        screen.blit(instruction_text, (250, 10))

        # Update level indicator
        level_text = self.MINI_HEADER_FONT.render(f"Level: {self.currentLevel}", True, self.BLACK)
        screen.blit(level_text, (150, 40))

        # Update score
        score_text = self.MINI_HEADER_FONT.render(f"Score: {self.score}", True, self.BLACK)
        screen.blit(score_text, (350, 40))

        # Update lives
        lives_text = self.MINI_HEADER_FONT.render(f"Lives: {self.livesLeft}", True, self.BLACK)
        screen.blit(lives_text, (550, 40))


    def handleClickLogic(self, event, currentTime):
        mouse_pos = event.pos

        # Check distance between click and circle center
        dist = ((mouse_pos[0] - self.targetCircleLocation[0]) ** 2 + (mouse_pos[1] - self.targetCircleLocation[1]) ** 2) ** 0.5
        if dist <= self.TARGET_CIRCLE_RADIUS:
            self.score += 1
            # Spawn new circle immediately on hit
            self.targetCircleLocation = (random.randint(self.TARGET_CIRCLE_RADIUS, self.WIDTH - self.TARGET_CIRCLE_RADIUS),
                          random.randint(self.TARGET_CIRCLE_RADIUS + self.HEADER_OFFSET_FROM_TOP, self.HEIGHT - self.TARGET_CIRCLE_RADIUS))
            self.targetCircleTime = pygame.time.get_ticks()
            self.lastClickTime = currentTime
        else:
            print("todo")


    def gameOver(self, screen):
        self.backgroundMusic.stop()

        gameOverMusic = pygame.mixer.Sound("GameOverMusic.mp3")
        gameOverMusic.set_volume(0.3)
        gameOverMusic.play(loops=0)

        self.drawGameOver(screen)

        waiting = True
        clock = pygame.time.Clock()
        while waiting:



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(60)



    def drawGameOver(self, screen):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.BLOOD_RED)
        screen.blit(overlay, (0, 0))

        #Game Over Text
        gameOverX = (self.WIDTH // 3) - 40
        gameOverY = (self.HEIGHT // 3)

        gameOverText = self.GAME_OVER_FONT.render("GAME OVER", True, self.WHITE)
        screen.blit(gameOverText, (gameOverX, gameOverY))

        #Play Again Button
        playAgainX = (self.WIDTH // 3) + 15
        playAgainY = (self.HEIGHT // 3) + 75
        playAgainWidth = 200
        playAgainHeight = 50

        playAgainRect = pygame.Rect(playAgainX, playAgainY, playAgainWidth, playAgainHeight)
        pygame.draw.rect(screen, self.WHITE, playAgainRect)
        pygame.draw.rect(screen, self.BLACK, playAgainRect, width=2)

        buttonFont = pygame.font.SysFont(None, 36)
        playAgainText = buttonFont.render("Play Again", True, self.BLACK)
        playAgainTextRect = playAgainText.get_rect(center=playAgainRect.center)
        screen.blit(playAgainText, playAgainTextRect)

        #Menu Button
        menuX = (self.WIDTH // 3) + 15
        menuY = (self.HEIGHT // 3) + 145
        menuWidth = 200
        menuHeight = 50

        menuRect = pygame.Rect(menuX, menuY, menuWidth, menuHeight)
        pygame.draw.rect(screen, self.WHITE, menuRect)
        pygame.draw.rect(screen, self.BLACK, menuRect, width=2)

        menuText = buttonFont.render("Menu", True, self.BLACK)
        menuTextRect = menuText.get_rect(center=menuRect.center)
        screen.blit(menuText, menuTextRect)

        pygame.display.flip()














