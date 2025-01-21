import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

# Function to select an image file
def select_file():
    path = filedialog.askopenfilename(filetypes=[
        ("PNG Image", "*.png"),
        ("GIF Image", "*.gif"),
        ("WebP Image", "*.webp"),
        ("All Files", "*.*")
    ])
    if path:
        open_image(path)

# Function to open and process the selected image
def open_image(path):
    global image, image_tk, canvas, selection_frame, preview_canvas, preview_image

    # Load the image
    image = Image.open(path)

    # Quantize the image to reduce colors to 32
    image = image.quantize(colors=32)

    # Create a Tkinter-compatible image
    image_tk = ImageTk.PhotoImage(image)

    # Update canvas size to fit the image
    canvas.config(width=image.width, height=image.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    # Initialize the selection frame
    selection_frame.place(x=0, y=0, width=64, height=64)
    update_preview()

# Start drag event for the selection frame
def start_drag(event):
    selection_frame.start_x = event.x
    selection_frame.start_y = event.y

# Move the selection frame during dragging
def move_frame(event):
    dx = event.x - selection_frame.start_x
    dy = event.y - selection_frame.start_y

    new_x = selection_frame.winfo_x() + dx
    new_y = selection_frame.winfo_y() + dy

    # Ensure the frame stays within image boundaries
    max_x = image.width - selection_frame.winfo_width()
    max_y = image.height - selection_frame.winfo_height()

    new_x = max(0, min(new_x, max_x))
    new_y = max(0, min(new_y, max_y))

    selection_frame.place(x=new_x, y=new_y)
    selection_frame.start_x = event.x
    selection_frame.start_y = event.y

    update_preview()

# Resize the selection frame
def resize_image():
    try:
        new_size = int(size_input.get())
        if new_size < 32:
            new_size = 32  # Minimum size
    except ValueError:
        print("Please enter a valid size.")
        return

    # Limit size to ensure it doesn't exceed the image dimensions
    new_size = min(new_size, image.width, image.height)

    # Update canvas with the resized image
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    selection_frame.place(x=0, y=0, width=new_size, height=new_size)
    update_preview()

# Update the preview panel
def update_preview():
    global preview_image

    x, y = selection_frame.winfo_x(), selection_frame.winfo_y()
    size = selection_frame.winfo_width()

    if size > 0:
        # Crop the image based on the selection frame
        crop = image.crop((x, y, x + size, y + size))
        crop = crop.resize((32, 32), Image.Resampling.LANCZOS)

        preview_image = ImageTk.PhotoImage(crop)
        preview_canvas.create_image(0, 0, anchor=tk.NW, image=preview_image)

# Save the cropped image
def save_image():
    x, y = selection_frame.winfo_x(), selection_frame.winfo_y()
    size = selection_frame.winfo_width()

    # Crop and resize the selected region
    crop = image.crop((x, y, x + size, y + size))
    crop = crop.resize((32, 32), Image.Resampling.LANCZOS)

    # Save the image to a file
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        crop.save(save_path)
        print(f"Image saved to {save_path}")

# Main window setup
window = tk.Tk()
window.title("Selection and 32x32 Resizing Tool")

# Main canvas for image display
canvas = tk.Canvas(window, bg="white")
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Side panel for controls
side_panel = tk.Frame(window)
side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Preview canvas
preview_canvas = tk.Canvas(side_panel, width=32, height=32, bg="white")
preview_canvas.pack(pady=10)

# Input for size
size_label = tk.Label(side_panel, text="Image Size:")
size_label.pack()

size_input = tk.Entry(side_panel)
size_input.insert(0, "64")
size_input.pack()

resize_button = tk.Button(side_panel, text="Resize Image", command=resize_image)
resize_button.pack(pady=5)

# Control buttons
select_button = tk.Button(side_panel, text="Select File", command=select_file)
select_button.pack(pady=5)

save_button = tk.Button(side_panel, text="Save Image", command=save_image)
save_button.pack(pady=5)

# Selection frame
selection_frame = tk.Frame(canvas, bg="white", width=64, height=64, highlightbackground="black", highlightthickness=1)
selection_frame.place(x=0, y=0)
selection_frame.bind("<Button-1>", start_drag)
selection_frame.bind("<B1-Motion>", move_frame)

window.mainloop()
