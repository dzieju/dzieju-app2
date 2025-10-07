"""
Tab for Exchange mail with sub-tabs for search and configuration
"""
import tkinter as tk
from tkinter import ttk
from gui.tab_mail_search import MailSearchTab
from gui.exchange_mail_config_widget import ExchangeMailConfigWidget

class TabPocztaExchange(ttk.Frame):
    """
    Exchange mail tab with sub-tabs:
    - Wyszukiwanie (Search)
    - Konfiguracja poczty (Mail Configuration)
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create a notebook for sub-tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        
        # Sub-tab: Wyszukiwanie (Search)
        search_tab = MailSearchTab(notebook)
        notebook.add(search_tab, text="Wyszukiwanie")
        
        # Sub-tab: Konfiguracja poczty (Mail Configuration)
        config_tab = ExchangeMailConfigWidget(notebook)
        notebook.add(config_tab, text="Konfiguracja poczty")
