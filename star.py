import pygame
from pygame.sprite import Sprite
import random

class Star(Sprite):
    """A class to represent a star in the background."""

    def __init__(self, ai_game):
        """Initialize the star and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Create a star rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, 2, 2)
        
        # Set random position
        self.rect.x = random.randint(0, self.screen_rect.width)
        self.rect.y = random.randint(-self.screen_rect.height, 0)
        
        # Store the star's exact vertical position
        self.y = float(self.rect.y)
        
        # Random star properties
        self.speed = random.uniform(0.5, 2.0)
        self.brightness = random.randint(100, 255)
        self.color = (self.brightness, self.brightness, self.brightness)

    def update(self):
        """Move the star down the screen."""
        self.y += self.speed
        self.rect.y = self.y

        # Reset star to top when it reaches bottom
        if self.rect.top > self.screen_rect.bottom:
            self.rect.y = random.randint(-50, 0)
            self.y = float(self.rect.y)
            self.rect.x = random.randint(0, self.screen_rect.width)
            self.speed = random.uniform(0.5, 2.0)
            self.brightness = random.randint(100, 255)
            self.color = (self.brightness, self.brightness, self.brightness) 