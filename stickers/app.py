"""
This module contains the main application class for Pysticker.

It manages the main window, existing notes, and the "New Sticker" button.

Copyright: (c) 2018 Augusto Cesar Perin. All rights reserved.
"""
import tkinter as tk
from tkinter import messagebox
import json
import os
import random
from .note import StickerNote

class App:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-topmost", True)
        
        self.root.withdraw()
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry("+{}+{}".format(x, y))
        self.root.deiconify()

        self.notes = {}
        self.save_file = "stickers_data.json"
        
        tk.Label(self.root, text="Pysticker", font=("Arial", 16, "bold")).pack(pady=(10, 10))
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Novo Sticker", command=self.create_note,
                 bg="#663399", fg="white", font=("Arial", 12), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="💀 Kill 'Em All", command=self.clear_all,
                 bg="#F44336", fg="white", font=("Arial", 12), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="?", command=self.show_about_window,
                 bg="gray", fg="white", font=("Arial", 12, "bold"), width=3).pack(side=tk.LEFT, padx=5)
        
        self.load_notes()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_note(self, x=None, y=None, width=250, height=200, color=None, text="", note_id=None):
        if x is None:
            x = random.randint(100, 800)
        if y is None:
            y = random.randint(100, 500)
        if color is None:
            colors = ["#FFEB3B", "#FF9800", "#4CAF50", "#2196F3", "#E91E63", "#9C27B0", "#00BCD4"]
            color = random.choice(colors)
        
        note = StickerNote(self.root, x, y, width, height, color, text, note_id)
        note.master_app = self
        self.notes[note.note_id] = note
        self.save_notes()
        return note
    
    def remove_note(self, note_id):
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_notes()
    
    def clear_all(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir todos os stickers?"):
            for note_id in list(self.notes.keys()):
                self.notes[note_id].window.destroy()
                del self.notes[note_id]
            self.save_notes()
    
    def save_notes(self):
        data = []
        for note in self.notes.values():
            try:
                data.append(note.get_data())
            except:
                pass
        
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_notes(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                for note_data in data:
                    note = self.create_note(
                        x=note_data.get("x", 100),
                        y=note_data.get("y", 100),
                        width=note_data.get("width", 250),
                        height=note_data.get("height", 200),
                        color=note_data.get("color", "#FFEB3B"),
                        text=note_data.get("text", ""),
                        note_id=note_data.get("id")
                    )
                    
                    if note_data.get("minimized"):
                        note.minimize()
                        
            except (json.JSONDecodeError, UnicodeDecodeError):
                messagebox.showerror("Erro de Carregamento", 
                                     "Não foi possível ler o arquivo '{}'. ".format(self.save_file)+
                                     "Um novo arquivo será criado.")
            except Exception as e:
                messagebox.showerror("Erro Inesperado", "Ocorreu um erro ao carregar as notas: {}".format(e))

    def show_about_window(self):
        about_win = tk.Toplevel(self.root)
        about_win.title("Sobre")
        about_win.geometry("300x150")
        about_win.resizable(False, False)
        about_win.transient(self.root)
        about_win.grab_set()
        
        tk.Label(about_win, text="Pysticker", font=("Arial", 14, "bold")).pack(pady=(10,5))
        tk.Label(about_win, text="Versão 1.0", font=("Arial", 9)).pack()
        tk.Label(about_win, text="\nCriado por Augusto Cesar Perin, 2018", font=("Arial", 10)).pack(pady=5)
        
        tk.Button(about_win, text="OK", command=about_win.destroy, width=10).pack(pady=10)
        
        self.root.wait_window(about_win)

    def on_closing(self):
        self.save_notes()
        self.root.destroy() 