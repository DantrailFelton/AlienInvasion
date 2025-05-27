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
        
        # Create a larger surface for the power-up
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
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
        self.color = self.settings.power_up_types[self.type]['color']
        
        # Draw the power-up based on its type
        self._draw_power_up()
        
        # Add glow effect
        self.glow_radius = 0
        self.glow_growing = True
        
    def update(self):
        """Move the power-up down the screen."""
        self.y += self.settings.power_up_speed
        self.rect.y = self.y
        
        # Update glow effect
        if self.glow_growing:
            self.glow_radius += 0.2
            if self.glow_radius >= 5:
                self.glow_growing = False
        else:
            self.glow_radius -= 0.2
            if self.glow_radius <= 0:
                self.glow_growing = True
        
        # Remove power-up if it goes off screen
        if self.rect.top > self.screen_rect.bottom:
            self.kill()
        
    def draw_power_up(self):
        """Draw the power-up to the screen."""
        # Draw glow effect
        glow_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
        glow_color = (*self.color, 100)  # Semi-transparent version of power-up color
        pygame.draw.circle(glow_surface, glow_color, 
                         (self.rect.width//2 + 10, self.rect.height//2 + 10),
                         int(self.glow_radius + 10))
        self.screen.blit(glow_surface, 
                        (self.rect.x - 10, self.rect.y - 10))
        
        # Draw the power-up
        self.screen.blit(self.image, self.rect)
        
    def _draw_power_up(self):
        """Draw the power-up on its image surface."""
        if self.type == 'large_blast':
            self._draw_ki_blast()
        elif self.type == 'auto_fire':
            self._draw_auto_fire()
        else:  # ally_help
            self._draw_ally_help()
            
    def _draw_ki_blast(self):
        """Draw a ki blast shape for the large blast power-up."""
        # Draw outer circle
        pygame.draw.circle(self.image, self.color, (15, 15), 12)
        # Draw inner circle
        pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 6)
        # Draw energy lines
        for i in range(8):
            angle = math.pi / 4 * i
            start_pos = (15 + math.cos(angle) * 6, 15 + math.sin(angle) * 6)
            end_pos = (15 + math.cos(angle) * 12, 15 + math.sin(angle) * 12)
            pygame.draw.line(self.image, (255, 255, 255), start_pos, end_pos, 2)
            
    def _draw_auto_fire(self):
        """Draw an auto-fire symbol."""
        # Draw circular base
        pygame.draw.circle(self.image, self.color, (15, 15), 12)
        # Draw three bullets
        for i in range(3):
            angle = math.pi / 3 * i
            x = 15 + math.cos(angle) * 8
            y = 15 + math.sin(angle) * 8
            pygame.draw.circle(self.image, (255, 255, 255), (int(x), int(y)), 3)
            
    def _draw_ally_help(self):
        """Draw an ally help symbol."""
        # Draw circular base
        pygame.draw.circle(self.image, self.color, (15, 15), 12)
        # Draw Vegeta's symbol (simplified)
        points = [
            (15, 8),  # Top
            (20, 15),  # Right
            (15, 22),  # Bottom
            (10, 15)   # Left
        ]
        pygame.draw.polygon(self.image, (255, 255, 255), points)
        # Draw inner circle
        pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 4) 