"""
Pysticker: A desktop sticky notes application.

Copyright: (c) 2018 Augusto Cesar Perin. All rights reserved.
"""

import tkinter as tk
from stickers.app import App

def main():
    """Main function to run the application."""
    root = tk.Tk()
    root.title("Pysticker")

    try:
        icon = tk.PhotoImage(file='assets/icon.png')
        root.iconphoto(True, icon)
    except tk.TclError:
        print("Could not load 'assets/icon.png'.")

    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main() 