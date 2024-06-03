import tkinter as tk

class SnellenChartApp:
    def __init__(self, master, optotypes, visual_acuities, test_distance=20, screen_size_cm=(34, 19), screen_resolution=(1920, 1080), scaling_factor=(1.25)):
        self.master = master
        self.master.title("Snellen Chart")
        self.canvas = tk.Canvas(master, width=screen_resolution[0], height=screen_resolution[1])
        self.canvas.pack()
        self.optotypes = optotypes
        self.visual_acuities = visual_acuities
        self.test_distance = test_distance
        self.screen_size_cm = screen_size_cm
        self.screen_resolution = screen_resolution
        self.scaling_factor = scaling_factor
        self.row_index = 0
        self.letter_index = 0
        self.update_letter()

    def calculate_size_based_on_formula(self, denominator):
        size = (denominator * 0.3048) * 0.00145
        return size

    def calculate_pixel_size(self, size_meters):
        # Calculate pixels per meter based on screen resolution and physical size
        ppm_width = self.screen_resolution[0] / (self.screen_size_cm[0] / 100)
        ppm_height = self.screen_resolution[1] / (self.screen_size_cm[1] / 100)

        # Calculate pixel size with scaling factor
        pixel_width_size = size_meters * ppm_width / self.scaling_factor
        pixel_height_size = size_meters * ppm_height / self.scaling_factor

        return int(pixel_width_size), int(pixel_height_size)

    def print_letter_size(self, optotype, size):
        print(f"Size of '{optotype}': {size:.4f} meters")

    def update_letter(self):
        optotype = self.optotypes[self.row_index][self.letter_index]
        visual_acuity = self.visual_acuities[self.row_index]

        # Calculate optotype size based on the specified formula
        denominator = int(visual_acuity.split('/')[1])
        size_formula = self.calculate_size_based_on_formula(denominator)
        self.print_letter_size(optotype, size_formula)

        # Calculate pixel size based on the laptop's resolution with scaling factor
        pixel_size = self.calculate_pixel_size(size_formula)

        self.canvas.delete("all")
        # Draw the optotype with specified dimensions
        font_size = pixel_size[0]  # Use width for font size
        self.canvas.create_text(self.screen_resolution[0] / 2, self.screen_resolution[1] / 2, text=optotype, font=("Helvetica", font_size), anchor="center")

        # Display size calculation in the top-right corner
        self.canvas.create_text(750, 50, text=f"Size: {size_formula:.4f} meters", anchor="e")

        # Move to the next letter or row after 3 seconds
        self.letter_index += 1
        if self.letter_index >= len(self.optotypes[self.row_index]):
            self.letter_index = 0
            self.row_index += 1

        if self.row_index < len(self.optotypes):
            self.master.after(8000, self.update_letter)

def main():
    # Define the structure of the custom Snellen-like chart
    optotypes = [
        ['E'],
        ['F', 'P'],
        ['T', 'O', 'Z'],
        ['L', 'P', 'E', 'D'],
        ['P', 'E', 'C', 'F', 'D'],
        ['E', 'D', 'F', 'C', 'Z', 'P'],
        ['F', 'E', 'L', 'O', 'P', 'Z', 'D'],
        ['D', 'E', 'F', 'P', 'O', 'T', 'E', 'C'],
        ['L', 'E', 'F', 'O', 'D', 'P', 'C', 'T'],
        ['F', 'D', 'P', 'L', 'T', 'C', 'E', 'O'],
        ['P', 'E', 'Z', 'O', 'L', 'C', 'R', 'T', 'D']
    ]

    # Define corresponding visual acuity levels
    visual_acuities = ['20/200', '20/100', '20/70', '20/50', '20/40', '20/30', '20/25', '20/20', '20/15', '20/13', '20/10']

    # Set the scaling factor (adjust as needed)
    scaling_factor = 1.2273

    # Create the Tkinter application
    root = tk.Tk()
    app = SnellenChartApp(root, optotypes, visual_acuities, scaling_factor=scaling_factor)

    root.mainloop()

if __name__ == "__main__":
    main()
