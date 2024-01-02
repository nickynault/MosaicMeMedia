# This is the GUI

import tkinter as tk
from tkinter import filedialog
from mosaic import generate_mosaic
import patoolib


# Uploading the images
def upload_images():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Your Zip File!",
                                           filetypes=[("Zip Files", "*.zip"),
                                                      ("RAR Files", "*.rar"),
                                                      ("7zip Files", "*.7z")])

    if file_path:
        extract_images(file_path)


def extract_images(file_path):
    # Implement code to extract images from the archive file and store them in a folder
    extract_folder = "extracted_images"
    patoolib.extract_archive(file_path, outdir=extract_folder)


def create_gui():
    app = tk.Tk()
    app.title("MosaicMeMagic")

    # Add GUI elements here
    upload_button = tk.Button(app, text="Upload Images", command=upload_images)
    upload_button.pack()

    return app
