import pygame

def create_ship():
    # Create a surface for Goku's ship (64x64 pixels)
    ship_surface = pygame.Surface((64, 64))
    ship_surface.fill((0, 0, 0))  # Fill with black for transparency
    ship_surface.set_colorkey((0, 0, 0))  # Make black transparent

    # Draw ship body (orange gi color)
    pygame.draw.polygon(ship_surface, (255, 140, 0), [
        (32, 10),   # Top point
        (10, 54),   # Bottom left
        (54, 54)    # Bottom right
    ])
    
    # Draw spiky hair (black)
    spikes = [
        [(32, 10), (25, 0), (32, 15)],   # Left spike
        [(32, 10), (32, 0), (32, 15)],   # Middle spike
        [(32, 10), (39, 0), (32, 15)],   # Right spike
    ]
    for spike in spikes:
        pygame.draw.polygon(ship_surface, (30, 30, 30), spike)
    
    # Add gi belt (blue)
    pygame.draw.rect(ship_surface, (0, 0, 255), (24, 40, 16, 4))
    
    return ship_surface

def create_ssj_ship():
    # Create a surface for Super Saiyan Goku's ship
    ship_surface = pygame.Surface((64, 64))
    ship_surface.fill((0, 0, 0))
    ship_surface.set_colorkey((0, 0, 0))

    # Draw ship body (orange gi color)
    pygame.draw.polygon(ship_surface, (255, 140, 0), [
        (32, 10),
        (10, 54),
        (54, 54)
    ])
    
    # Draw spiky hair (gold)
    spikes = [
        [(32, 10), (25, 0), (32, 15)],
        [(32, 10), (32, 0), (32, 15)],
        [(32, 10), (39, 0), (32, 15)],
    ]
    for spike in spikes:
        pygame.draw.polygon(ship_surface, (255, 215, 0), spike)
    
    # Add gi belt (blue)
    pygame.draw.rect(ship_surface, (0, 0, 255), (24, 40, 16, 4))
    
    # Add aura effect (yellow)
    pygame.draw.circle(ship_surface, (255, 255, 0), (32, 32), 30, 2)
    
    return ship_surface

def create_ssj2_ship():
    # Create a surface for Super Saiyan 2 Goku's ship
    ship_surface = pygame.Surface((64, 64))
    ship_surface.fill((0, 0, 0))
    ship_surface.set_colorkey((0, 0, 0))

    # Draw ship body (orange gi color)
    pygame.draw.polygon(ship_surface, (255, 140, 0), [
        (32, 10),
        (10, 54),
        (54, 54)
    ])
    
    # Draw spiky hair (gold with lightning)
    spikes = [
        [(32, 10), (25, 0), (32, 15)],
        [(32, 10), (32, 0), (32, 15)],
        [(32, 10), (39, 0), (32, 15)],
    ]
    for spike in spikes:
        pygame.draw.polygon(ship_surface, (255, 215, 0), spike)
    
    # Add lightning effects
    lightning = [
        [(25, 0), (20, -5), (25, 5)],
        [(39, 0), (44, -5), (39, 5)],
    ]
    for bolt in lightning:
        pygame.draw.polygon(ship_surface, (255, 255, 255), bolt)
    
    # Add gi belt (blue)
    pygame.draw.rect(ship_surface, (0, 0, 255), (24, 40, 16, 4))
    
    # Add aura effect (yellow with white)
    pygame.draw.circle(ship_surface, (255, 255, 0), (32, 32), 30, 2)
    pygame.draw.circle(ship_surface, (255, 255, 255), (32, 32), 28, 1)
    
    return ship_surface

def create_ssj3_ship():
    # Create a surface for Super Saiyan 3 Goku's ship
    ship_surface = pygame.Surface((64, 64))
    ship_surface.fill((0, 0, 0))
    ship_surface.set_colorkey((0, 0, 0))

    # Draw ship body (orange gi color)
    pygame.draw.polygon(ship_surface, (255, 140, 0), [
        (32, 10),
        (10, 54),
        (54, 54)
    ])
    
    # Draw long spiky hair (gold)
    long_spikes = [
        [(32, 10), (25, -10), (32, 15)],
        [(32, 10), (32, -15), (32, 15)],
        [(32, 10), (39, -10), (32, 15)],
    ]
    for spike in long_spikes:
        pygame.draw.polygon(ship_surface, (255, 215, 0), spike)
    
    # Add gi belt (blue)
    pygame.draw.rect(ship_surface, (0, 0, 255), (24, 40, 16, 4))
    
    # Add aura effect (yellow with white and blue)
    pygame.draw.circle(ship_surface, (255, 255, 0), (32, 32), 30, 2)
    pygame.draw.circle(ship_surface, (255, 255, 255), (32, 32), 28, 1)
    pygame.draw.circle(ship_surface, (0, 0, 255), (32, 32), 26, 1)
    
    return ship_surface

def create_alien():
    # Create a surface for Frieza-style alien (48x48 pixels)
    alien_surface = pygame.Surface((48, 48))
    alien_surface.fill((0, 0, 0))  # Fill with black for transparency
    alien_surface.set_colorkey((0, 0, 0))  # Make black transparent

    # Draw Frieza-style head (white with purple)
    pygame.draw.ellipse(alien_surface, (255, 255, 255), (8, 8, 32, 24))  # White base
    pygame.draw.ellipse(alien_surface, (160, 32, 240), (4, 4, 40, 16))   # Purple top

    # Draw eyes (red)
    pygame.draw.circle(alien_surface, (255, 0, 0), (16, 20), 3)
    pygame.draw.circle(alien_surface, (255, 0, 0), (32, 20), 3)
    
    # Draw horns (white with purple tips)
    pygame.draw.polygon(alien_surface, (255, 255, 255), [
        (8, 12),    # Left horn base
        (0, 4),     # Left horn tip
        (16, 12)    # Left horn bottom
    ])
    pygame.draw.polygon(alien_surface, (255, 255, 255), [
        (32, 12),   # Right horn base
        (48, 4),    # Right horn tip
        (40, 12)    # Right horn bottom
    ])
    
    # Purple horn tips
    pygame.draw.circle(alien_surface, (160, 32, 240), (0, 4), 3)
    pygame.draw.circle(alien_surface, (160, 32, 240), (48, 4), 3)
    
    return alien_surface

def main():
    pygame.init()
    
    # Create the images
    ship = create_ship()
    ship_ssj = create_ssj_ship()
    ship_ssj2 = create_ssj2_ship()
    ship_ssj3 = create_ssj3_ship()
    alien = create_alien()
    
    # Save the images
    pygame.image.save(ship, 'images/ship.bmp')
    pygame.image.save(ship_ssj, 'images/ship_ssj.bmp')
    pygame.image.save(ship_ssj2, 'images/ship_ssj2.bmp')
    pygame.image.save(ship_ssj3, 'images/ship_ssj3.bmp')
    pygame.image.save(alien, 'images/alien.bmp')
    
    pygame.quit()

if __name__ == '__main__':
    main() 