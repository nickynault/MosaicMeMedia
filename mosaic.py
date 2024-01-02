# mosaic only

from PIL import Image
import os
import random

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


def generate_mosaic(images_folder, base_image_path, tile_size):
    # Implement code to generate mosaic from images in new folder
    pass

def random_phrase(phrases):
    chosen_phrase = random.choice(phrases)
    return chosen_phrase
