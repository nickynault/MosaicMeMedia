# This is the GUI

import tkinter as tk
from tkinter import filedialog
from mosaic import *
import patoolib

mosaic_description: tk.StringVar


# Uploading the images
def upload_images():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Your Zip File!",
                                           filetypes=[("Zip Files", "*.zip"),
                                                      ("RAR Files", "*.rar"),
                                                      ("7zip Files", "*.7z")])

    if file_path:
        extract_images(file_path)


def extract_images(file_path):
    global mosaic_description
    
    # Implement code to extract images from the archive file and store them in a folder
    extract_folder = "extracted_images"
    patoolib.extract_archive(file_path, outdir=extract_folder)

    mosaic_description.set(random_phrase(mosaic_feedback_phrases))    # changes phrases randomly after upload


def create_gui():
    global mosaic_description
    
    app = tk.Tk()
    app.title("MosaicMeMagic")
    app.geometry("800x800")
    app.configure(bg="#f0f0f0")

    # Add GUI elements here
    label = tk.Label(app, text="Welcome to MosaicMeMagic!", font=("Arial", 20), bg="#f0f0f0", pady=10)
    label.pack(side="top")

    mosaic_description = tk.StringVar()
    mosaic_description.set("Upload a zipped '.zip', '.7z', or '.rar' folder with some images inside. \nYour mosaic will appear here.")

    mosaic_label = tk.Label(app, textvariable=mosaic_description, bg="#f0f0f0", pady=10, font=("Arial", 15))
    mosaic_label.pack(side="top")
    
    upload_button = tk.Button(app, text="Upload Images", command=upload_images)
    upload_button.pack()

    return app
