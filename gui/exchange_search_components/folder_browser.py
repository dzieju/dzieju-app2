"""
Exchange Folder Browser Component
Displays folder hierarchy with icons, message counts, and sizes
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from tools.logger import log


class FolderInfo:
    """Container for folder information"""
    def __init__(self, name, display_name, message_count=0, size=0, flags=None, delimiter='/'):
        self.name = name
        self.display_name = display_name
        self.message_count = message_count
        self.size = size
        self.flags = flags or []
        self.delimiter = delimiter
        self.is_special = self._detect_special_folder()
        self.icon = self._get_icon()
    
    def _detect_special_folder(self):
        """Detect if this is a special folder based on flags and name"""
        # Build flag string (empty if no flags)
        flag_str = ' '.join(str(f) for f in self.flags).upper() if self.flags else ''
        name_upper = self.name.upper()
        
        # Extract last part of folder path for better detection
        # e.g., "recepcja@woox.pl/Odebrane" -> "ODEBRANE"
        folder_basename = name_upper.split('/')[-1].split('.')[-1]
        
        # SPECIAL-USE flags (RFC 6154) OR name-based detection (English and Polish)
        if '\\INBOX' in flag_str or name_upper == 'INBOX' or folder_basename in ('ODEBRANE', 'PRZYCHODZĄCE'):
            return 'inbox'
        elif '\\SENT' in flag_str or folder_basename in ('WYSLANE', 'WYSŁANE', 'SENT ITEMS', 'SENT'):
            return 'sent'
        elif '\\DRAFTS' in flag_str or folder_basename in ('DRAFT', 'DRAFTS', 'SZKICE', 'ROBOCZE'):
            return 'drafts'
        elif '\\TRASH' in flag_str or folder_basename in ('TRASH', 'DELETED ITEMS', 'DELETED', 'KOSZ', 'ŚMIECI'):
            return 'trash'
        elif '\\JUNK' in flag_str or folder_basename in ('SPAM', 'JUNK', 'JUNK EMAIL'):
            return 'spam'
        elif '\\ARCHIVE' in flag_str or folder_basename in ('ARCHIVE', 'ARCHIWUM'):
            return 'archive'
        elif folder_basename in ('OUTBOX', 'SKRZYNKA NADAWCZA'):
            return 'outbox'
        
        return None
    
    def _get_icon(self):
        """Get icon/emoji for folder type"""
        if self.is_special == 'inbox':
            return '📥'
        elif self.is_special == 'sent':
            return '📤'
        elif self.is_special == 'drafts':
            return '📝'
        elif self.is_special == 'trash':
            return '🗑️'
        elif self.is_special == 'spam':
            return '⚠️'
        elif self.is_special == 'archive':
            return '📦'
        elif self.is_special == 'outbox':
            return '📮'
        else:
            return '📁'
    
    def get_display_name_polish(self):
        """Get Polish display name for system folders"""
        if self.is_special == 'inbox':
            return 'Odebrane'
        elif self.is_special == 'sent':
            return 'Wysłane'
        elif self.is_special == 'drafts':
            return 'Szkice'
        elif self.is_special == 'trash':
            return 'Kosz'
        elif self.is_special == 'spam':
            return 'Spam'
        elif self.is_special == 'archive':
            return 'Archiwum'
        elif self.is_special == 'outbox':
            return 'Skrzynka nadawcza'
        else:
            # For custom folders, use FolderNameMapper to get Polish name if available
            from gui.exchange_search_components.mail_connection import FolderNameMapper
            return FolderNameMapper.get_folder_display_name(self.display_name, "exchange")
    
    def format_size(self):
        """Format size in human-readable format"""
        if self.size == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(self.size)
        unit_index = 0
        
        while size >= 1024.0 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"


class FolderBrowser(ttk.Frame):
    """
    Exchange Folder Browser with tree view
    Displays folders with icons, message counts, and sizes
    """
    
    def __init__(self, parent, mail_connection):
        super().__init__(parent)
        self.mail_connection = mail_connection
        self.folders = []
        self.folder_map = {}  # Map folder names to FolderInfo objects
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the folder browser UI"""
        # Top control panel
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(control_frame, text="Foldery Exchange", font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        
        self.refresh_button = ttk.Button(control_frame, text="🔄 Odśwież foldery", command=self.refresh_folders)
        self.refresh_button.pack(side='right', padx=5)
        
        # Account info label
        self.account_label = ttk.Label(control_frame, text="Konto: nie połączono", foreground='gray')
        self.account_label.pack(side='right', padx=10)
        
        # Status label
        self.status_label = ttk.Label(self, text="Kliknij 'Odśwież foldery' aby pobrać listę folderów", foreground='gray')
        self.status_label.pack(fill='x', padx=5, pady=2)
        
        # Create treeview with columns
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, 
                                  columns=('messages', 'size'),
                                  yscrollcommand=vsb.set,
                                  xscrollcommand=hsb.set,
                                  selectmode='browse')
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure columns
        self.tree.heading('#0', text='Nazwa folderu', anchor='w')
        self.tree.heading('messages', text='Wiadomości', anchor='e')
        self.tree.heading('size', text='Rozmiar', anchor='e')
        
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('messages', width=120, minwidth=80, anchor='e')
        self.tree.column('size', width=120, minwidth=80, anchor='e')
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_folder_double_click)
    
    def refresh_folders(self):
        """Refresh folder list in background thread"""
        self.refresh_button.config(state='disabled')
        self.status_label.config(text="Pobieranie listy folderów...", foreground='blue')
        
        threading.Thread(target=self._refresh_folders_thread, daemon=True).start()
    
    def _refresh_folders_thread(self):
        """Background thread for folder refresh"""
        try:
            # Get Exchange account
            account = self.mail_connection.get_exchange_account()
            
            if not account:
                self.after_idle(lambda: self._show_error("Brak konta Exchange - skonfiguruj konto w zakładce 'Konfiguracja poczty'"))
                return
            
            # Get account config
            account_config = self.mail_connection.current_account_config
            if not account_config:
                self.after_idle(lambda: self._show_error("Brak konfiguracji konta"))
                return
            
            account_name = account_config.get('name', 'Unknown')
            account_email = account_config.get('email', '')
            
            log(f"[FOLDER BROWSER] Refreshing folders for Exchange account: {account_name} ({account_email})")
            
            # Update account label
            self.after_idle(lambda: self.account_label.config(
                text=f"Konto: {account_name} ({account_email})",
                foreground='black'
            ))
            
            # Use the enhanced method to get folders with details
            folders_data = self.mail_connection.get_folders_with_details(account_config)
            
            if not folders_data:
                self.after_idle(lambda: self._show_error("Nie można pobrać listy folderów z serwera Exchange"))
                return
            
            folders_info = []
            
            for folder_data in folders_data:
                try:
                    # Create FolderInfo object from the data
                    folder_info = FolderInfo(
                        name=folder_data['name'],
                        display_name=folder_data['name'],
                        message_count=folder_data['message_count'],
                        size=folder_data['size'],
                        flags=folder_data['flags'],
                        delimiter=folder_data['delimiter']
                    )
                    
                    folders_info.append(folder_info)
                    
                except Exception as folder_error:
                    log(f"[FOLDER BROWSER] Error processing folder data: {folder_error}")
                    continue
            
            # Update UI
            self.after_idle(lambda: self._update_tree(folders_info))
            self.after_idle(lambda: self.status_label.config(
                text=f"Znaleziono {len(folders_info)} folderów Exchange",
                foreground='green'
            ))
            
        except Exception as e:
            log(f"[FOLDER BROWSER] Error refreshing Exchange folders: {e}")
            self.after_idle(lambda: self._show_error(f"Błąd pobierania folderów Exchange: {str(e)}"))
        finally:
            self.after_idle(lambda: self.refresh_button.config(state='normal'))
    
    def _update_tree(self, folders_info):
        """Update tree view with folder information using proper hierarchy"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.folder_map = {}
        
        # Sort folders: system folders first, then alphabetically
        system_folders = [f for f in folders_info if f.is_special]
        custom_folders = [f for f in folders_info if not f.is_special]
        
        # Sort system folders by predefined order
        system_order = ['inbox', 'drafts', 'sent', 'spam', 'trash', 'archive']
        system_folders.sort(key=lambda f: system_order.index(f.is_special) if f.is_special in system_order else 999)
        
        # Sort custom folders alphabetically
        custom_folders.sort(key=lambda f: f.name.lower())
        
        # Build hierarchical structure
        # Map of folder paths to tree item IDs for parent lookup
        path_to_item = {}
        
        # Process system folders first (always at root level)
        for folder in system_folders:
            display_name = f"{folder.icon} {folder.get_display_name_polish()}"
            item_id = self.tree.insert('', 'end', 
                                       text=display_name,
                                       values=(
                                           f"{folder.message_count:,}",
                                           folder.format_size()
                                       ),
                                       tags=(folder.name,))
            self.folder_map[item_id] = folder
            path_to_item[folder.name] = item_id
        
        # Process custom folders with hierarchy support
        for folder in custom_folders:
            parent_id = ''
            
            # Check if folder has parent (contains delimiter)
            if folder.delimiter and folder.delimiter in folder.name:
                parts = folder.name.split(folder.delimiter)
                # Look for parent folder
                parent_path = folder.delimiter.join(parts[:-1])
                if parent_path in path_to_item:
                    parent_id = path_to_item[parent_path]
            
            # Get display name (just the last part for hierarchical folders)
            if folder.delimiter and folder.delimiter in folder.name:
                parts = folder.name.split(folder.delimiter)
                display_name = f"{folder.icon} {parts[-1]}"
            else:
                display_name = f"{folder.icon} {folder.get_display_name_polish()}"
            
            # Insert into tree
            item_id = self.tree.insert(parent_id, 'end', 
                                       text=display_name,
                                       values=(
                                           f"{folder.message_count:,}",
                                           folder.format_size()
                                       ),
                                       tags=(folder.name,))
            
            self.folder_map[item_id] = folder
            path_to_item[folder.name] = item_id
    
    def _show_error(self, message):
        """Show error message"""
        self.status_label.config(text=message, foreground='red')
        self.refresh_button.config(state='normal')
    
    def on_folder_double_click(self, event):
        """Handle double-click on folder"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        if item_id in self.folder_map:
            folder = self.folder_map[item_id]
            messagebox.showinfo(
                "Informacje o folderze",
                f"Folder: {folder.get_display_name_polish()}\n"
                f"Ścieżka: {folder.name}\n"
                f"Liczba wiadomości: {folder.message_count:,}\n"
                f"Szacowany rozmiar: {folder.format_size()}\n"
                f"Typ: {'Systemowy' if folder.is_special else 'Własny'}"
            )
