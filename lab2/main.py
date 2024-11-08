import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

def open_image():
    global image
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Select an image",
        filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("all files", "*.*")),
    )
    if filepath:
        image = cv2.imread(filepath)
        cv2.imshow("Original Image", image)

def process_image(method1, method2):
    global image
    if image is None:
        return
    processed_image = image.copy()  # Work on a copy of the image

    # --- Method 1 Implementations ---
    if method1 == 1:
        # Histogram Equalization + Linear Contrast Stretching
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.equalizeHist(gray)
    elif method1 == 6:
        # Global Thresholding (Method 1)
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        _, processed_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    elif method1 == 7: 
        # Global Thresholding (Method 2 - Otsu's)
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        _, processed_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method1 == 11: 
        # Adaptive Thresholding (Method 1 - Mean)
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    elif method1 == 12:
        # Adaptive Thresholding (Method 2 - Gaussian)
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # ... (Implement other method1 options: 16, 17)

    # --- Method 2 Implementations ---
    if method2 == 2:
        # Low Pass - Gaussian Blur
        processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
    elif method2 == 3:
        # High Pass - Laplacian (for edge detection)
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.Laplacian(gray, cv2.CV_64F)
        processed_image = np.uint8(np.absolute(processed_image)) # Convert back to 8-bit
    elif method2 == 4:
        # Segmentation - Canny Edge Detection 
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.Canny(gray, 100, 200) 
    # ... (Implement other method2 options: 5, 8, 9, 10, 13, 14, 15, 18, 19, 20)

    cv2.imshow("Processed Image", processed_image)

# --- Tkinter GUI Setup --- 
root = tk.Tk()
root.title("Image Processing App")

image = None 

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=10)

# Add buttons for all your method combinations 
# (Example for a few combinations):
process_button_2_4 = tk.Button(root, text="Process (2 & 4)", command=lambda: process_image(2, 4))
process_button_2_4.pack()

process_button_7_3 = tk.Button(root, text="Process (7 & 3)", command=lambda: process_image(7, 3))
process_button_7_3.pack()

# Add more buttons for other method combinations... 

root.mainloop()