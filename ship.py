import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship images for different forms
        self.images = {
            'base': pygame.image.load('images/ship.bmp'),
            'ssj': pygame.image.load('images/ship_ssj.bmp'),
            'ssj2': pygame.image.load('images/ship_ssj2.bmp'),
            'ssj3': pygame.image.load('images/ship_ssj3.bmp')
        }
        
        # Start with base form
        self.image = self.images['base']
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # Transformation state
        self.form = 'base'
        self.power_level = 0

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed * self.settings.transformation_speed_multipliers[self.form]
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed * self.settings.transformation_speed_multipliers[self.form]

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def transform(self, power_level):
        """Transform the ship based on power level."""
        self.power_level = power_level
        
        # Determine form based on power level
        if power_level >= self.settings.transformation_power_levels['ssj3']:
            new_form = 'ssj3'
        elif power_level >= self.settings.transformation_power_levels['ssj2']:
            new_form = 'ssj2'
        elif power_level >= self.settings.transformation_power_levels['ssj']:
            new_form = 'ssj'
        else:
            new_form = 'base'

        # Only update if form has changed
        if new_form != self.form:
            self.form = new_form
            self.image = self.images[self.form]
            # Update ship speed based on new form
            self.settings.ship_speed *= self.settings.transformation_speed_multipliers[self.form]
