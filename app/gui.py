import tkinter as tk

def create_gui():
    window = tk.Tk()
    window.title("To-Do List App")

    label = tk.Label(window, text="Welcome to To-Do List App")
    label.pack()

    window.mainloop()
