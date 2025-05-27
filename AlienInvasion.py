import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from start_screen import StartScreen
from sounds import Sounds
from power_up import PowerUp
from explosion import Explosion
from game_over_screen import GameOverScreen
from ally_ship import AllyShip
import random

class AlienInvasion:

    """Overall class to manage game assets and behavior."""
    def __init__(self):
        " Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
        (self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Dragon Ball Z: Alien Invasion")

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.start_screen = StartScreen(self)
        self.sounds = Sounds()
        self.game_over_screen = GameOverScreen(self)

        self.ship = Ship(self)
        self.ally_ship = None  # Will be initialized when ally is activated
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.last_auto_fire_time = 0
        self.explosions = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars()

        # Set the background color.
        self.bg_color = self.settings.bg_color
        
        # Start background music
        self.sounds.play_background_music()

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                if self.ally_ship:
                    self.ally_ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_stars()
                self._update_power_ups()
                self._check_power_up_collisions()
                self._check_power_up_timers()
                self._handle_auto_fire()
                self._update_ally()
            
            self._update_screen()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (4 * alien_width)  # Increased spacing

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                           (3 * alien_height) - ship_height)
        number_rows = available_space_y // (4 * alien_height)  # Increased vertical spacing

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 4 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = -alien_height * (row_number + 1)
        
        # Randomly assign dive bomber status (25% chance)
        alien.is_dive_bomber = random.random() < 0.25
        
        # Add random movement patterns for non-dive bombers
        if not alien.is_dive_bomber:
            alien.movement_pattern = alien_number % 3  # 0: normal, 1: zigzag, 2: circular
        else:
            alien.movement_pattern = 3  # dive bomber
            
        alien.movement_angle = 0
        alien.original_x = alien.x
        alien.target_y = alien_height + 4 * alien_height * row_number
        
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update(self.stats.level)

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for alien-ally collisions.
        if self.ally_ship and pygame.sprite.spritecollideany(self.ally_ship, self.aliens):
            destroyed = self.ally_ship.take_hit()
            if destroyed:
                self.ally_ship = None
                self.settings.ally_active = False
                self.settings.ally_spawned = False
                # Optionally play a sound or show an effect here

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

        # Check if all aliens have been defeated
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self.ally_bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()
            self.sounds.play_level_up()
            # Reset power-up/ally spawn flags for new level
            self.settings.power_up_spawned = False
            self.settings.ally_spawned = False
            # Start new accuracy tracking for this level
            self.stats.start_new_level()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if not self.stats.game_active:
                self._reset_game()
            else:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group. Ally fires in tandem if present."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self, self.ship)
            self.bullets.add(new_bullet)
            self.sounds.play_ki_blast()
            self.stats.bullets_fired += 1
            # Ally fires in tandem
            if self.ally_ship:
                if len(self.ally_bullets) < self.settings.bullets_allowed:
                    new_ally_bullet = Bullet(self, self.ally_ship)
                    self.ally_bullets.add(new_ally_bullet)
                    self.sounds.play_laser()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()
        self.ally_bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        for bullet in self.ally_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.ally_bullets.remove(bullet)

        # Check for collisions with aliens
        self._check_bullet_alien_collisions()
        self._check_bullet_power_up_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check player bullet collisions
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        # Check ally bullet collisions
        ally_collisions = pygame.sprite.groupcollide(
                self.ally_bullets, self.aliens, True, True)
        
        if collisions or ally_collisions:
            # Handle player bullet collisions
            for aliens in collisions.values():
                for alien in aliens:
                    # Create explosion at alien's position
                    explosion = Explosion(self, alien.rect.center, 'small')
                    self.explosions.add(explosion)
                self.stats.score += self.settings.alien_points * len(aliens)
                self.stats.power_level = self.stats.score
                self.ship.transform(self.stats.power_level)
                self.sounds.play_explosion()
                # Track hits for accuracy
                self.stats.register_hits(len(aliens))
                # Check for power-up and ally thresholds
                self._check_power_up_threshold()
                self._check_ally_threshold()
                
            # Handle ally bullet collisions
            for aliens in ally_collisions.values():
                for alien in aliens:
                    # Create explosion at alien's position
                    explosion = Explosion(self, alien.rect.center, 'small')
                    self.explosions.add(explosion)
                self.stats.score += self.settings.alien_points * len(aliens)
                self.stats.power_level = self.stats.score
                self.ship.transform(self.stats.power_level)
                self.sounds.play_explosion()
                # Track hits for accuracy
                self.stats.register_hits(len(aliens))
                # Check for power-up and ally thresholds
                self._check_power_up_threshold()
                self._check_ally_threshold()
                
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_power_level()
            self.sb.check_high_score()

    def _check_power_up_threshold(self):
        """Check if score has reached power-up threshold."""
        if (self.stats.score >= self.settings.power_up_threshold and 
            not self.settings.power_up_spawned):
            # Spawn a power-up
            power_up = PowerUp(self)
            self.power_ups.add(power_up)
            self.settings.power_up_spawned = True
            # Set next threshold
            self.settings.power_up_threshold += 500
            
    def _check_ally_threshold(self):
        """Check if score has reached ally threshold."""
        if (self.stats.score >= self.settings.ally_threshold and 
            not self.settings.ally_spawned):
            # Create ally ship
            self.ally_ship = AllyShip(self)
            self.settings.ally_spawned = True
            # Set next threshold
            self.settings.ally_threshold += 1000
            
    def _check_bullet_power_up_collisions(self):
        """Check for collisions between bullets and power-ups."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.power_ups, True, True)
            
        for power_ups in collisions.values():
            for power_up in power_ups:
                if power_up.type == 'senzu_bean':
                    # Add an extra life
                    self.stats.ships_left += 1
                    self.sb.prep_ships()
                    self.sounds.play_level_up()  # Use level up sound for senzu bean
                else:
                    self._activate_power_up(power_up.type)
                    
    def _create_stars(self):
        """Create the starfield background."""
        for _ in range(self.settings.star_count):
            star = Star(self)
            self.stars.add(star)

    def _update_stars(self):
        """Update the positions of all stars."""
        self.stars.update()

    def _update_power_ups(self):
        """Update power-up positions and remove those that have gone off screen."""
        self.power_ups.update()
        
        # Remove power-ups that have gone off screen
        for power_up in self.power_ups.copy():
            if power_up.rect.top >= self.settings.screen_height:
                self.power_ups.remove(power_up)

    def _check_power_up_collisions(self):
        """Check for collisions between ship and power-ups."""
        collisions = pygame.sprite.spritecollide(self.ship, self.power_ups, True)
        
        for power_up in collisions:
            self._activate_power_up(power_up.type)

    def _activate_power_up(self, power_up_type):
        """Activate a power-up effect."""
        print(f"Activating power-up: {power_up_type}")
        self.settings.power_up_active = True
        self.settings.power_up_type = power_up_type
        self.settings.power_up_start_time = pygame.time.get_ticks()
        
        if power_up_type == 'large_blast':
            # Increase bullet size
            self.settings.bullet_width = int(self.settings.original_bullet_width * 
                                          self.settings.power_up_types['large_blast']['width_multiplier'])
            self.settings.bullet_height = int(self.settings.original_bullet_height * 
                                           self.settings.power_up_types['large_blast']['height_multiplier'])
            # Play power-up sound
            self.sounds.play_level_up()
            
        elif power_up_type == 'auto_fire':
            # Enable auto-fire
            self.settings.auto_fire = True
            self.settings.last_fire_time = pygame.time.get_ticks()
            # Play power-up sound
            self.sounds.play_level_up()
            
        elif power_up_type == 'ally_help':
            print("Activating ally help power-up")
            self.settings.ally_active = True
            # Create ally ship if it doesn't exist
            if not self.ally_ship:
                print("Creating new ally ship")
                self.ally_ship = AllyShip(self)
            # Initialize ally fire time
            self.settings.last_ally_fire_time = pygame.time.get_ticks()
            # Start firing ally bullets
            self._fire_ally_bullet()
            # Play power-up sound
            self.sounds.play_level_up()
            
    def _check_power_up_timers(self):
        """Check if power-ups have expired."""
        current_time = pygame.time.get_ticks()
        
        if self.settings.power_up_active:
            power_up_type = self.settings.power_up_type
            if power_up_type in self.settings.power_up_types:
                duration = self.settings.power_up_types[power_up_type]['duration']
                if current_time - self.settings.power_up_start_time >= duration:
                    self._deactivate_power_up()
                    
    def _deactivate_power_up(self):
        """Deactivate power-up effects."""
        print(f"Deactivating power-up: {self.settings.power_up_type}")
        if self.settings.power_up_type == 'large_blast':
            # Reset bullet size to original dimensions
            self.settings.bullet_width = self.settings.original_bullet_width
            self.settings.bullet_height = self.settings.original_bullet_height
            
        elif self.settings.power_up_type == 'auto_fire':
            # Disable auto-fire
            self.settings.auto_fire = False
            
        elif self.settings.power_up_type == 'ally_help':
            # Deactivate ally but don't remove the ship
            self.settings.ally_active = False
            print("Deactivating ally help")
            
        self.settings.power_up_active = False
        self.settings.power_up_type = None
        
    def _handle_auto_fire(self):
        """Handle automatic firing for player only (no ally auto-fire)."""
        if self.settings.auto_fire and self.stats.game_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.settings.last_fire_time >= self.settings.power_up_types['auto_fire']['fire_delay']:
                self._fire_bullet()
                self.settings.last_fire_time = current_time

    def _update_ally(self):
        """Update ally position and firing."""
        if self.settings.ally_active:
            # Update ally bullets
            self.ally_bullets.update()
            
            # Remove bullets that have gone off screen
            for bullet in self.ally_bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.ally_bullets.remove(bullet)
                    
            # Check for collisions with aliens
            collisions = pygame.sprite.groupcollide(
                self.ally_bullets, self.aliens, True, True)
            
            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                    self.stats.register_hits(len(aliens))
                self.sb.prep_score()
                self.sb.check_high_score()
                
    def _fire_ally_bullet(self):
        """Create a new bullet and add it to the ally bullets group."""
        if self.ally_ship and len(self.ally_bullets) < self.settings.bullets_allowed:
            print("Creating ally bullet")
            new_bullet = Bullet(self, self.ally_ship)
            self.ally_bullets.add(new_bullet)
            self.sounds.play_laser()
            
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        
        # Draw stars first (background)
        for star in self.stars.sprites():
            pygame.draw.rect(self.screen, star.color, star.rect)
        
        if self.stats.game_active:
            self.ship.blitme()
            if self.ally_ship:
                self.ally_ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.ally_bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.power_ups.draw(self.screen)
            
            # Update and draw explosions
            self.explosions.update()
            for explosion in self.explosions.sprites():
                explosion.draw()
                
            # Draw the score information
            self.sb.show_score()
        else:
            if self.stats.ships_left == 0:
                self.game_over_screen.show()
            else:
                self.start_screen.show_screen()

        pygame.display.flip()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Create explosion at ship's position
            explosion = Explosion(self, self.ship.rect.center, 'large')
            self.explosions.add(explosion)
            
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.power_ups.empty()  # Clear power-ups when ship is hit
            self.ally_bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            if self.ally_ship:
                self.ally_ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.sounds.play_game_over()
            self.sounds.stop_background_music()
            pygame.mouse.set_visible(True)
            # Reset power-up/ally spawn flags for next game
            self.settings.power_up_spawned = False
            self.settings.ally_spawned = False
            # End accuracy tracking
            self.stats.end_game()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Reset alien to top of screen instead of losing a life
                alien._reset_to_top()
                break

    def _reset_game(self):
        """Reset the game to initial state."""
        # Reset game statistics
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_power_level()
        self.sb.prep_ships()
        
        # Reset game settings
        self.settings = Settings()  # Create new settings instance
        
        # Clear all game objects
        self.aliens.empty()
        self.bullets.empty()
        self.ally_bullets.empty()
        self.power_ups.empty()
        self.explosions.empty()
        self.stars.empty()
        
        # Reset ship and ally
        self.ship.center_ship()
        self.ally_ship = None
        
        # Reset power-up and ally flags
        self.settings.power_up_spawned = False
        self.settings.ally_spawned = False
        self.settings.power_up_active = False
        self.settings.power_up_type = None
        self.settings.ally_active = False
        
        # Reset power-up thresholds
        self.settings.power_up_threshold = 500
        self.settings.ally_threshold = 1000
        
        # Reset bullet settings
        self.settings.bullet_width = 8
        self.settings.bullet_height = 25
        
        # Create new fleet and stars
        self._create_fleet()
        self._create_stars()
        
        # Start the game
        self.stats.game_active = True
        pygame.mouse.set_visible(False)
        
        # Restart background music
        self.sounds.stop_background_music()
        self.sounds.play_background_music()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
