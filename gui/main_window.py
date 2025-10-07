import tkinter as tk
from tkinter import ttk
from gui.mail_config_widget import MailConfigWidget
from gui.tab_mail_search import MailSearchTab
from gui.tab_poczta_imap import TabPocztaIMAP
from gui.tab_system import SystemTab
from gui.tab_zakupy import ZakupiTab
from tools import logger
from tools.version_info import format_title_bar

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        logger.log("Inicjalizacja MainWindow")
        
        # Set title with program name, PR number, and version
        title_text = format_title_bar()
        self.title(title_text)
        logger.log(f"Tytuł aplikacji ustawiony: {title_text}")
        self.geometry("900x600")

        # Apply neutral background color
        self.configure(bg="#F8FAFC")  # Light gray background
        
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Configure pastel styles for notebook tabs
        style.configure("TNotebook", background="#F8FAFC", borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background="#E8F4FF",  # Pastel blue
                       foreground="#333333",
                       padding=[20, 10],
                       borderwidth=1,
                       relief="raised")
        style.map("TNotebook.Tab",
                 background=[("selected", "#E8F4FF"),  # Pastel blue when selected
                            ("active", "#E8FFE8")],     # Pastel green on hover
                 foreground=[("selected", "#000000")])
        
        # Configure pastel styles for labels
        style.configure("TLabel",
                       background="#F8FAFC",  # Match main window background
                       foreground="#333333")
        
        # Configure pastel styles for buttons
        style.configure("TButton",
                       background="#E8F4FF",  # Pastel blue
                       foreground="#333333",
                       borderwidth=1,
                       relief="raised",
                       padding=[10, 5])
        style.map("TButton",
                 background=[("active", "#E8FFE8"),     # Pastel green on hover
                            ("pressed", "#E8F4FF")],    # Pastel blue when pressed
                 relief=[("pressed", "sunken")])
        
        logger.log("Konfiguracja stylu GUI zakończona (pastel theme)")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        logger.log("Utworzenie głównego Notebook")

        # Zakładka: Poczta Exchange (first tab)
        logger.log("Ładowanie zakładki: Poczta Exchange")
        mail_search_tab = MailSearchTab(notebook)
        notebook.add(mail_search_tab, text="Poczta Exchange")
        logger.log("Zakładka 'Poczta Exchange' załadowana")

        # Zakładka: Poczta IMAP
        logger.log("Ładowanie zakładki: Poczta IMAP")
        imap_tab = TabPocztaIMAP(notebook)
        notebook.add(imap_tab, text="Poczta IMAP")
        logger.log("Zakładka 'Poczta IMAP' załadowana")

        # Zakładka: Konfiguracja poczty
        logger.log("Ładowanie zakładki: Konfiguracja poczty")
        mail_config_tab = MailConfigWidget(notebook)
        notebook.add(mail_config_tab, text="Konfiguracja poczty")
        logger.log("Zakładka 'Konfiguracja poczty' załadowana")

        # Zakładka: Zakupy
        logger.log("Ładowanie zakładki: Zakupy")
        zakupy_tab = ZakupiTab(notebook)
        notebook.add(zakupy_tab, text="Zakupy")
        logger.log("Zakładka 'Zakupy' załadowana")

        # Dodanie rozbudowanej zakładki System
        logger.log("Ładowanie zakładki: System")
        system_tab = SystemTab(notebook)
        notebook.add(system_tab, text="System")
        logger.log("Zakładka 'System' załadowana")
        
        # Store reference to system tab for title updates
        self.system_tab = system_tab
        
        logger.log("MainWindow - wszystkie komponenty załadowane pomyślnie")
    
    def refresh_title_bar(self):
        """Refresh the title bar with current version information."""
        title_text = format_title_bar()
        self.title(title_text)
        logger.log(f"Tytuł aplikacji odświeżony: {title_text}")
        
        # Also refresh system tab if it exists
        if hasattr(self, 'system_tab') and self.system_tab:
            self.system_tab.refresh_version_info()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()