import pygame.font
import pygame

class StartScreen:
    """A class to manage the start screen."""

    def __init__(self, ai_game):
        """Initialize start screen attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Font settings
        self.title_font = pygame.font.SysFont('impact', 72)  # Changed to Impact font
        self.text_font = pygame.font.SysFont('impact', 48)   # Changed to Impact font
        
        # DBZ-inspired colors
        self.title_color = (255, 215, 0)  # Gold
        self.text_color = (255, 255, 255)  # White
        self.accent_color = (255, 0, 0)    # Red
        
        # Prepare the title and instructions
        self.prep_title()
        self.prep_instructions()
        
        # Create aura effect
        self.aura_radius = 0
        self.aura_growing = True
        self.aura_color = (255, 215, 0, 128)  # Semi-transparent gold

    def prep_title(self):
        """Turn the title into a rendered image."""
        title_str = "DRAGON BALL Z"
        subtitle_str = "ALIEN INVASION"
        
        # Render main title
        self.title_image = self.title_font.render(title_str, True, self.title_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = 100
        
        # Render subtitle
        self.subtitle_image = self.title_font.render(subtitle_str, True, self.accent_color)
        self.subtitle_rect = self.subtitle_image.get_rect()
        self.subtitle_rect.centerx = self.screen_rect.centerx
        self.subtitle_rect.top = self.title_rect.bottom + 10

    def prep_instructions(self):
        """Turn the instructions into rendered images."""
        instructions = [
            "CONTROLS:",
            "← → ARROW KEYS: MOVE",
            "SPACEBAR: FIRE KI BLAST",
            "Q: QUIT GAME",
            "",
            "PRESS SPACE TO START"
        ]
        
        self.instruction_images = []
        self.instruction_rects = []
        
        for i, instruction in enumerate(instructions):
            # Make the last line (start instruction) gold and larger
            if i == len(instructions) - 1:
                image = self.title_font.render(instruction, True, self.title_color)
            else:
                image = self.text_font.render(instruction, True, self.text_color)
                
            rect = image.get_rect()
            rect.centerx = self.screen_rect.centerx
            rect.top = self.subtitle_rect.bottom + 50 + (i * 40)
            self.instruction_images.append(image)
            self.instruction_rects.append(rect)

    def show_screen(self):
        """Show the start screen."""
        # Update aura effect
        if self.aura_growing:
            self.aura_radius += 0.5
            if self.aura_radius >= 100:
                self.aura_growing = False
        else:
            self.aura_radius -= 0.5
            if self.aura_radius <= 50:
                self.aura_growing = True
        
        # Draw aura
        aura_surface = pygame.Surface((self.screen_rect.width, self.screen_rect.height), pygame.SRCALPHA)
        pygame.draw.circle(aura_surface, self.aura_color, 
                         (self.screen_rect.centerx, self.screen_rect.centery),
                         int(self.aura_radius))
        self.screen.blit(aura_surface, (0, 0))
        
        # Draw title with shadow effect
        shadow_offset = 3
        title_shadow = self.title_font.render("DRAGON BALL Z", True, (0, 0, 0))
        shadow_rect = self.title_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(self.title_image, self.title_rect)
        
        # Draw subtitle with shadow
        subtitle_shadow = self.title_font.render("ALIEN INVASION", True, (0, 0, 0))
        shadow_rect = self.subtitle_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        self.screen.blit(subtitle_shadow, shadow_rect)
        self.screen.blit(self.subtitle_image, self.subtitle_rect)
        
        # Draw instructions
        instructions = [
            "CONTROLS:",
            "← → ARROW KEYS: MOVE",
            "SPACEBAR: FIRE KI BLAST",
            "Q: QUIT GAME",
            "",
            "PRESS SPACE TO START"
        ]
        
        for i, (image, rect) in enumerate(zip(self.instruction_images, self.instruction_rects)):
            # Add shadow to instructions
            if i == len(self.instruction_images) - 1:  # Last instruction (start message)
                shadow = self.title_font.render("PRESS SPACE TO START", True, (0, 0, 0))
                shadow_rect = rect.copy()
                shadow_rect.x += shadow_offset
                shadow_rect.y += shadow_offset
                self.screen.blit(shadow, shadow_rect)
            else:
                shadow = self.text_font.render(instructions[i], True, (0, 0, 0))
                shadow_rect = rect.copy()
                shadow_rect.x += shadow_offset
                shadow_rect.y += shadow_offset
                self.screen.blit(shadow, shadow_rect)
            self.screen.blit(image, rect) 