class Settings:
    """A class to store all settings for AlienInvasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 0.5  # Reduced from 1.5 for smoother movement
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.0  # Slightly reduced from 2.5 to match slower pace
        self.bullet_width = 8
        self.bullet_height = 25
        self.bullet_color = (0, 191, 255)  # Bright blue color
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 0.1  # Much slower base speed for beginning levels
        self.fleet_drop_speed = 3  # Reduced drop speed
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Star settings
        self.star_count = 100  # Number of stars in the background
        self.star_speed = 0.5  # Speed of star movement

        # Transformation settings
        self.transformation_power_levels = {
            'base': 0,
            'ssj': 1000,
            'ssj2': 2000,
            'ssj3': 3000
        }
        self.transformation_speed_multipliers = {
            'base': 1.0,
            'ssj': 1.3,
            'ssj2': 1.6,
            'ssj3': 1.9
        }
        self.transformation_bullet_multipliers = {
            'base': 1.0,
            'ssj': 1.2,
            'ssj2': 1.4,
            'ssj3': 1.6
        }

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Power-up settings
        self.power_up_speed = 0.5
        self.power_up_types = {
            'large_blast': {
                'duration': 10000,  # 10 seconds
                'width_multiplier': 2.0,
                'height_multiplier': 2.0
            },
            'auto_fire': {
                'duration': 8000,  # 8 seconds
                'fire_rate': 200  # milliseconds between shots
            },
            'ally_help': {
                'duration': 15000,  # 15 seconds
                'fire_rate': 500  # milliseconds between shots
            }
        }
        self.power_up_active = False
        self.power_up_type = None
        self.power_up_start_time = 0
        self.ally_active = False
        self.ally_last_shot = 0
        
        # Point thresholds for power-ups and allies
        self.power_up_threshold = 500
        self.ally_threshold = 1000
        self.power_up_spawned = False
        self.ally_spawned = False

        # Ally settings
        self.ally_threshold = 1000  # Score needed to spawn ally
        self.ally_fire_delay = 1000  # Time between ally shots in milliseconds
        self.last_ally_fire_time = 0  # Track last ally fire time
        
        # Auto-fire settings
        self.auto_fire = False  # Whether auto-fire is active
        self.fire_delay = 200  # Time between auto-fire shots in milliseconds
        self.last_fire_time = 0  # Track last fire time

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

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