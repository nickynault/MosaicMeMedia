# mosaic only

from PIL import Image, ImageTk, ImageGrab
import os
import random

selected_shape = "square"

mosaic_feedback_phrases = [
    "You just crafted a masterpiece! Ready for more?",
    "Your mosaic game is strong! Want another round?",
    "Impressive mosaic skills! How about one more try?",
    "Wow, you're a mosaic maestro! Ready for another creation?",
    "That mosaic is a work of art! Want to try your luck again?",
    "You've got the mosaic magic! Up for another challenge?",
    "Bravo! Your mosaic skills are top-notch. Ready for more fun?",
    "A true mosaic marvel! Want to create another masterpiece?",
    "Your mosaic mojo is unbeatable! Ready for another spin?",
    "Mosaic excellence achieved! Want to give it another shot?"
]


def generate_mosaic(extract_folder, progress_callback=None):
    # Get a list of subfolders within the extracted folder
    valid_images = [file for file in os.listdir(extract_folder) if
                    file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"))]

    if not valid_images:
        raise ValueError("No valid image files found in the 'extracted_images' folder.")

    # Randomly select an image for each tile in the mosaic
    mosaic_size = 550
    tile_size = 50
    rows = columns = mosaic_size // tile_size
    total_tiles = rows * columns

    mosaic = Image.new("RGB", (mosaic_size, mosaic_size))

    for row in range(rows):
        for col in range(columns):
            image_path = os.path.join(extract_folder, random.choice(valid_images))
            tile = Image.open(image_path)
            tile = tile.resize((tile_size, tile_size), Image.BICUBIC)
            mosaic.paste(tile, (col * tile_size, row * tile_size))

            # Update progress for each tile
            if progress_callback:
                progress_callback((row * columns + col + 1) / total_tiles * 100)

    # Convert the mosaic to a Tkinter PhotoImage
    mosaic_photo = ImageTk.PhotoImage(mosaic)

    return mosaic_photo


def random_phrase(phrases):
    chosen_phrase = random.choice(phrases)
    return chosen_phrase


def set_shape(shape):
    global selected_shape
    selected_shape = shape
