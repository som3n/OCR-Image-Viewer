# OCR-Image-Viewer

## Overview

**ImageViewerWithOCR** is a Python-based GUI application that allows users to view images and perform Optical Character Recognition (OCR) on them using Tesseract. It supports various image formats and provides tools for zooming, panning, and applying advanced image preprocessing for accurate OCR results. The OCR output can be copied, saved as a text file, or exported as a Word document.

## Features

- **Load Images**: Open individual image files or load entire folders of images for viewing.
- **OCR Processing**: Extract text from images using Tesseract OCR with preprocessing for improved accuracy.
- **Zoom and Pan**: Easily zoom in/out and pan across images for better viewing.
- **Preprocessing**: Automatically applies grayscale conversion, resizing, Gaussian blur, and thresholding for enhanced OCR.
- **Keyboard Shortcuts**: Fast access to features using keyboard shortcuts.
- **OCR Result Output**: View, copy, and save OCR results in text or Word document formats.

## Requirements

- **Python 3.x**
- **Tesseract-OCR** installed and configured
- Required Python libraries:
  - `pytesseract`
  - `Pillow`
  - `tkinter`
  - `opencv-python`
  - `numpy`
  - `python-docx`

### Installing Required Libraries

You can install the necessary libraries using pip:

```bash
pip install pytesseract Pillow opencv-python numpy python-docx
```

### Installing Tesseract

1. Download and install Tesseract from its official repository:
   - Windows: [Tesseract Installation](https://github.com/tesseract-ocr/tesseract/wiki)
   - Linux (Debian-based): `sudo apt install tesseract-ocr`
2. Ensure the Tesseract executable is accessible from your system's PATH.

## Usage

1. **Run the Application:**

   To start the application, run the following command:

   ```bash
   python theImages.py
   ```

2. **Open Images:**

   - Use **File > Open Folder** or press `Ctrl + O` to load a folder of images.
   - Use **File > Open Image** to load a single image file.

3. **Zoom and Pan:**

   - Zoom in with the **Up Arrow** or scroll up with the mouse wheel.
   - Zoom out with the **Down Arrow** or scroll down with the mouse wheel.
   - Use **Left** and **Right** arrow keys to switch between images.
   - Use the **Pan** option from the menu or drag the image using the mouse.

4. **Perform OCR:**

   - Use **File > Perform OCR** or press `Ctrl + W` to extract text from the current image.
   - The extracted text will be displayed in a new window.

5. **Copy and Save OCR Result:**

   - In the OCR result window, you can **Copy Selected** text or save the result as a `.txt` or `.docx` file using the **Save as** button.

## Keyboard Shortcuts

- `Ctrl + O`: Open folder or image file
- `Ctrl + W`: Perform OCR on the current image
- **Up Arrow**: Zoom in
- **Down Arrow**: Zoom out
- **Left Arrow**: Previous image
- **Right Arrow**: Next image
- **Mouse Scroll**: Zoom in/out

## License

This project is licensed under the MIT License.

## Author

This application was developed by Somen Samanta.

## Contact

For any queries, feel free to contact: [Your Email]

---

Enjoy using ImageViewerWithOCR for all your image viewing and text extraction needs!
