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

        # fonts
        self.BIG_HEADER_FONT = pygame.font.SysFont(None, 36)
        self.MINI_HEADER_FONT = pygame.font.SysFont(None, 23)

        # screen information
        self.WIDTH = 800
        self.HEIGHT = 600
        self.score = 0

        # header information
        self.HEADER_OFFSET_FROM_TOP = 60

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
                self.gameOver()
                break


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClickLogic(event)

            current_time = pygame.time.get_ticks()

            # Check if circle time expired - spawn new circle
            if current_time - self.targetCircleTime > self.TARGET_CIRCLE_VISIBLE_TIME:
                self.targetCircleLocation = (
                random.randint(self.TARGET_CIRCLE_RADIUS, self.WIDTH - self.TARGET_CIRCLE_RADIUS),
                random.randint(self.TARGET_CIRCLE_RADIUS + self.HEADER_OFFSET_FROM_TOP,
                               self.HEIGHT - self.TARGET_CIRCLE_RADIUS))
                self.targetCircleTime = current_time

            self.drawGameScreen(screen, current_time)

            clock.tick(60)

        pygame.quit()
        sys.exit()

    def drawGameScreen(self, screen, currentTime):
        if currentTime < self.flashUntil:
            self.drawFlash(screen)
        else:
            # clear screen
            self.drawWhiteBackground(screen)

            # draw the header
            self.drawHeader(screen)

            # Draw the circle
            pygame.draw.circle(screen, self.GREEN, self.targetCircleLocation, self.TARGET_CIRCLE_RADIUS)
            pygame.draw.circle(screen, self.BLACK, self.targetCircleLocation, self.TARGET_CIRCLE_RADIUS,
                                self.TARGET_CIRCLE_BORDER_RADIUS)

        pygame.display.flip()

    def drawFlash(self, screen):
        screen.fill(self.RED)

    def drawWhiteBackground(self, screen):
        screen.fill(self.WHITE)

    def drawHeader(self, screen):
        # Draw the blue lines for top border
        pygame.draw.line(screen, self.BLUE, (0, 60), (799, 60), width=2)
        pygame.draw.line(screen, self.BLUE, (0, 0), (799, 0), width=2)
        pygame.draw.line(screen, self.BLUE, (0, 60), (0, 0), width=2)
        pygame.draw.line(screen, self.BLUE, (799, 0), (799, 60), width=2)

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


    def handleClickLogic(self, event):
        mouse_pos = event.pos

        # Check distance between click and circle center
        dist = ((mouse_pos[0] - self.targetCircleLocation[0]) ** 2 + (mouse_pos[1] - self.targetCircleLocation[1]) ** 2) ** 0.5
        if dist <= self.TARGET_CIRCLE_RADIUS:
            self.score += 1
            # Spawn new circle immediately on hit
            self.targetCircleLocation = (random.randint(self.TARGET_CIRCLE_RADIUS, self.WIDTH - self.TARGET_CIRCLE_RADIUS),
                          random.randint(self.TARGET_CIRCLE_RADIUS + self.HEADER_OFFSET_FROM_TOP, self.HEIGHT - self.TARGET_CIRCLE_RADIUS))
            self.targetCircleTime = pygame.time.get_ticks()
        else:
            self.livesLeft -= 1
            self.flashUntil = pygame.time.get_ticks() + 50

    def gameOver(self):
        self.backgroundMusic.stop()

        gameOverMusic = pygame.mixer.Sound("GameOverMusic.mp3")
        gameOverMusic.set_volume(0.3)
        gameOverMusic.play(loops=0)



