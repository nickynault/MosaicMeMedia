# This is the GUI

import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import patoolib

from mosaic import *

mosaic_description: tk.StringVar
mosaic_display: tk.Label
download_button: tk.Button
app: tk.Tk
loading_bar: tk.ttk.Progressbar
shape_dropdown: ttk.Combobox

VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".PNG", ".bmp", ".gif", ".tiff", ".webp"}


def download_mosaic():
    global app, mosaic_display, download_button

    try:
        # Take a screenshot of the area containing the mosaic
        screenshot = ImageGrab.grab(bbox=(app.winfo_rootx() + mosaic_display.winfo_x(),
                                          app.winfo_rooty() + mosaic_display.winfo_y(),
                                          app.winfo_rootx() + mosaic_display.winfo_x() + mosaic_display.winfo_width(),
                                          app.winfo_rooty() + mosaic_display.winfo_y() + mosaic_display.winfo_height()))

        # Save the screenshot as a PNG file
        save_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'mosaic.png')
        screenshot.save(save_path, 'PNG')

        messagebox.showinfo("Download Complete", f"Mosaic successfully downloaded to {save_path}")

        # Show the download button after successfully capturing the mosaic
        download_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


# Check if the images inside the zipped folder are actual valid images
def is_valid_image(file_path):
    try:
        Image.open(file_path)
        return True
    except Exception:
        return False


# Uploading the images
def upload_images():
    global mosaic_display, download_button, shape_dropdown

    # Check if extracted_images folder exists and delete its contents
    extracted_folder_path = "extracted_images"
    if os.path.exists(extracted_folder_path):
        shutil.rmtree(extracted_folder_path)

    file_path = filedialog.askopenfilename(initialdir="/", title="Select Your Zip File!",
                                           filetypes=[("Zip Files", "*.zip"),
                                                      ("RAR Files", "*.rar"),
                                                      ("7zip Files", "*.7z")])

    if file_path:
        if not file_path.lower().endswith((".zip", ".rar", ".7z")):
            messagebox.showerror("Error",
                                 "Please select a valid archive file (zip, rar, 7z).")  # shouldn't need this. but just in case
        elif not shape_dropdown.get():
            messagebox.showerror("Error", "Please select a shape!")
        else:
            extract_images(file_path)
            create_download_button()


def create_download_button():
    global download_button

    # Create a download button (initially hidden)
    download_button = tk.Button(app, text="Download", command=download_mosaic)
    download_button.grid(pady=20)


def update_loading_bar():
    global loading_bar

    loading_bar.grid()  # Pack the loading bar before starting it
    loading_bar['mode'] = 'determinate'  # Change mode to 'determinate'

    def progress_callback(progress):
        loading_bar['value'] = progress
        loading_bar.update()

    # Generate the mosaic with a loading bar
    generate_mosaic("extracted_images", progress_callback)

    loading_bar['mode'] = 'indeterminate'  # Change mode back to 'indeterminate'


def extract_images(file_path):
    global mosaic_description, mosaic_display, loading_bar

    try:
        # Create a folder to extract images
        extract_folder = "extracted_images"
        os.makedirs(extract_folder, exist_ok=True)

        # Extract images from the archive file
        patoolib.extract_archive(file_path, outdir=extract_folder)

        # Move images directly to 'extracted_images' folder
        subfolders = [subfolder for subfolder in os.listdir(extract_folder) if
                      os.path.isdir(os.path.join(extract_folder, subfolder))]

        if subfolders:
            subfolder_path = os.path.join(extract_folder, subfolders[0])
            for file in os.listdir(subfolder_path):
                source_path = os.path.join(subfolder_path, file)
                destination_path = os.path.join(extract_folder, file)
                shutil.move(source_path, destination_path)

            # Remove the now empty subfolder
            os.rmdir(subfolder_path)

        # Check if the extracted folder is not empty
        files_in_folder = os.listdir(extract_folder)

        if not files_in_folder:
            raise FileNotFoundError("No files found in the extracted folder.")

        # Generate a loading bar
        update_loading_bar()

        # Generate the mosaic
        mosaic_photo = generate_mosaic(extract_folder)

        # Update the mosaic description
        mosaic_description.set(random_phrase(mosaic_feedback_phrases))

        # Update the mosaic_display label to show the generated mosaic
        mosaic_display.config(image=mosaic_photo)
        mosaic_display.image = mosaic_photo  # Keep a reference to avoid garbage collection

        # Hide loading bar after completion
        loading_bar.grid_forget()

    except FileNotFoundError:
        messagebox.showerror("Extraction Error", "The extracted folder is empty.")
    except patoolib.util.PatoolError as e:
        messagebox.showerror("Extraction Error", f"An error occurred during extraction: {str(e)}")
    except ValueError as e:
        messagebox.showerror("Validation Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


def create_gui():
    global mosaic_description, mosaic_display, app, \
        loading_bar, selected_shape, shape_dropdown

    app = tk.Tk()
    app.title("MosaicMeMagic")
    app.geometry("1000x800")
    app.configure(bg="#f0f0f0")

    # Add GUI elements here
    label = tk.Label(app, text="Welcome to MosaicMeMagic!", font=("Arial", 20), bg="#f0f0f0", pady=10)
    label.grid(row=0, column=0, padx=150)

    mosaic_description = tk.StringVar()
    mosaic_description.set(
        "Upload a zipped '.zip', '.7z', or '.rar' folder with some images inside. \nYour mosaic will appear here.")

    mosaic_label = tk.Label(app, textvariable=mosaic_description, bg="#f0f0f0", pady=10, font=("Arial", 15))
    mosaic_label.grid()

    upload_button = tk.Button(app, text="Upload Images", command=upload_images)
    upload_button.grid(pady=20)

    mosaic_display = tk.Label(app, text="", font=("Arial", 15), bg="#f0f0f0")
    mosaic_display.grid()

    loading_bar = tk.ttk.Progressbar(app, length=200, mode="indeterminate")
    loading_bar.grid_forget()

    # Set custom color to differentiate between the columns
    customize_frame = tk.Frame(app, bg='#e0e0e0', bd=0)  # Replace '#e0e0e0' with your desired color
    customize_frame.grid(row=0, column=1, rowspan=100, sticky='ns')  # Adjust rowspan as needed

    customize_label = tk.Label(customize_frame, text="Customize Your Mosaic", font=("Arial", 15))
    customize_label.grid(row=2, column=1, padx=10, pady=180, sticky='w')

    # Dropdown menu for selecting shape
    shape_label = tk.Label(app, text="Select Shape:", bg="#f0f0f0", font=("Arial", 12))
    shape_label.grid(row=4, column=1, padx=65, pady=10, sticky="w")

    shapes = ["Square", "Triangle", "Circle", "Pentagon"]
    shape_var = tk.StringVar(app)
    shape_var.set("Square")  # Default to Square

    shape_dropdown = ttk.Combobox(app, textvariable=shape_var, values=shapes, state="readonly")
    shape_dropdown.grid(row=5, column=1, padx=50, pady=10, sticky="e")

    return app
