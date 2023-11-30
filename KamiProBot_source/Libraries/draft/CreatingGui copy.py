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
        self.add_buttons_and_image("Assets\MainScreen.png")

        # Start the Tkinter event loop
        self.window.mainloop()

    def add_buttons_and_image(self, image_path):
        
        #<Button section>
        #Creating button frame
        
        self.frame_buttons = tk.Frame(self.window)
        self.frame_buttons.pack(side=tk.LEFT)

        # Create buttons and pack them vertically inside the frame
        for i in range(5):  # Change this number as per your requirement
            button_text = f"Button {i + 1}"
            button = tk.Button(self.frame_buttons, text=button_text, width=30, height=5)
            button.pack(side=tk.TOP, anchor=tk.NW, pady=1)


        #<Image section>
        #Creating image frame
        self.frame_img = tk.Frame(self.window)
        self.frame_img.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a Canvas widget and add it to the Frame
        canvas = tk.Canvas(self.frame_img, height=self.altura)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Now you can add your image to the canvas
        img = tk.PhotoImage(file=image_path)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)

        # Load the image and get its original dimensions
        original_image = tk.PhotoImage(file=image_path)
        original_width = original_image.width()
        original_height = original_image.height()

        # Calculate the new width to fit the frame height
        new_width = int((self.altura / original_height) * original_width)

        # Resize the image
        resized_image = original_image.subsample(int(original_width / new_width))

        # Add the resized image to the Canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=resized_image)

        # Keep a reference to the image to prevent it from being garbage collected
        canvas.image = resized_image
        

    def update_label_text(self, event):
        current_width, current_height = self.get_window_size()
        self.label_var.set(f"Window Size: {current_width} x {current_height}")

    def update_img_size(self, event):
        current_width, current_height = self.get_window_size()
        self.frame_img.config(width=current_width)

    def create_dynamic_label(self):
        width = self.window.winfo_width()
        height = self.window.winfo_height()

        self.label_var = tk.StringVar()
        label = tk.Label(self.window, textvariable=self.label_var)
        label.pack(pady=10)

        # Bind the update_label_text function to the Configure event
        self.window.bind("<Configure>", self.update_label_text)
        self.window.bind("<Configure>", self.update_img_size)

    def get_window_size(self):
        return self.window.winfo_width(), self.window.winfo_height()

# Instantiate the class to create the GUI
my_gui = MyGUI()
