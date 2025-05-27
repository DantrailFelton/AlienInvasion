import pygame

class GameOverScreen:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

    def show(self):
        self.screen.fill((0, 0, 0))
        # Title
        title = self.font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title.get_rect(center=(self.screen_rect.centerx, 80))
        self.screen.blit(title, title_rect)
        # Final score
        score_text = self.small_font.render(f"Final Score: {self.stats.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (80, 160))
        # Highest level
        level_text = self.small_font.render(f"Highest Level: {self.stats.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (80, 200))
        # Accuracy per level
        y = 250
        total_hits = 0
        total_bullets = 0
        for level, accuracy, bullets, hits in self.stats.level_accuracies:
            acc_percent = int(accuracy * 100) if bullets > 0 else 0
            acc_text = self.small_font.render(
                f"Level {level}: {acc_percent}% ({hits}/{bullets})", True, (200, 200, 0))
            self.screen.blit(acc_text, (80, y))
            y += 32
            total_hits += hits
            total_bullets += bullets
        # Total accuracy
        if total_bullets > 0:
            total_acc = int(total_hits / total_bullets * 100)
        else:
            total_acc = 0
        total_acc_text = self.small_font.render(
            f"Total Accuracy: {total_acc}% ({total_hits}/{total_bullets})", True, (0, 200, 0))
        self.screen.blit(total_acc_text, (80, y + 16))
        # Instructions
        instr = self.small_font.render("Press SPACE to restart", True, (180, 180, 180))
        self.screen.blit(instr, (80, y + 64))
        pygame.display.flip() 