import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from enum import Enum, auto

class EOrientation(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class EChartApp:
    def __init__(self, master):
        self.master = master
        self.current_orientation = EOrientation.UP

        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()

        self.canvas = tk.Canvas(master, width=self.screen_width, height=self.screen_height, bg="white")
        self.canvas.pack()

        self.label = tk.Label(master, text="Press Enter to change orientation", font=("Helvetica", 20), fg="black", bg="white")
        self.label.place(relx=0.5, rely=0.9, anchor="center")

        self.e_images = {
            EOrientation.UP: self.create_e_image(0),
            EOrientation.DOWN: self.create_e_image(180),
            EOrientation.LEFT: self.create_e_image(90),
            EOrientation.RIGHT: self.create_e_image(270),
        }

        self.current_e_image = self.e_images[self.current_orientation]
        self.image_on_canvas = self.canvas.create_image(self.screen_width // 2, self.screen_height // 2, image=self.current_e_image)

        master.bind("<Return>", self.change_orientation)

    def create_e_image(self, angle):
        e_image = Image.new("RGB", (200, 200), "white")  # White background
        draw = ImageDraw.Draw(e_image)

        font_size = 40
        font = ImageFont.truetype("arial.ttf", font_size)

        draw.text((100, 100), "E", font=font, fill="black", anchor="mm")  # Black text

        rotated_image = e_image.rotate(angle)
        rotated_photo = self.image_to_photo(rotated_image)

        return rotated_photo

    def draw_e(self, orientation):
        self.canvas.itemconfig(self.image_on_canvas, image=self.e_images[orientation])

    def change_orientation(self, event):
    # Change to the next orientation
        self.current_orientation = EOrientation((self.current_orientation.value) % 4 + 1)

    # Update the rotated 'E' image on the canvas
        self.draw_e(self.current_orientation)


    def image_to_photo(self, image):
        return ImageTk.PhotoImage(image=image)

if __name__ == "__main__":
    # Create a full-screen window
    root = tk.Tk()
    root.attributes('-fullscreen', True)

    # Create the EChartApp instance
    e_chart_app = EChartApp(root)

    # Start the Tkinter event loop
    root.mainloop()
