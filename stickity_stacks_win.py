#!/usr/bin/env python3
"""Stickity Stacks - Windows Implementation"""
import tkinter as tk
from tkinter import ttk, font as tkfont, colorchooser, scrolledtext
import json
import os
from pathlib import Path
from typing import List, Optional
import ctypes

# Enable DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

class StickyNoteWindow(tk.Toplevel):
    def __init__(self, parent, note_id, title, content="", 
                 font_family="Segoe UI", font_size=11,
                 fg_color="#1a1a1a", bg_color="#fffad1"):
        super().__init__(parent)
        self.parent = parent
        self.note_id = note_id
        self.note_title = title
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.font_family = font_family
        self.font_size = font_size
        
        # Set geometry BEFORE overrideredirect
        self.geometry("280x220")
        self.update_idletasks()  # Force geometry update
        
        self.overrideredirect(True)
        self.attributes('-topmost', False)
        self.configure(bg=bg_color)
        
        self._create_widgets(content)
        self._setup_bindings()
        
    def _create_widgets(self, content):
        control_frame = tk.Frame(self, bg=self.bg_color, height=30)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        control_frame.pack_propagate(False)
        
        # Use X instead of emoji for close button
        close_btn = tk.Button(control_frame, text="X", bg=self.bg_color, fg="red",
                              relief=tk.FLAT, bd=0, font=("Segoe UI", 10, "bold"),
                              width=2, cursor="hand2",
                              activebackground=self.bg_color, activeforeground="darkred")
        close_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        # Bind click events explicitly
        close_btn.bind("<Button-1>", lambda e: self._delete_note())
        
        # Use text for settings button
        settings_btn = tk.Button(control_frame, text="⋯", bg=self.bg_color, fg=self.fg_color,
                                relief=tk.FLAT, bd=0, font=("Segoe UI", 14, "bold"),
                                width=2, cursor="hand2",
                                activebackground=self.bg_color, activeforeground=self.fg_color)
        settings_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        # Bind click events explicitly
        settings_btn.bind("<Button-1>", lambda e: self._open_settings())
        
        # Title label
        title_label = tk.Label(control_frame, text=self.note_title, bg=self.bg_color, 
                              fg=self.fg_color, font=("Segoe UI", 9))
        title_label.pack(side=tk.LEFT, padx=5)
        
        self.drag_handle = tk.Label(control_frame, text="", bg=self.bg_color)
        self.drag_handle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.text_widget = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, bg=self.bg_color, fg=self.fg_color,
            font=(self.font_family, self.font_size), relief=tk.FLAT, bd=0,
            padx=8, pady=8, insertbackground=self.fg_color
        )
        self.text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        if content:
            self.text_widget.insert("1.0", content)
        
        # Resize grip with better visibility
        resize_grip = tk.Label(self, text="◢", bg=self.bg_color, fg=self.fg_color,
                              cursor="size_nw_se", font=("Segoe UI", 10))
        resize_grip.place(relx=1.0, rely=1.0, anchor=tk.SE)
        resize_grip.bind("<Button-1>", self._start_resize)
        resize_grip.bind("<B1-Motion>", self._do_resize)
        
    def _setup_bindings(self):
        self.drag_handle.bind("<Button-1>", self._start_drag)
        self.drag_handle.bind("<B1-Motion>", self._do_drag)
        self.text_widget.bind("<Control-s>", lambda e: self.parent.create_new_note())
        self.text_widget.bind("<Control-n>", lambda e: self.parent.create_new_note())
        self.text_widget.bind("<Control-d>", lambda e: self._delete_note())
        self.text_widget.bind("<Escape>", lambda e: self._delete_note())
        self.text_widget.bind("<KeyRelease>", lambda e: self.parent.save_notes())
        
    def _start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        
    def _do_drag(self, event):
        x = self.winfo_x() + event.x - self._drag_start_x
        y = self.winfo_y() + event.y - self._drag_start_y
        self.geometry(f"+{x}+{y}")
        
    def _start_resize(self, event):
        self._resize_start_x = event.x_root
        self._resize_start_y = event.y_root
        self._resize_start_width = self.winfo_width()
        self._resize_start_height = self.winfo_height()
        
    def _do_resize(self, event):
        delta_x = event.x_root - self._resize_start_x
        delta_y = event.y_root - self._resize_start_y
        new_width = max(200, self._resize_start_width + delta_x)
        new_height = max(150, self._resize_start_height + delta_y)
        self.geometry(f"{new_width}x{new_height}")
        
    def _open_settings(self):
        self.parent.open_settings_dialog(self)
        
    def _delete_note(self):
        self.parent.delete_note(self)
        
    def get_content(self):
        return self.text_widget.get("1.0", tk.END).strip()
        
    def update_styling(self, font_family, font_size, fg_color, bg_color):
        self.font_family = font_family
        self.font_size = font_size
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.configure(bg=bg_color)
        self.text_widget.configure(bg=bg_color, fg=fg_color, font=(font_family, font_size))

class StickyNotesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.data_file = Path.home() / "stickity_stacks_notes_win.json"
        self.notes = []
        self.note_counter = 1
        self.font_family = "Segoe UI"
        self.font_size = 11
        self.fg_color = "#1a1a1a"
        self.bg_color = "#fffad1"
        
        # Force root to update before creating notes
        self.root.update_idletasks()
        
        self.load_preferences()
        self.load_notes()
        if not self.notes:
            self.create_new_note()
        self.root.bind_all("<Control-n>", lambda e: self.create_new_note())
        self.root.bind_all("<Control-q>", lambda e: self.quit_app())
        
    def create_new_note(self, title=None, content=""):
        if title is None:
            title = f"Note {self.note_counter}"
            self.note_counter += 1
        note = StickyNoteWindow(self.root, len(self.notes), title, content,
                               self.font_family, self.font_size, self.fg_color, self.bg_color)
        
        # Position the note
        if self.notes:
            last = self.notes[-1]
            # Make sure last note dimensions are available
            last.update_idletasks()
            note.geometry(f"+{last.winfo_x()+30}+{last.winfo_y()+30}")
        else:
            # Update root to get screen dimensions
            self.root.update_idletasks()
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            # Center the first note
            x = (sw - 280) // 2
            y = (sh - 220) // 2
            note.geometry(f"280x220+{x}+{y}")
        
        # Force update before making visible
        note.update_idletasks()
        
        self.notes.append(note)
        self.save_notes()
        return note
        
    def delete_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
            note.destroy()
        if not self.notes:
            # If all notes deleted, quit the app
            self.quit_app()
        else:
            self.save_notes()
    
    def quit_app(self):
        """Quit the entire application"""
        self.save_notes()
        for note in self.notes:
            note.destroy()
        self.root.quit()
        self.root.destroy()
            
    def open_settings_dialog(self, note=None):
        win = tk.Toplevel(self.root)
        win.title("Stickity Stacks - Settings")
        win.geometry("400x350")
        win.resizable(False, False)
        win.configure(bg="#f0f0f0")
        win.transient(self.root)
        win.grab_set()
        
        tk.Label(win, text="Customize Your Notes", font=("Segoe UI", 14, "bold"),
                bg="#f0f0f0").pack(pady=15)
        
        font_frame = tk.LabelFrame(win, text="Font", bg="#f0f0f0", padx=15, pady=10)
        font_frame.pack(padx=20, pady=10, fill=tk.X)
        font_var = tk.StringVar(value=self.font_family)
        ttk.Combobox(font_frame, textvariable=font_var,
                    values=sorted(tkfont.families()), state="readonly",
                    width=30).pack(side=tk.LEFT, padx=5)
        size_var = tk.IntVar(value=self.font_size)
        tk.Spinbox(font_frame, from_=8, to=24, textvariable=size_var,
                  width=5).pack(side=tk.LEFT, padx=5)
        
        def apply_settings():
            self.font_family = font_var.get()
            self.font_size = size_var.get()
            for n in self.notes:
                n.update_styling(self.font_family, self.font_size, self.fg_color, self.bg_color)
            self.save_preferences()
            self.save_notes()
            win.destroy()
        
        tk.Button(win, text="Apply & Close", command=apply_settings,
                 font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white",
                 padx=20, pady=5).pack(pady=15)
        
    def save_notes(self):
        data = {'notes': [{'title': n.note_title, 'content': n.get_content(),
                          'geometry': n.geometry()} for n in self.notes],
               '_prefs': {'font_family': self.font_family, 'font_size': self.font_size,
                         'fg_color': self.fg_color, 'bg_color': self.bg_color}}
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving: {e}")
            
    def load_notes(self):
        if not self.data_file.exists():
            return
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for idx, nd in enumerate(data.get('notes', []), 1):
                self.note_counter = idx
                note = self.create_new_note(nd.get('title', f"Note {idx}"), nd.get('content', ''))
                if 'geometry' in nd:
                    # Apply saved geometry after note is created
                    note.update_idletasks()
                    note.geometry(nd['geometry'])
        except Exception as e:
            print(f"Error loading: {e}")
            
    def load_preferences(self):
        if not self.data_file.exists():
            return
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            prefs = data.get('_prefs', {})
            self.font_family = prefs.get('font_family', self.font_family)
            self.font_size = prefs.get('font_size', self.font_size)
            self.fg_color = prefs.get('fg_color', self.fg_color)
            self.bg_color = prefs.get('bg_color', self.bg_color)
        except Exception as e:
            print(f"Error loading prefs: {e}")
            
    def save_preferences(self):
        try:
            data = json.load(open(self.data_file, 'r')) if self.data_file.exists() else {'notes': []}
            data['_prefs'] = {'font_family': self.font_family, 'font_size': self.font_size,
                            'fg_color': self.fg_color, 'bg_color': self.bg_color}
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving prefs: {e}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StickyNotesApp()
    app.run()
