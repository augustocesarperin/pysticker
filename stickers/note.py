"""
Represents a single sticky note window in the Pysticker application.

Handles the appearance, behavior, and data of an individual note.

Copyright: (c) 2018 Augusto Cesar Perin. All rights reserved.
"""
import tkinter as tk
from tkinter import colorchooser
from datetime import datetime

class StickerNote:
    def __init__(self, master, x=100, y=100, width=250, height=200, color="#FFEB3B", text="", note_id=None):
        self.master = master
        self.master_app = None
        self.note_id = note_id or datetime.now().strftime("%Y%m%d%H%M%S%f")
        
        self.window = tk.Toplevel(master)
        self.window.title("")
        self.window.geometry("{}x{}+{}+{}".format(width, height, x, y))
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        self.main_frame = tk.Frame(self.window, bg=color, highlightbackground="gray", highlightthickness=1)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.top_bar = tk.Frame(self.main_frame, bg=self.darken_color(color), height=25)
        self.top_bar.pack(fill=tk.X)
        self.top_bar.pack_propagate(False)
        
        self.close_btn = tk.Button(self.top_bar, text="✕", command=self.close_note,
                                  bg=self.darken_color(color), fg="white", bd=0,
                                  font=("Arial", 12, "bold"))
        self.close_btn.pack(side=tk.RIGHT, padx=5)
        
        self.color_btn = tk.Button(self.top_bar, text="🎨", command=self.change_color,
                                  bg=self.darken_color(color), fg="white", bd=0,
                                  font=("Arial", 12))
        self.color_btn.pack(side=tk.RIGHT, padx=2)
        
        self.minimize_btn = tk.Button(self.top_bar, text="—", command=self.minimize,
                                     bg=self.darken_color(color), fg="white", bd=0,
                                     font=("Arial", 12, "bold"))
        self.minimize_btn.pack(side=tk.RIGHT, padx=2)
        
        self.text_area = tk.Text(self.main_frame, bg=color, fg="black", 
                                font=("Arial", 11), bd=0, wrap=tk.WORD,
                                insertbackground="black")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_area.insert("1.0", text)
        
        self.top_bar.bind("<Button-1>", self.start_drag)
        self.top_bar.bind("<ButtonRelease-1>", self.stop_drag)
        self.top_bar.bind("<B1-Motion>", self.drag)
        
        self.resize_grip = tk.Label(self.main_frame, text="◢", bg=color, 
                                   font=("Arial", 8), cursor="bottom_right_corner")
        self.resize_grip.place(relx=1.0, rely=1.0, anchor="se")
        self.resize_grip.bind("<Button-1>", self.start_resize)
        self.resize_grip.bind("<B1-Motion>", self.resize)
        
        self.text_area.bind("<KeyRelease>", lambda e: self.master_app.save_notes())
        
        self.drag_data = {"x": 0, "y": 0}
        self.current_color = color
        self.is_minimized = False
        self.saved_height = height
        
    def darken_color(self, color):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        r = max(0, r - 40)
        g = max(0, g - 40)
        b = max(0, b - 40)
        
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    
    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def stop_drag(self, event):
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.master_app.save_notes()
    
    def drag(self, event):
        x = self.window.winfo_x() + event.x - self.drag_data["x"]
        y = self.window.winfo_y() + event.y - self.drag_data["y"]
        self.window.geometry("+{}+{}".format(x, y))
    
    def start_resize(self, event):
        self.resize_data = {"x": event.x_root, "y": event.y_root,
                           "width": self.window.winfo_width(),
                           "height": self.window.winfo_height()}
    
    def resize(self, event):
        delta_x = event.x_root - self.resize_data["x"]
        delta_y = event.y_root - self.resize_data["y"]
        
        new_width = max(150, self.resize_data["width"] + delta_x)
        new_height = max(100, self.resize_data["height"] + delta_y)
        
        self.window.geometry("{}x{}".format(new_width, new_height))
        self.saved_height = new_height
        self.master_app.save_notes()
    
    def minimize(self):
        if not self.is_minimized:
            self.saved_height = self.window.winfo_height()
            self.window.geometry("{}x{}".format(self.window.winfo_width(), 30))
            self.text_area.pack_forget()
            self.resize_grip.place_forget()
            self.is_minimized = True
        else:
            self.window.geometry("{}x{}".format(self.window.winfo_width(), self.saved_height))
            self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.resize_grip.place(relx=1.0, rely=1.0, anchor="se")
            self.is_minimized = False
        self.master_app.save_notes()
    
    def change_color(self):
        color = colorchooser.askcolor(color=self.current_color)[1]
        if color:
            self.current_color = color
            self.main_frame.config(bg=color)
            self.text_area.config(bg=color)
            self.resize_grip.config(bg=color)
            
            dark_color = self.darken_color(color)
            self.top_bar.config(bg=dark_color)
            self.close_btn.config(bg=dark_color)
            self.color_btn.config(bg=dark_color)
            self.minimize_btn.config(bg=dark_color)
            
            self.master_app.save_notes()
    
    def close_note(self):
        self.window.destroy()
        self.master_app.remove_note(self.note_id)
    
    def get_data(self):
        return {
            "id": self.note_id,
            "x": self.window.winfo_x(),
            "y": self.window.winfo_y(),
            "width": self.window.winfo_width(),
            "height": self.window.winfo_height(),
            "color": self.current_color,
            "text": self.text_area.get("1.0", tk.END).strip(),
            "minimized": self.is_minimized
        } 