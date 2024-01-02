# This is the GUI

import tkinter as tk
from tkinter import filedialog
from mosaic import *
import patoolib

mosaic_description: tk.StringVar

# Check if the images inside the zipped folder are actual valid images
def is_valid_image(file_path):
    try:
        Image.open(file_path)
        return True
    except Exception as e:
        return False
        

# Uploading the images
def upload_images():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Your Zip File!",
                                           filetypes=[("Zip Files", "*.zip"),
                                                      ("RAR Files", "*.rar"),
                                                      ("7zip Files", "*.7z")])

    if file_path:
        if not file_path.lower().endswith((".zip", ".rar", ".7z")):
            messagebox.showerror("Error", "Please select a valid archive file (zip, rar, 7z).")  # shouldn't need this. but just in case
        else:
            extract_images(file_path)


def extract_images(file_path):
    global mosaic_description
    
    try:
        # Create a folder to extract images
        extract_folder = "extracted_images"
        os.makedirs(extract_folder, exist_ok=True)

        # Extract images from the archive file
        patoolib.extract_archive(file_path, outdir=extract_folder)

        # Check if the extracted folder is NOT empty
        files_in_folder = os.listdir(extract_folder)
        if not files_in_folder:
            raise FileNotFoundError("The extracted folder is empty.")

        # Check if the extracted folder contains valid image files
        valid_images = [file for file in files_in_folder if file.lower().endswith(tuple(VALID_IMAGE_EXTENSIONS))]
        if not valid_images:
            raise ValueError("The extracted folder does not contain valid image files.")

        # Update the mosaic description
        mosaic_description.set(random_phrase(mosaic_feedback_phrases))

    except FileNotFoundError:
        messagebox.showerror("Extraction Error", "The extracted folder is empty.")
    except patoolib.util.PatoolError as e:
        messagebox.showerror("Extraction Error", f"An error occurred during extraction: {str(e)}")
    except ValueError as e:
        messagebox.showerror("Validation Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


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
