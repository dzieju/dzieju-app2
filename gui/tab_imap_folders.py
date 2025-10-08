"""
IMAP Folders Tab
Displays IMAP folder structure with icons, message counts, and sizes
"""
import tkinter as tk
from tkinter import ttk
from gui.imap_search_components.folder_browser import FolderBrowser
from gui.imap_search_components.mail_connection import MailConnection


class IMAPFoldersTab(ttk.Frame):
    """Tab for browsing IMAP folders"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize mail connection
        self.connection = MailConnection()
        
        # Create folder browser
        self.folder_browser = FolderBrowser(self, self.connection)
        self.folder_browser.pack(fill='both', expand=True)
        
        # Auto-refresh on tab open
        self.bind('<Visibility>', self._on_visibility)
        self._first_visibility = True
    
    def _on_visibility(self, event):
        """Called when tab becomes visible"""
        if self._first_visibility and event.widget == self:
            self._first_visibility = False
            # Auto-refresh folders on first visibility
            self.after(500, self.folder_browser.refresh_folders)
