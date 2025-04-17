import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys
import pickle


def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()  # Ensure the font module is initialized
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Set up the screen and clock
    pygame.display.set_caption("Asteroids in Python!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load high score
    try:
        with open("high_score.pkl", "rb") as f:
            high_score = pickle.load(f)
    except (FileNotFoundError, EOFError):
        high_score = 0
        print("No high score found. Starting from 0.")

    # Initialize game variables
    dt = 0
    score = 0

    # Set up fonts
    try:
        score_font = pygame.font.Font("3270-Regular.ttf", 36)
        high_score_font = pygame.font.Font("3270-Regular.ttf", 24)
    except FileNotFoundError:
        print("Font file not found. Using default font.")
        score_font = pygame.font.Font(None, 36)
        high_score_font = pygame.font.Font(None, 24)

    # Define score locations
    score_location = (SCREEN_WIDTH / 2, 30)
    high_score_location = (SCREEN_WIDTH / 2, 10)

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Assign sprite groups to class containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    # Create game objects
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Update game objects
        updatable.update(dt)

        # Check for collisions
        for asteroid in asteroids:
            if player.collision(asteroid):
                print("Game Over!")
                print(f"Score: {score}")

                if score > high_score:
                    high_score = score
                    with open("high_score.pkl", "wb") as f:
                        pickle.dump(high_score, f)
                pygame.quit()
                return

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()
                    score += 1

        # Render score text
        score_text = score_font.render(f"Score: {score}", True, "white")
        high_score_text = high_score_font.render(
            f"High Score: {high_score}", True, "white"
        )

        # Clear the screen
        screen.fill("black")

        # Draw score and high score
        screen.blit(score_text, score_location)
        screen.blit(high_score_text, high_score_location)

        # Draw all drawable objects
        for obj in drawable:
            obj.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
