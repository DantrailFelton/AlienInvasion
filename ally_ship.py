from ship import Ship

class AllyShip(Ship):
    """A class to represent the ally ship that mirrors the player's ship."""
    
    def __init__(self, ai_game):
        """Initialize the ally ship and set its starting position."""
        super().__init__(ai_game)
        self.ai_game = ai_game  # Store reference to main game
        # Position the ally ship to the right of the player's ship
        self.rect.midleft = (self.screen_rect.right - 60, self.screen_rect.bottom - 60)
        self.x = float(self.rect.x)
        
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