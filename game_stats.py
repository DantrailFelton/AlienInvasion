class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Start game in an inactive state
        self.game_active = False
        
        # High score should never be reset
        self.high_score = 0

        # Accuracy tracking
        self.level_accuracies = []  # List of (level, accuracy, bullets, hits)
        self.bullets_fired = 0
        self.hits = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.power_level = 0
        self.bullets_fired = 0
        self.hits = 0
        self.level_accuracies = []
        self.aliens_defeated = 0  # Track aliens defeated for level progression 

    def start_new_level(self):
        # Save accuracy for previous level
        if self.bullets_fired > 0:
            accuracy = self.hits / self.bullets_fired
        else:
            accuracy = 0.0
        self.level_accuracies.append((self.level, accuracy, self.bullets_fired, self.hits))
        # Reset counters for new level
        self.bullets_fired = 0
        self.hits = 0

    def register_hits(self, n):
        self.hits += n

    def end_game(self):
        # Save accuracy for last level
        if self.bullets_fired > 0:
            accuracy = self.hits / self.bullets_fired
        else:
            accuracy = 0.0
        self.level_accuracies.append((self.level, accuracy, self.bullets_fired, self.hits)) 