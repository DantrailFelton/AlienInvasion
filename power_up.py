import pygame
from pygame.sprite import Sprite
import random
import math

class PowerUp(Sprite):
    """A class to represent power-ups in the game."""
    
    def __init__(self, ai_game):
        """Initialize the power-up and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        
        # Load the power-up image and set its rect attribute.
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 215, 0))  # Gold color
        self.rect = self.image.get_rect()
        
        # Start each new power-up at a random position at the top of the screen.
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -self.rect.height
        
        # Store the power-up's exact position.
        self.y = float(self.rect.y)
        
        # Power-up types and their effects
        self.types = ['large_blast', 'auto_fire', 'ally_help']
        self.type = random.choice(self.types)
        
        # Set color based on type
        if self.type == 'large_blast':
            self.image.fill((255, 0, 0))  # Red for large blast
        elif self.type == 'auto_fire':
            self.image.fill((0, 255, 0))  # Green for auto fire
        else:  # ally_help
            self.image.fill((0, 0, 255))  # Blue for ally help
            
    def update(self):
        """Move the power-up down the screen."""
        self.y += self.settings.power_up_speed
        self.rect.y = self.y
        
        # Remove power-up if it goes off screen
        if self.rect.top > self.screen_rect.bottom:
            self.kill()
        
    def draw_power_up(self):
        """Draw the power-up to the screen."""
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)
        self.screen.blit(self.image, self.rect.topleft)
        
    def _draw_power_up(self):
        """Draw the power-up on its image surface."""
        if self.type == 'star':
            self._draw_star()
        elif self.type == 'circle':
            pygame.draw.circle(self.image, self.color, (15, 15), 15)
        elif self.type == 'square':
            pygame.draw.rect(self.image, self.color, self.image.get_rect())
        else:  # bean
            self._draw_bean()
            
        # Draw a border
        pygame.draw.rect(self.image, (255, 255, 255), self.image.get_rect(), 2)
        
    def _draw_star(self):
        """Draw a star shape for the large blast power-up."""
        points = []
        center = (15, 15)
        outer_radius = 15
        inner_radius = 7
        for i in range(10):
            angle = math.pi / 5 * i
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center[0] + math.cos(angle) * radius
            y = center[1] + math.sin(angle) * radius
            points.append((x, y))
        pygame.draw.polygon(self.image, self.color, points)
        
    def _draw_bean(self):
        """Draw a bean shape for the senzu bean power-up."""
        pygame.draw.ellipse(self.image, self.color, (0, 5, 30, 20)) 