import pygame.font

class StartScreen:
    """A class to manage the start screen."""

    def __init__(self, ai_game):
        """Initialize start screen attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Font settings
        self.title_font = pygame.font.SysFont(None, 72)
        self.text_font = pygame.font.SysFont(None, 48)
        self.text_color = (255, 255, 0)  # DBZ yellow

        # Prepare the title and instructions
        self.prep_title()
        self.prep_instructions()

    def prep_title(self):
        """Turn the title into a rendered image."""
        title_str = "Dragon Ball Z: Alien Invasion"
        self.title_image = self.title_font.render(title_str, True, self.text_color)
        
        # Position the title at the top center of the screen
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = 100

    def prep_instructions(self):
        """Turn the instructions into rendered images."""
        instructions = [
            "Controls:",
            "Left/Right Arrow Keys: Move",
            "Spacebar: Fire Ki Blast",
            "Q: Quit Game",
            "",
            "Press SPACE to Start"
        ]
        
        self.instruction_images = []
        self.instruction_rects = []
        
        for i, instruction in enumerate(instructions):
            image = self.text_font.render(instruction, True, self.text_color)
            rect = image.get_rect()
            rect.centerx = self.screen_rect.centerx
            rect.top = self.title_rect.bottom + 50 + (i * 40)
            self.instruction_images.append(image)
            self.instruction_rects.append(rect)

    def show_screen(self):
        """Draw the start screen."""
        # Draw title
        self.screen.blit(self.title_image, self.title_rect)
        
        # Draw instructions
        for image, rect in zip(self.instruction_images, self.instruction_rects):
            self.screen.blit(image, rect) 