from PIL import Image
import os

def extract_sprites(sheet_path, num_cols, num_rows, output_folder):
    """Extracts individual sprites from a sprite sheet based on grid layout."""
    sprite_sheet = Image.open(sheet_path)
    os.makedirs(output_folder, exist_ok=True)
    
    sheet_width, sheet_height = sprite_sheet.size
    sprite_width = sheet_width // num_cols
    sprite_height = sheet_height // num_rows
    
    frames = []
    for row in range(num_rows):
        for col in range(num_cols):
            box = (
                col * sprite_width,
                row * sprite_height,
                (col + 1) * sprite_width,
                (row + 1) * sprite_height
            )
            sprite = sprite_sheet.crop(box)
            sprite_path = os.path.join(output_folder, f"frame_{row}_{col}.png")
            sprite.save(sprite_path)
            frames.append(sprite_path)
    
    print(f"Extracted {len(frames)} frames from {sheet_path} into {output_folder}")
    return frames

# 🔧 **Set the correct number of columns and rows in your sprite sheet**
num_cols = 4  # Update based on your sheet
num_rows = 1  # Update based on your sheet

# Extract sprites
extract_sprites("zombiewalk_flipped.png", num_cols, num_rows, "zombiewalkright")
