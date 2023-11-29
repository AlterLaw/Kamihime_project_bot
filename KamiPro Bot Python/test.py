import tkinter as tk

root = tk.Tk()
root.title("Tkinter Divs")

# Creating frames (divs) with visible borders
frame1 = tk.Frame(root, borderwidth=2, relief="solid", highlightbackground="black", highlightcolor="black")
frame2 = tk.Frame(root, borderwidth=2, relief="solid", highlightbackground="black", highlightcolor="black")

# Adding widgets to frames
label1 = tk.Label(frame1, text="Frame 1 Content")
label2 = tk.Label(frame2, text="Frame 2 Content")

# Packing frames and labels
frame1.pack(side="left", padx=10, pady=10)
frame2.pack(side="left", padx=10, pady=10)

label1.pack()
label2.pack()

root.mainloop()
