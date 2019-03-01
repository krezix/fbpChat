import tkinter as tk

class fbGui(tk.Frame):
    def __init__(self,parent):
        self.parent = parent


if __name__ == "__main__":
    root = tk.Tk()
    fb = fbGui(root)
    

