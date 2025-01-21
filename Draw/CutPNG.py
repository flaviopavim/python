import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

# Function to select an image file
def select_file():
    path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if path:
        open_image(path)

# Function to open the image and configure the canvas
def open_image(path):
    global image, image_tk, canvas, frame, preview_canvas, preview_image

    image = Image.open(path)
    image_tk = ImageTk.PhotoImage(image)

    canvas.config(width=image.width, height=image.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    frame.place(x=0, y=0, width=64, height=64)
    update_preview()

# Function to start dragging the selection frame
def start_drag(event):
    frame.start_x = event.x
    frame.start_y = event.y

# Function to move the selection frame during dragging
def move_frame(event):
    dx = event.x - frame.start_x
    dy = event.y - frame.start_y

    new_x = frame.winfo_x() + dx
    new_y = frame.winfo_y() + dy

    # Restrict movement within the image boundaries
    max_x = image.width - frame.winfo_width()
    max_y = image.height - frame.winfo_height()

    new_x = max(0, min(new_x, max_x))
    new_y = max(0, min(new_y, max_y))

    frame.place(x=new_x, y=new_y)
    frame.start_x = event.x
    frame.start_y = event.y

    update_preview()

# Function to resize the selection frame
def resize_frame():
    try:
        new_size = int(size_input.get())
        if new_size < 32:
            new_size = 32  # Minimum size
    except ValueError:
        print("Enter a valid size.")
        return

    # Limit size to fit within the image dimensions
    new_size = min(new_size, image.width, image.height)

    frame.place(x=0, y=0, width=new_size, height=new_size)
    update_preview()

# Function to update the preview canvas
def update_preview():
    global preview_image

    x, y = frame.winfo_x(), frame.winfo_y()
    size = frame.winfo_width()

    if size > 0:
        cropped = image.crop((x, y, x + size, y + size))
        cropped = cropped.resize((32, 32), Image.Resampling.LANCZOS)
        preview_image = ImageTk.PhotoImage(cropped)
        preview_canvas.create_image(0, 0, anchor=tk.NW, image=preview_image)

# Function to save the cropped and resized image
def save_image():
    x, y = frame.winfo_x(), frame.winfo_y()
    size = frame.winfo_width()

    cropped = image.crop((x, y, x + size, y + size))
    cropped = cropped.resize((32, 32), Image.Resampling.LANCZOS)

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if output_path:
        cropped.save(output_path)
        print(f"Image saved at {output_path}")

# Main window configuration
window = tk.Tk()
window.title("32x32 Selection and Resizing")

# Main canvas
canvas = tk.Canvas(window, bg="white")
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Sidebar frame
sidebar_frame = tk.Frame(window)
sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Preview canvas
preview_canvas = tk.Canvas(sidebar_frame, width=32, height=32, bg="white")
preview_canvas.pack(pady=10)

# Input for size
size_label = tk.Label(sidebar_frame, text="Frame size:")
size_label.pack()

size_input = tk.Entry(sidebar_frame)
size_input.insert(0, "64")
size_input.pack()

btn_resize = tk.Button(sidebar_frame, text="Resize Frame", command=resize_frame)
btn_resize.pack(pady=5)

# Control buttons
btn_select = tk.Button(sidebar_frame, text="Select File", command=select_file)
btn_select.pack(pady=5)

btn_save = tk.Button(sidebar_frame, text="Save Image", command=save_image)
btn_save.pack(pady=5)

# Selection frame
frame = tk.Frame(canvas, bg="white", width=64, height=64, highlightbackground="black", highlightthickness=1)
frame.place(x=0, y=0)
frame.bind("<Button-1>", start_drag)
frame.bind("<B1-Motion>", move_frame)

window.mainloop()
