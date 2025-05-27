from ship import Ship
import pygame

class AllyShip(Ship):
    """A class to represent the ally ship that mirrors the player's ship."""
    
    def __init__(self, ai_game):
        """Initialize the ally ship and set its starting position."""
        super().__init__(ai_game)
        self.ai_game = ai_game  # Store reference to main game
        
        # Load Vegeta's ship image
        self.image = pygame.image.load('images/vegeta_ship.bmp')
        self.rect = self.image.get_rect()
        
        # Position the ally ship to the right of the player's ship
        self.rect.midbottom = (self.screen_rect.right - 60, self.screen_rect.bottom - 60)
        self.x = float(self.rect.x)
        
        # Ally hit points
        self.hit_points = 3
    
    def update(self):
        """Update the ally ship's position based on the player's ship."""
        # Mirror the player's ship movement
        speed = self.settings.ship_speed * self.settings.transformation_speed_multipliers[self.form]
        if self.ai_game.ship.moving_right and self.rect.left > 0:
            self.x -= speed
        if self.ai_game.ship.moving_left and self.rect.right < self.screen_rect.right:
            self.x += speed
        # Update the rect position
        self.rect.x = self.x
        # Keep the ally ship on screen
        if self.rect.left < self.screen_rect.left:
            self.rect.left = self.screen_rect.left
            self.x = float(self.rect.x)
        if self.rect.right > self.screen_rect.right:
            self.rect.right = self.screen_rect.right
            self.x = float(self.rect.x)
    
    def take_hit(self):
        """Reduce hit points by 1. Return True if destroyed."""
        self.hit_points -= 1
        if self.hit_points <= 0:
            return True
        return False

    def blitme(self):
        """Draw the ally ship at its current location and show health bar."""
        self.screen.blit(self.image, self.rect)
        # Draw health bar above the ally ship
        bar_width = 40
        bar_height = 6
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 12
        # Background (gray)
        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        # Health (green)
        health_width = int(bar_width * (self.hit_points / 3))
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1) 