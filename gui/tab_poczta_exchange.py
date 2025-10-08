"""
Tab for Exchange mail with sub-tabs for search and configuration
"""
import tkinter as tk
from tkinter import ttk
from gui.tab_exchange_search import ExchangeSearchTab
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
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        # Sub-tab: Wyszukiwanie (Search)
        self.search_tab = ExchangeSearchTab(self.notebook)
        self.notebook.add(self.search_tab, text="Wyszukiwanie")
        
        # Sub-tab: Konfiguracja poczty (Mail Configuration)
        self.config_tab = ExchangeMailConfigWidget(self.notebook)
        self.notebook.add(self.config_tab, text="Konfiguracja poczty")
        
        # Connect configuration changes to search tab refresh
        self.config_tab.on_config_saved = self._on_config_changed
        
        # Add reference to config tab in search tab for easy navigation
        self.search_tab.config_tab_callback = self._open_config_tab
    
    def _on_config_changed(self):
        """Called when configuration is saved - refresh search tab account info"""
        if hasattr(self.search_tab, 'update_account_info_display'):
            self.search_tab.update_account_info_display()
    
    def _open_config_tab(self):
        """Switch to configuration tab"""
        self.notebook.select(self.config_tab)
