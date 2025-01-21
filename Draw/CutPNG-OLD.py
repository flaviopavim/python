import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to select a file
def select_file():
    path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if path:
        open_image(path)

# Function to open the image and prepare the canvas
def open_image(path):
    global image, image_tk, canvas, frame

    image = Image.open(path)
    image_tk = ImageTk.PhotoImage(image)

    canvas.config(width=image.width, height=image.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    frame.place(x=0, y=0, width=32, height=32)

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

    # Restrict movement within image boundaries
    if 0 <= new_x <= (image.width - 32) and 0 <= new_y <= (image.height - 32):
        frame.place(x=new_x, y=new_y)
        frame.start_x = event.x
        frame.start_y = event.y

# Function to crop the selected area and save it
def crop_and_save():
    x, y = frame.winfo_x(), frame.winfo_y()
    cropped = image.crop((x, y, x + 32, y + 32))

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if output_path:
        cropped.save(output_path)
        print(f"Cropped image saved at {output_path}")

# Main window configuration
window = tk.Tk()
window.title("32x32 Crop Tool")

# Canvas to display the image
canvas = tk.Canvas(window, bg="white")
canvas.pack(expand=True, fill=tk.BOTH)

# Buttons
btn_select = tk.Button(window, text="Select File", command=select_file)
btn_select.pack(side=tk.TOP, pady=10)

btn_save = tk.Button(window, text="Crop and Save", command=crop_and_save)
btn_save.pack(side=tk.BOTTOM, pady=10)

# Selection frame
frame = tk.Frame(canvas, bg="white", width=32, height=32)
frame.place(x=0, y=0)
frame.attributes = {'alpha': 0.5}  # Set transparency
frame.bind("<Button-1>", start_drag)
frame.bind("<B1-Motion>", move_frame)

window.mainloop()
