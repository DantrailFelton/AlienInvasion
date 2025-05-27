import pygame
from pygame.sprite import Sprite
import math
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien above the screen
        self.rect.x = self.rect.width
        self.rect.y = -self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement pattern attributes
        self.movement_pattern = 0  # 0: normal, 1: zigzag, 2: circular, 3: dive bomber
        self.movement_angle = 0
        self.original_x = self.x
        self.zigzag_offset = 0
        self.circular_radius = 50
        self.circular_center_x = self.x
        self.circular_center_y = self.y
        
        # Dive bomber attributes
        self.is_dive_bomber = False
        self.dive_target_x = None
        self.dive_speed = 1.0
        self.dive_angle = 0
        self.dive_started = False
        
        # Entrance state
        self.has_entered = False
        self.entrance_speed = 0.3
        self.target_y = self.rect.height

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self, level):
        """Move the alien based on its pattern and entrance state."""
        # Calculate speed based on level
        level_speed = self.settings.alien_speed * level
        
        if not self.has_entered:
            # Move down until reaching target position
            if self.rect.y < self.target_y:
                self.y += self.entrance_speed
                self.rect.y = self.y
            else:
                self.has_entered = True
                self.circular_center_y = self.y
                # Initialize dive bomber if selected
                if self.is_dive_bomber:
                    self.dive_target_x = self.settings.screen_width * random.random()
                    self.dive_angle = math.atan2(self.settings.screen_height - self.y,
                                               self.dive_target_x - self.x)
        else:
            if self.is_dive_bomber and not self.dive_started:
                # Check if it's time to start diving (25% chance per update)
                if random.random() < 0.25 * (1 + (level - 1) * 0.1):  # Increase chance with level
                    self.dive_started = True
            
            if self.dive_started:
                # Dive bomber movement
                self.x += math.cos(self.dive_angle) * self.dive_speed * level_speed
                self.y += math.sin(self.dive_angle) * self.dive_speed * level_speed
                self.rect.x = self.x
                self.rect.y = self.y
                
                # If dive bomber goes off screen, reset it to top
                if self.rect.top > self.settings.screen_height:
                    self._reset_to_top()
            else:
                # Normal movement patterns
                if self.movement_pattern == 0:  # Normal movement
                    self.x += (level_speed * self.settings.fleet_direction)
                    self.rect.x = self.x
                elif self.movement_pattern == 1:  # Zigzag movement
                    self.zigzag_offset += 0.1
                    self.x = self.original_x + math.sin(self.zigzag_offset) * 50
                    self.y += level_speed * 0.2
                    self.rect.x = self.x
                    self.rect.y = self.y
                elif self.movement_pattern == 2:  # Circular movement
                    self.movement_angle += 0.05
                    self.x = self.circular_center_x + math.cos(self.movement_angle) * self.circular_radius
                    self.y = self.circular_center_y + math.sin(self.movement_angle) * self.circular_radius
                    self.rect.x = self.x
                    self.rect.y = self.y

    def _reset_to_top(self):
        """Reset the alien to the top of the screen."""
        self.rect.y = -self.rect.height
        self.y = float(self.rect.y)
        self.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.x = self.x
        self.has_entered = False
        self.dive_started = False
        if self.is_dive_bomber:
            self.dive_target_x = self.settings.screen_width * random.random()
            self.dive_angle = math.atan2(self.settings.screen_height - self.y,
                                       self.dive_target_x - self.x) 