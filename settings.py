class Settings:
    """A class to store all settings for AlienInvasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 0.3  # Reduced base speed
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.5  # Reduced bullet speed
        self.bullet_width = 8
        self.bullet_height = 25
        self.bullet_color = (0, 191, 255)  # Bright blue color
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 0.05  # Reduced base alien speed
        self.fleet_drop_speed = 2  # Reduced drop speed
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Star settings
        self.star_count = 100
        self.star_speed = 0.3  # Reduced star speed

        # Transformation settings
        self.transformation_power_levels = {
            'base': 0,
            'ssj': 1000,
            'ssj2': 2000,
            'ssj3': 3000
        }
        self.transformation_speed_multipliers = {
            'base': 1.0,
            'ssj': 1.2,    # Reduced speed multiplier
            'ssj2': 1.4,   # Reduced speed multiplier
            'ssj3': 1.6    # Reduced speed multiplier
        }
        self.transformation_bullet_multipliers = {
            'base': 1.0,
            'ssj': 1.2,
            'ssj2': 1.4,
            'ssj3': 1.6
        }

        # How quickly the game speeds up (reduced scaling)
        self.speedup_scale = 1.05
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Power-up settings
        self.power_up_speed = 0.3
        self.power_up_types = {
            'large_blast': {
                'width_multiplier': 2.0,  # Increased for more dramatic effect
                'height_multiplier': 2.0,
                'duration': 10000,  # 10 seconds
                'color': (255, 0, 0)  # Red
            },
            'auto_fire': {
                'duration': 8000,  # 8 seconds
                'fire_delay': 200,  # 200ms between shots
                'color': (0, 255, 0)  # Green
            },
            'ally_help': {
                'duration': 15000,  # 15 seconds
                'color': (0, 0, 255)  # Blue
            }
        }
        self.power_up_active = False
        self.power_up_type = None
        self.power_up_start_time = 0
        self.power_up_spawned = False
        self.power_up_threshold = 500
        self.auto_fire = False  # Track auto-fire state
        self.last_fire_time = 0  # Track last auto-fire time
        self.last_ally_fire_time = 0  # Track last ally fire time
        self.ally_active = False
        self.ally_spawned = False
        self.ally_threshold = 1000
        self.ally_fire_delay = 1000  # 1 second between ally shots

        # Store original bullet dimensions for reset
        self.original_bullet_width = 8
        self.original_bullet_height = 25

        # Initialize alien points
        self.alien_points = 50

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        # More gradual speed increases
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # Cap maximum speeds
        self.ship_speed = min(self.ship_speed, 0.6)  # Cap ship speed
        self.bullet_speed = min(self.bullet_speed, 2.5)  # Cap bullet speed
        self.alien_speed = min(self.alien_speed, 0.2)  # Cap alien speed

        self.alien_points = int(self.alien_points * self.score_scale)

    def increase_power(self):
        """Power up the ship's weapons."""
        if self.bullets_allowed < 5:  # Cap at 5 simultaneous bullets
            self.bullets_allowed += 1
        self.bullet_width += 1  # Wider ki blasts
        if self.bullet_width > 10:  # Cap width at 10 pixels
            self.bullet_width = 10

        # Star settings
        self.star_count = 100  # Number of stars in the background