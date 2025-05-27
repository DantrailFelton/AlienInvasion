import pygame

class Sounds:
    """A class to manage game sounds."""
    
    def __init__(self):
        """Initialize sound settings."""
        try:
            pygame.mixer.init()
            # Load sound effects
            self.ki_blast = pygame.mixer.Sound('sounds/ki_blast.wav')
            self.explosion = pygame.mixer.Sound('sounds/explosion.wav')
            self.level_up = pygame.mixer.Sound('sounds/level_up.wav')
            self.game_over = pygame.mixer.Sound('sounds/game_over.wav')
            # Set volume for each sound
            self.ki_blast.set_volume(0.3)
            self.explosion.set_volume(0.4)
            self.level_up.set_volume(0.5)
            self.game_over.set_volume(0.5)
            # Load and set up background music
            pygame.mixer.music.load('sounds/background_music.wav')
            pygame.mixer.music.set_volume(0.2)
        except Exception as e:
            print(f"Error loading sound files: {e}")
            print("Continuing without sound effects...")
            self.ki_blast = DummySound()
            self.explosion = DummySound()
            self.level_up = DummySound()
            self.game_over = DummySound()
    
    def play_ki_blast(self):
        self.ki_blast.play()
    def play_explosion(self):
        self.explosion.play()
    def play_level_up(self):
        self.level_up.play()
    def play_game_over(self):
        self.game_over.play()
    def play_background_music(self):
        try:
            pygame.mixer.music.play(-1)
        except:
            pass
    def stop_background_music(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass
    def play_laser(self):
        self.play_ki_blast()

class DummySound:
    def play(self):
        pass 