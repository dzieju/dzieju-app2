import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import queue
from imapclient import IMAPClient
import smtplib
import ssl

CONFIG_FILE = "imap_config.json"

class ImapConfigTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Threading support variables
        self.testing_cancelled = False
        self.testing_thread = None
        self.result_queue = queue.Queue()

        # Input fields
        self.imap_server_var = tk.StringVar()
        self.imap_port_var = tk.StringVar(value="993")
        self.email_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.imap_ssl_var = tk.BooleanVar(value=True)
        
        # SMTP fields
        self.smtp_server_var = tk.StringVar()
        self.smtp_port_var = tk.StringVar(value="587")
        self.smtp_ssl_var = tk.BooleanVar(value=True)

        # IMAP Settings Section
        imap_frame = ttk.LabelFrame(self, text="Ustawienia IMAP (odbiór)", padding=10)
        imap_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ttk.Label(imap_frame, text="Serwer IMAP:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(imap_frame, textvariable=self.imap_server_var, width=40).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(imap_frame, text="Port IMAP:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(imap_frame, textvariable=self.imap_port_var, width=40).grid(row=1, column=1, padx=5, pady=5)

        ttk.Checkbutton(imap_frame, text="Użyj SSL/TLS", variable=self.imap_ssl_var).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # SMTP Settings Section
        smtp_frame = ttk.LabelFrame(self, text="Ustawienia SMTP (wysyłanie)", padding=10)
        smtp_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ttk.Label(smtp_frame, text="Serwer SMTP:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(smtp_frame, textvariable=self.smtp_server_var, width=40).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(smtp_frame, text="Port SMTP:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(smtp_frame, textvariable=self.smtp_port_var, width=40).grid(row=1, column=1, padx=5, pady=5)

        ttk.Checkbutton(smtp_frame, text="Użyj SSL/TLS", variable=self.smtp_ssl_var).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Account Details Section
        account_frame = ttk.LabelFrame(self, text="Dane konta", padding=10)
        account_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        ttk.Label(account_frame, text="Adres e-mail:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(account_frame, textvariable=self.email_var, width=40).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(account_frame, text="Login użytkownika:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(account_frame, textvariable=self.username_var, width=40).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(account_frame, text="Hasło:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(account_frame, textvariable=self.password_var, show="*", width=40).grid(row=2, column=1, padx=5, pady=5)

        # Buttons and status
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Zapisz ustawienia", command=self.save_config).pack(side="left", padx=5)
        
        self.test_button = ttk.Button(button_frame, text="Testuj połączenie", command=self.toggle_test_connection)
        self.test_button.pack(side="left", padx=5)
        
        self.status_label = ttk.Label(button_frame, text="Gotowy", foreground="green")
        self.status_label.pack(side="left", padx=10)

        self.load_config()
        
        # Start processing queue
        self._process_result_queue()

    def save_config(self):
        config = {
            "imap_server": self.imap_server_var.get(),
            "imap_port": self.imap_port_var.get(),
            "imap_ssl": self.imap_ssl_var.get(),
            "smtp_server": self.smtp_server_var.get(),
            "smtp_port": self.smtp_port_var.get(),
            "smtp_ssl": self.smtp_ssl_var.get(),
            "email": self.email_var.get(),
            "username": self.username_var.get(),
            "password": self.password_var.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        messagebox.showinfo("Zapisano", "Ustawienia IMAP zostały zapisane.")

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.imap_server_var.set(config.get("imap_server", ""))
                self.imap_port_var.set(config.get("imap_port", "993"))
                self.imap_ssl_var.set(config.get("imap_ssl", True))
                self.smtp_server_var.set(config.get("smtp_server", ""))
                self.smtp_port_var.set(config.get("smtp_port", "587"))
                self.smtp_ssl_var.set(config.get("smtp_ssl", True))
                self.email_var.set(config.get("email", ""))
                self.username_var.set(config.get("username", ""))
                self.password_var.set(config.get("password", ""))
        except FileNotFoundError:
            pass

    def toggle_test_connection(self):
        """Toggle between starting and cancelling connection test"""
        if self.testing_thread and self.testing_thread.is_alive():
            self.cancel_test_connection()
        else:
            self.start_test_connection()
    
    def cancel_test_connection(self):
        """Cancel ongoing connection test"""
        self.testing_cancelled = True
        self.status_label.config(text="Anulowanie...", foreground="orange")
        self.test_button.config(text="Testuj połączenie")
    
    def start_test_connection(self):
        """Start the threaded connection test"""
        # Reset cancellation flag
        self.testing_cancelled = False
        
        # Update UI
        self.test_button.config(text="Anuluj test")
        self.status_label.config(text="Testowanie połączenia IMAP...", foreground="blue")

        # Start testing in background thread
        self.testing_thread = threading.Thread(
            target=self._threaded_connection_test,
            daemon=True
        )
        self.testing_thread.start()
    
    def _threaded_connection_test(self):
        """Connection test logic running in background thread"""
        try:
            if self.testing_cancelled:
                self.result_queue.put({'type': 'test_cancelled'})
                return
            
            # Test IMAP connection
            imap_port = int(self.imap_port_var.get())
            imap = IMAPClient(
                self.imap_server_var.get(),
                port=imap_port,
                ssl=self.imap_ssl_var.get()
            )
            
            if self.testing_cancelled:
                self.result_queue.put({'type': 'test_cancelled'})
                return
            
            imap.login(self.username_var.get(), self.password_var.get())
            
            if self.testing_cancelled:
                imap.logout()
                self.result_queue.put({'type': 'test_cancelled'})
                return
            
            # Try to select inbox to verify connection
            imap.select_folder('INBOX')
            imap.logout()
            
            self.result_queue.put({
                'type': 'test_success',
                'email': self.email_var.get()
            })
        except Exception as e:
            self.result_queue.put({
                'type': 'test_error',
                'error': str(e)
            })
    
    def _process_result_queue(self):
        """Process results from worker thread"""
        try:
            while True:
                try:
                    result = self.result_queue.get_nowait()
                    
                    if result['type'] == 'test_success':
                        email = result['email']
                        messagebox.showinfo("Połączenie OK", f"Połączono z kontem IMAP: {email}")
                        self.status_label.config(text="Test połączenia udany", foreground="green")
                        self.test_button.config(text="Testuj połączenie")
                        
                    elif result['type'] == 'test_cancelled':
                        self.status_label.config(text="Test anulowany", foreground="orange")
                        self.test_button.config(text="Testuj połączenie")
                        
                    elif result['type'] == 'test_error':
                        error_msg = result['error']
                        messagebox.showerror("Błąd połączenia IMAP", error_msg)
                        self.status_label.config(text="Błąd połączenia", foreground="red")
                        self.test_button.config(text="Testuj połączenie")
                        
                except queue.Empty:
                    break
        except Exception as e:
            print(f"Błąd przetwarzania kolejki wyników: {e}")
        
        # Schedule next check
        self.after(100, self._process_result_queue)

    def test_connection(self):
        """Legacy method for backward compatibility"""
        self.start_test_connection()
    
    def destroy(self):
        """Cleanup when widget is destroyed"""
        if self.testing_thread and self.testing_thread.is_alive():
            self.testing_cancelled = True
        super().destroy()
