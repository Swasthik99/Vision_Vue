import tkinter as tk
#The code starts by importing the tkinter library for creating the graphical user interface  
import random
#the random module for shuffling the letters in the Snellen chart.

class SnellenChartApp:
    def __init__(self, master, alphabet):
        #It takes master (the Tkinter root window) 
        #alphabet (a string containing the letters for the Snellen chart) as parameters.
        self.master = master
        self.alphabet = alphabet
        self.current_letter_index = 0
        self.base_font_size = 80  # Base font size for 20/20 vision

        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        #winfo_screenwidth() and winfo_screenheight() methods are used to retrieve the width and height of the screen, respectively, on which the Tkinter window is displayed.

        self.canvas = tk.Canvas(master, width=self.screen_width, height=self.screen_height, bg="white")
        #The canvas is used as a background, and the label displays the current letter.
        self.canvas.pack()
        #The pack() method adjusts the size of the canvas based on its content and places it within the available space in the master window.

        self.label = tk.Label(master, text=self.alphabet[self.current_letter_index], font=("Helvetica", self.base_font_size), fg="black", bg="white")
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        #The place() method is called on the label to specify its placement within the master window.
        #relx=0.5: Sets the relative x-coordinate of the anchor point to the center of the master window.
        #rely=0.5: Sets the relative y-coordinate of the anchor point to the center of the master window.


        master.bind("<Return>", self.next_letter)
        #binds the Enter key to the next_letter method, so pressing Enter will trigger the display of the next letter.

    def next_letter(self, event):
        self.current_letter_index += 1
        if self.current_letter_index < len(self.alphabet):
            # Decrease font size by a factor of 1.2 for each letter
            self.base_font_size = int(self.base_font_size / 1.2)
            self.label.config(text=self.alphabet[self.current_letter_index], font=("Helvetica", self.base_font_size))
            #Updates the text displayed on the label to the next letter in the Snellen chart. 
        else:
            # Display a message when all letters are shown
            self.label.config(text="Test complete", font=("Helvetica", 30))

if __name__ == "__main__":
    # Define the specified nine letters for the Snellen chart
    snellen_alphabet = "CDEFLLOPTZ"
    
    # Create a full-screen window
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    #sets the window to be displayed in full-screen mode.

    # Create the SnellenChartApp instance
    app = SnellenChartApp(root, snellen_alphabet)
    #This line creates an instance of the SnellenChartApp class, passing the Tkinter root window (root) and the string of Snellen chart letters (snellen_alphabet) as parameters.

    # Start the Tkinter event loop
    root.mainloop()
