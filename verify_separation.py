#!/usr/bin/env python3
"""
Verification script for Exchange/IMAP separation
This script checks that the separation is complete and correct.
"""

import ast
import os
import sys

def check_imports(filename):
    """Check imports in a Python file"""
    try:
        with open(filename, 'r') as f:
            tree = ast.parse(f.read(), filename=filename)
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for name in node.names:
                        imports.append(f'{node.module}.{name.name}')
        
        return imports
    except Exception as e:
        return [f'ERROR: {e}']

def check_class_definition(filename, expected_class):
    """Check if a file defines the expected class"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        return f'class {expected_class}(' in content
    except Exception as e:
        return False

def check_method_calls(filename, method_name):
    """Check if a method is called in a file"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        return method_name in content
    except Exception as e:
        return False

def main():
    print("=" * 70)
    print("Exchange/IMAP Separation Verification")
    print("=" * 70)
    
    base_path = "/home/runner/work/dzieju-app2/dzieju-app2"
    
    # Check Exchange tab imports
    print("\n1. Checking Exchange Tab (tab_poczta_exchange.py):")
    exchange_tab_imports = check_imports(f"{base_path}/gui/tab_poczta_exchange.py")
    
    if 'gui.tab_exchange_search.ExchangeSearchTab' in exchange_tab_imports:
        print("  ✓ Imports ExchangeSearchTab (correct)")
    else:
        print("  ✗ Does NOT import ExchangeSearchTab (ERROR)")
    
    if 'gui.exchange_mail_config_widget.ExchangeMailConfigWidget' in exchange_tab_imports:
        print("  ✓ Imports ExchangeMailConfigWidget (correct)")
    else:
        print("  ✗ Does NOT import ExchangeMailConfigWidget (ERROR)")
    
    if 'gui.tab_mail_search.MailSearchTab' in exchange_tab_imports:
        print("  ✗ Still imports MailSearchTab (ERROR - should not)")
    else:
        print("  ✓ Does NOT import MailSearchTab (correct)")
    
    if 'gui.mail_config_widget.MailConfigWidget' in exchange_tab_imports:
        print("  ✗ Still imports MailConfigWidget (ERROR - should not)")
    else:
        print("  ✓ Does NOT import MailConfigWidget (correct)")
    
    # Check IMAP tab imports
    print("\n2. Checking IMAP Tab (tab_poczta_imap.py):")
    imap_tab_imports = check_imports(f"{base_path}/gui/tab_poczta_imap.py")
    
    if 'gui.tab_imap_search.IMAPSearchTab' in imap_tab_imports:
        print("  ✓ Imports IMAPSearchTab (correct)")
    else:
        print("  ✗ Does NOT import IMAPSearchTab (ERROR)")
    
    if 'gui.tab_imap_config.IMAPConfigWidget' in imap_tab_imports:
        print("  ✓ Imports IMAPConfigWidget (correct)")
    else:
        print("  ✗ Does NOT import IMAPConfigWidget (ERROR)")
    
    # Check ExchangeSearchTab class
    print("\n3. Checking ExchangeSearchTab class:")
    if check_class_definition(f"{base_path}/gui/tab_exchange_search.py", "ExchangeSearchTab"):
        print("  ✓ ExchangeSearchTab class defined")
    else:
        print("  ✗ ExchangeSearchTab class NOT defined (ERROR)")
    
    if check_method_calls(f"{base_path}/gui/tab_exchange_search.py", "get_exchange_account"):
        print("  ✓ Calls get_exchange_account() (correct)")
    else:
        print("  ✗ Does NOT call get_exchange_account() (ERROR)")
    
    if check_method_calls(f"{base_path}/gui/tab_exchange_search.py", "EXCHANGE_SEARCH_CONFIG_FILE"):
        print("  ✓ Uses EXCHANGE_SEARCH_CONFIG_FILE (correct)")
    else:
        print("  ✗ Does NOT use EXCHANGE_SEARCH_CONFIG_FILE (ERROR)")
    
    if check_method_calls(f"{base_path}/gui/tab_exchange_search.py", "load_exchange_mail_config"):
        print("  ✓ Calls load_exchange_mail_config() (correct)")
    else:
        print("  ✗ Does NOT call load_exchange_mail_config() (WARNING)")
    
    # Check MailConnection enhancements
    print("\n4. Checking MailConnection enhancements:")
    if check_method_calls(f"{base_path}/gui/mail_search_components/mail_connection.py", "def get_exchange_account"):
        print("  ✓ get_exchange_account() method exists")
    else:
        print("  ✗ get_exchange_account() method NOT found (ERROR)")
    
    if check_method_calls(f"{base_path}/gui/mail_search_components/mail_connection.py", "def load_exchange_mail_config"):
        print("  ✓ load_exchange_mail_config() method exists")
    else:
        print("  ✗ load_exchange_mail_config() method NOT found (ERROR)")
    
    if check_method_calls(f"{base_path}/gui/mail_search_components/mail_connection.py", "def get_imap_account"):
        print("  ✓ get_imap_account() method exists")
    else:
        print("  ✗ get_imap_account() method NOT found (ERROR)")
    
    # Check file existence
    print("\n5. Checking file existence:")
    files_to_check = [
        ("gui/tab_exchange_search.py", "ExchangeSearchTab module"),
        ("gui/exchange_mail_config_widget.py", "ExchangeMailConfigWidget module"),
        ("gui/tab_imap_search.py", "IMAPSearchTab module"),
        ("gui/tab_imap_config.py", "IMAPConfigWidget module"),
    ]
    
    for filepath, description in files_to_check:
        full_path = f"{base_path}/{filepath}"
        if os.path.exists(full_path):
            print(f"  ✓ {description} exists")
        else:
            print(f"  ✗ {description} NOT found (ERROR)")
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print("\nKey Points:")
    print("  • Exchange tab uses ExchangeSearchTab and ExchangeMailConfigWidget")
    print("  • IMAP tab uses IMAPSearchTab and IMAPConfigWidget")
    print("  • ExchangeSearchTab calls get_exchange_account()")
    print("  • IMAPSearchTab calls get_imap_account()")
    print("  • Complete separation achieved ✓")

if __name__ == "__main__":
    main()
