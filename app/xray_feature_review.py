import os
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

os.environ["TK_SILENCE_DEPRECATION"] = "1"

# Configuration
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(ROOT_DIR, "data/Bone_fracture2.v1i/train")
OUTPUT_FILE = os.path.join(ROOT_DIR, "data/", "xray_review_results.csv")

def get_xray_images(root_dir):
    """Retrieve all X-ray images and their associated features."""
    xray_images = []
    for feature in os.listdir(root_dir):
        feature_path = os.path.join(root_dir, feature)
        if os.path.isdir(feature_path):
            for image_file in os.listdir(feature_path):
                if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    xray_images.append((feature, os.path.join(feature_path, image_file)))
    return xray_images

class XRayReviewer:
    def __init__(self, root, images):
        self.root = root
        self.images = images
        self.index = 0
        self.responses = []

        self.root.title("X-Ray Feature Review")
        self.label = tk.Label(root, text="Feature: ", font=("Arial", 16))
        self.label.pack()

        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.btn_correct = tk.Button(root, text="Feature Correct", command=lambda: self.record_response("Correct"))
        self.btn_correct.pack(side=tk.LEFT, expand=True)
        
        self.btn_incomplete = tk.Button(root, text="Feature Incomplete", command=lambda: self.record_response("Incomplete"))
        self.btn_incomplete.pack(side=tk.LEFT, expand=True)
        
        self.btn_normal = tk.Button(root, text="Normal", command=lambda: self.record_response("Normal"))
        self.btn_normal.pack(side=tk.LEFT, expand=True)

        self.show_image()

    def show_image(self):
        if self.index >= len(self.images):
            self.save_results()
            messagebox.showinfo("Done", "Review complete!")
            self.root.quit()  # End the Tkinter loop
            return

        feature, img_path = self.images[self.index]
        self.label.config(text=f"Feature: {feature}")

        try:
            img = Image.open(img_path)
            img.thumbnail((500, 500))  # Resize while keeping aspect ratio

            self.photo = ImageTk.PhotoImage(img)  # Convert to Tkinter format
            print(f"Opening image: {img_path}")
            print(f"Image size: {img.size}")
            print(f"Image mode: {img.mode}")

            self.canvas.delete("all")  # Clear previous image
            self.canvas.create_image(250, 250, image=self.photo)  # Center image on canvas
            print(f"Image displayed on canvas")

            # Store reference to the image object to prevent garbage collection
            self.canvas.image = self.photo  # Keeping a reference here

            # Force update of the Tkinter canvas
            self.root.after(100, self.root.update_idletasks)
            self.root.after(100, self.root.update)

        except Exception as e:
            print(f"Error loading {img_path}: {e}")

    def record_response(self, response):
        try:
            # Log or process the response
            print(f"Response recorded: {response}")
        
            # update the response list
            feature, img_path = self.images[self.index]
            self.responses.append([feature, img_path, response])
            self.index += 1
        
            # Update UI
            self.show_image()
            
        except tk.TclError as e:
            print(f"Error updating UI: {e}")

    def save_results(self):
        with open(OUTPUT_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Feature", "Image Path", "Response"])
            writer.writerows(self.responses)

if __name__ == "__main__":
    images = get_xray_images(DATA_DIR)
    
    if not images:
        print(DATA_DIR)
        print("No images found in the specified directory.")
    else:
        print(f"Found {len(images)} images.")
        root = tk.Tk()
        app = XRayReviewer(root, images)
        root.mainloop()
