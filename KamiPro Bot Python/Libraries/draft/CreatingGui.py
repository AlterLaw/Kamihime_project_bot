import tkinter as tk

class MyGUI:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()

        # Set the window title
        self.window.title("KamiPro Bot")

        # Set the window size to 400x500
        self.largura = 1200
        self.altura = 400
        self.window.geometry(f"{self.largura}x{self.altura}")
        self.window.minsize(950, 480)  # Set your desired minimum width and height

        # Add elements
        self.create_dynamic_label()
        self.add_buttons()
        self.add_image("Assets\MainScreen.png")


        # Start the Tkinter event loop
        self.window.mainloop()

    def add_buttons(self):
        # Create buttons and pack them vertically on the left side
        for i in range(5):  # Change this number as per your requirement
            button_text = f"Button {i + 1}"
            button = tk.Button(self.window, text=button_text, width=30, height=5)
            button.pack(side=tk.TOP, anchor=tk.NW, pady=1)  # Adjust padx and pady as needed

    def update_label_text(self, event):
        current_width, current_height = self.get_window_size()
        self.label_var.set(f"Window Size: {current_width} x {current_height}")
    
    def add_image(self, image_path):
        # Create a Canvas widget and add an image to it
        canvas = tk.Canvas(self.window, width=300, height=self.altura)
        canvas.pack(side=tk.RIGHT, fill=tk.Y)

        # Load the image
        image = tk.PhotoImage(file=image_path)

        # Add the image to the Canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=image)

        # Keep a reference to the image to prevent it from being garbage collected
        canvas.image = image

    def create_dynamic_label(self):
        width = self.window.winfo_width()
        height = self.window.winfo_height()

        self.label_var = tk.StringVar()
        label = tk.Label(self.window, textvariable=self.label_var)
        label.pack(pady=10)

        # Bind the update_label_text function to the Configure event
        self.window.bind("<Configure>", self.update_label_text)

    def get_window_size(self):
        return self.window.winfo_width(), self.window.winfo_height()

# Instantiate the class to create the GUI
my_gui = MyGUI()
