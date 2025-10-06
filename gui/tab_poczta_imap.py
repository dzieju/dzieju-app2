import tkinter as tk
from tkinter import ttk


class ImapTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create a label with centered text
        label = ttk.Label(
            self, 
            text="tu będzie wyszukiwanie poczty IMAP",
            font=("Arial", 14)
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
