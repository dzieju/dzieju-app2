import tkinter as tk
from tkinter import ttk
from gui.mail_config_widget import MailConfigWidget
from gui.tab_mail_search import MailSearchTab
from gui.tab_system import SystemTab
from gui.tab_zakupy import ZakupiTab
from gui.tab_poczta_imap import TabPocztaIMAP
from tools import logger
from tools.version_info import format_title_bar

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        logger.log("Inicjalizacja MainWindow")

        # Pastelowe tło okna
        try:
            self.configure(bg='#e6f2ff')
        except Exception:
            # Some platforms/styles may not allow tk bg on ttk widgets; ignore if fails
            pass

        # Set title with program name, PR number, and version
        title_text = format_title_bar()
        self.title(title_text)
        logger.log(f"Tytuł aplikacji ustawiony: {title_text}")
        self.geometry("900x600")

        style = ttk.Style(self)
        # keep existing theme, use clam for better styling control
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Pastel notebook/tab styles
        style.configure("TNotebook.Tab", background="#cce6ff", foreground="#1a1a1a", font=('Arial', 11, 'bold'), padding=[10, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", "#80bfff"), ("active", "#b3daff")],
                  foreground=[("selected", "#1a1a1a")])

        # General ttk color hints
        style.configure("TFrame", background="#e6f2ff")
        style.configure("TLabel", background="#e6f2ff", foreground="#1a1a1a", font=('Arial', 11))
        style.configure("TButton", background="#cce6ff", foreground="#1a1a1a", font=('Arial', 10, 'bold'))
        style.map("TButton", background=[("active", "#b3daff")])

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)
        logger.log("Utworzenie głównego Notebook")

        # Zakładka: Poczta Exchange
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

        # Zakładka: System
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