import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Path to a single image for testing
image_path = "/Users/nynor/CODE/Nynor-code/projects/x_ray_labeling/data/Bone_fracture2.v1i/train/Fractured/IMG0002449_jpg.rf.71486b3de332600c0d571fec1e192d30.jpg"

def show_image():
    root = tk.Tk()
    root.title("X-Ray Image Test")

    # Create a canvas to display the image
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    try:
        img = Image.open(image_path)
        img.thumbnail((500, 500))  # Resize while keeping aspect ratio

        photo = ImageTk.PhotoImage(img)
        print(f"Opening image: {image_path}")
        print(f"Image size: {img.size}")
        print(f"Image mode: {img.mode}")

        canvas.create_image(250, 250, image=photo)  # Center image on canvas
        print("Image displayed on canvas")

        # Keep a reference to the image object to prevent garbage collection
        canvas.image = photo

        # Force update of Tkinter window
        root.update()

        root.mainloop()  # Start Tkinter main loop
    except Exception as e:
        print(f"Error loading {image_path}: {e}")

if __name__ == "__main__":
    show_image()
