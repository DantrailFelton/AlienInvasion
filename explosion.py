import pygame
from pygame.sprite import Sprite
import random
import math

class Explosion(Sprite):
    """A class to represent explosion effects."""
    
    def __init__(self, ai_game, center, size='large'):
        """Initialize the explosion at the given center position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Set explosion size
        self.size = size
        if size == 'large':
            self.radius = 30
            self.particle_count = 20
        else:  # small
            self.radius = 15
            self.particle_count = 10
            
        # Create explosion particles
        self.particles = []
        self.create_particles(center)
        
        # Animation settings
        self.frame = 0
        self.max_frames = 30
        self.alpha = 255  # For fade out effect
        
    def create_particles(self, center):
        """Create particles for the explosion."""
        for _ in range(self.particle_count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(2, 5)
            size = random.uniform(2, 4)
            color = (
                random.randint(200, 255),  # Red
                random.randint(100, 200),  # Green
                random.randint(0, 100)     # Blue
            )
            
            self.particles.append({
                'pos': list(center),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'size': size,
                'color': color
            })
            
    def update(self):
        """Update the explosion animation."""
        self.frame += 1
        
        # Update particle positions
        for particle in self.particles:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['vel'][1] += 0.1  # Gravity effect
            particle['size'] *= 0.95   # Shrink particles
            
        # Fade out effect
        self.alpha = int(255 * (1 - self.frame / self.max_frames))
        
        # Remove explosion when animation is complete
        if self.frame >= self.max_frames:
            self.kill()
            
    def draw(self):
        """Draw the explosion particles."""
        for particle in self.particles:
            if self.alpha > 0:
                color = (*particle['color'], self.alpha)
                pos = (int(particle['pos'][0]), int(particle['pos'][1]))
                size = int(particle['size'])
                pygame.draw.circle(self.screen, color, pos, size) 