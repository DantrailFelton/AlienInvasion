import os
import requests

def download_file(url, filename):
    """Download a file from a URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

def main():
    # Create sounds directory if it doesn't exist
    if not os.path.exists('sounds'):
        os.makedirs('sounds')

    # Only background music can be downloaded directly
    sounds = {
        'background_music.ogg': 'https://opengameart.org/sites/default/files/8-bit-dungeon-boss.ogg'
    }

    # Download each sound file
    for filename, url in sounds.items():
        filepath = os.path.join('sounds', filename)
        download_file(url, filepath)

    print("\nFor other sound effects, please download the following packs and extract the OGG files:")
    print("- Ki Blast: Kenney Sci-fi Sounds (https://kenney.nl/assets/sci-fi-sounds) -> e.g. sciFiWeapon1.ogg")
    print("- Explosion: Kenney Impact Sounds (https://kenney.nl/assets/impact-sounds) -> e.g. impactSoft_medium_001.ogg")
    print("- Level Up: Kenney UI Audio (https://kenney.nl/assets/ui-audio) -> e.g. notification_003.ogg")
    print("- Game Over: Kenney UI Audio (https://kenney.nl/assets/ui-audio) -> e.g. notification_004.ogg")
    print("Place the selected OGG files in your 'sounds' directory and rename them as needed.")

if __name__ == '__main__':
    main() 