import pygame
import sys
import random


def launch_game():
    pygame.init()
    pygame.mixer.init();

    #pygame.mixer.music.load("AimGameMusic.mp3")
    #pygame.mixer.music.play(-1)  # -1 means loop forever
    #pygame.mixer.music.set_volume(0.3)

    sound = pygame.mixer.Sound("AimGameMusic.ogg")
    sound.set_volume(0.3)
    sound.play(loops=-1)

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aim Game")

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Circle properties
    CIRCLE_RADIUS = 20
    CIRCLE_BORDER_RADIUS = 2
    HEADER_OFFSET_FROM_TOP = 44
    circle_pos = (random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS),
                  random.randint(CIRCLE_RADIUS + HEADER_OFFSET_FROM_TOP, HEIGHT - CIRCLE_RADIUS))

    # Timer for how long circle stays visible (in milliseconds)
    CIRCLE_VISIBLE_TIME = 1200
    circle_timer = pygame.time.get_ticks()

    score = 0
    font = pygame.font.SysFont(None, 48)

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        #Draw the black line
        pygame.draw.line(screen, BLACK, (0, 44), (800, 44), width=2)

        # Draw the circle
        pygame.draw.circle(screen, GREEN, circle_pos, CIRCLE_RADIUS)
        pygame.draw.circle(screen, BLACK, circle_pos, CIRCLE_RADIUS, CIRCLE_BORDER_RADIUS)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        #Display instructions
        instruction_text = font.render("Click the Green Circle!", True, BLACK)
        screen.blit(instruction_text, (250, 10))

        pygame.display.flip()

        current_time = pygame.time.get_ticks()
        # Check if circle time expired - spawn new circle
        if current_time - circle_timer > CIRCLE_VISIBLE_TIME:
            circle_pos = (random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS),
                          random.randint(CIRCLE_RADIUS + HEADER_OFFSET_FROM_TOP, HEIGHT - CIRCLE_RADIUS))
            circle_timer = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check distance between click and circle center
                dist = ((mouse_pos[0] - circle_pos[0]) ** 2 + (mouse_pos[1] - circle_pos[1]) ** 2) ** 0.5
                if dist <= CIRCLE_RADIUS:
                    score += 1
                    # Spawn new circle immediately on hit
                    circle_pos = (random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS),
                                  random.randint(CIRCLE_RADIUS + HEADER_OFFSET_FROM_TOP, HEIGHT - CIRCLE_RADIUS))
                    circle_timer = pygame.time.get_ticks()

        clock.tick(60)

    pygame.quit()
    sys.exit()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    launch_game()
