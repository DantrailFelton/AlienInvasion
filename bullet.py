import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class to manage the bullet fired from the ship """

    def __init__(self, ai_game, ship):
        """ Create a bullet object at the ship's current position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

        # Create trail effect
        self.trail_positions = []
        self.trail_length = 5
        self.trail_alpha = 128  # Semi-transparent trail

    def update(self):
        """ Move the bullet up the screen"""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

        # Update trail positions
        self.trail_positions.append((self.rect.centerx, self.rect.bottom))
        if len(self.trail_positions) > self.trail_length:
            self.trail_positions.pop(0)

    def draw_bullet(self):
        """ Draw the bullet on the screen"""
        # Draw trail
        if len(self.trail_positions) > 1:
            trail_surface = pygame.Surface((self.settings.bullet_width, 
                self.settings.bullet_height * self.trail_length), pygame.SRCALPHA)
            for i in range(len(self.trail_positions) - 1):
                alpha = int(255 * (1 - i / len(self.trail_positions)))
                pygame.draw.line(trail_surface, (*self.color, alpha),
                    self.trail_positions[i], self.trail_positions[i + 1],
                    int(self.settings.bullet_width))
            self.screen.blit(trail_surface, (self.rect.x, self.rect.bottom))
        
        # Draw main bullet
        pygame.draw.rect(self.screen, self.color, self.rect)
