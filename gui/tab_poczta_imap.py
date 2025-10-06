import tkinter as tk
from tkinter import ttk

class TabPocztaIMAP(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        label = ttk.Label(
            self,
            text="tu będzie wyszukiwanie poczty IMAP",
            font=("Arial", 16)
        )
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)