import os
import pytesseract
from PIL import Image, ImageTk, ImageOps, ImageEnhance
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from docx import Document
import cv2
import numpy as np

class ImageViewerWithOCR:
    def __init__(self, root):
        self.root = root
        self.root.title("The Images")
        self.root.geometry("800x600")
        self.root.config(bg='black')

        # Canvas for image display
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Variables for images and OCR result
        self.img_original = None
        self.img_display = None
        self.images = []
        self.current_image_index = 0
        self.zoom_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Set up keyboard shortcuts
        self.root.bind("<Control-o>", lambda event: self.load_folder_or_file())
        self.root.bind("<Control-w>", lambda event: self.perform_ocr())
        self.root.bind("<Left>", lambda event: self.toggle_image(-1))
        self.root.bind("<Right>", lambda event: self.toggle_image(1))
        self.root.bind("<Up>", self.reset_zoom)
        self.root.bind("<Down>", self.zoom_out)
        
        # Mouse wheel for zooming
        self.canvas.bind("<MouseWheel>", self.zoom)

        # Menu Bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Folder (Ctrl + O)", command=self.load_folder_or_file)
        self.file_menu.add_command(label="Perform OCR (Ctrl + W)", command=self.perform_ocr)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Add more options in the menu for zoom and pan
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Zoom In (Up Arrow)", command=self.zoom_in)
        self.edit_menu.add_command(label="Zoom Out (Down Arrow)", command=self.zoom_out)
        self.edit_menu.add_command(label="Pan", command=self.start_pan)

    def load_folder_or_file(self):
        """Load a folder or open an individual image file."""
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))]
            if self.images:
                self.current_image_index = 0
                self.load_image()
            else:
                messagebox.showwarning("No Images", "No images found in the selected folder.")
        else:
            file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")])
            if file_path:
                self.images = [file_path]  # Treat the selected file as the only image
                self.current_image_index = 0
                self.load_image()

    def load_image(self):
        """Load and display the current image."""
        if self.images:
            self.img_original = Image.open(self.images[self.current_image_index])
            self.zoom_scale = 1.0  # Reset zoom scale
            self.offset_x = 0  # Reset pan offset
            self.offset_y = 0  # Reset pan offset
            self.display_image()

    def display_image(self):
        """Display the current image on the canvas."""
        img = self.img_original.resize((int(self.img_original.width * self.zoom_scale), int(self.img_original.height * self.zoom_scale)))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete(tk.ALL)  # Clear the canvas
        self.canvas.create_image(self.offset_x + self.canvas.winfo_width() // 2, self.offset_y + self.canvas.winfo_height() // 2, anchor=tk.CENTER, image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def toggle_image(self, direction):
        """Toggle between images in the loaded folder."""
        self.current_image_index += direction
        if self.current_image_index < 0:
            self.current_image_index = len(self.images) - 1  # Wrap to last image
        elif self.current_image_index >= len(self.images):
            self.current_image_index = 0  # Wrap to first image
        self.load_image()

    def reset_zoom(self, event=None):
        """Reset the zoom level to the original size."""
        self.zoom_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.display_image()

    def zoom(self, event):
        """Zoom in and out with the mouse wheel."""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        """Zoom in on the image."""
        self.zoom_scale *= 1.1  # Increase zoom scale
        self.display_image()

    def zoom_out(self):
        """Zoom out from the image."""
        self.zoom_scale /= 1.1  # Decrease zoom scale
        self.display_image()

    def start_pan(self):
        """Start panning the image."""
        self.canvas.bind("<ButtonPress-1>", self.on_pan_start)
        self.canvas.bind("<B1-Motion>", self.on_pan_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_pan_end)

    def on_pan_start(self, event):
        """Store the initial position for panning."""
        self.last_x = event.x
        self.last_y = event.y

    def on_pan_motion(self, event):
        """Update the offsets based on mouse movement."""
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.offset_x += dx
        self.offset_y += dy
        self.last_x = event.x
        self.last_y = event.y
        self.display_image()

    def on_pan_end(self, event):
        """End panning."""
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def perform_ocr(self):
        """Perform OCR on the currently loaded image with preprocessing."""
        if self.img_original:
            # Convert PIL image to OpenCV format
            img_cv = cv2.cvtColor(np.array(self.img_original), cv2.COLOR_RGB2BGR)

            # Preprocessing for OCR accuracy
            img_processed = self.preprocess_image(img_cv)

            # Perform OCR using pytesseract with custom configuration
            custom_config = r'--oem 3 --psm 6'
            ocr_text = pytesseract.image_to_string(img_processed, config=custom_config)

            # Show the OCR result
            self.show_ocr_result(ocr_text)
        else:
            messagebox.showwarning("No Image", "Please load an image first.")

    def preprocess_image(self, img):
        """Apply advanced preprocessing to enhance image for OCR."""
        # Convert to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Resize image to make it larger for better OCR recognition
        img_resized = cv2.resize(img_gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # Apply Gaussian blur to reduce noise
        img_blur = cv2.GaussianBlur(img_resized, (5, 5), 0)

        # Thresholding (Binarization) to get a pure black-and-white image
        _, img_thresh = cv2.threshold(img_blur, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        return img_thresh

    def show_ocr_result(self, ocr_text):
        """Show the OCR result in a new window."""
        ocr_window = tk.Toplevel(self.root)
        ocr_window.title("OCR Result")
        ocr_window.geometry("600x400")

        # ScrolledText widget for displaying OCR text
        self.text_area = scrolledtext.ScrolledText(ocr_window, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.text_area.insert(tk.END, ocr_text)

        # Copy and Save buttons
        copy_button = tk.Button(ocr_window, text="Copy Selected", command=self.copy_selection)
        copy_button.pack(side=tk.LEFT, padx=5, pady=5)

        save_button = tk.Button(ocr_window, text="Save as (TXT/DOC)", command=self.save_ocr_result)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

    def copy_selection(self):
        """Copy selected text from the text area."""
        try:
            self.text_area.event_generate("<<Copy>>")
        except Exception as e:
            messagebox.showwarning("Copy Error", "Error while copying: " + str(e))

    def save_ocr_result(self):
        """Save the OCR result as a text file or Word document."""
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Word Document", "*.docx")])
        if save_path:
            if save_path.endswith('.txt'):
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get("1.0", tk.END))
            elif save_path.endswith('.docx'):
                doc = Document()
                doc.add_paragraph(self.text_area.get("1.0", tk.END))
                doc.save(save_path)
            messagebox.showinfo("Success", "OCR result saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerWithOCR(root)
    root.mainloop()
