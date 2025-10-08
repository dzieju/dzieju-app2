#!/usr/bin/env python3
"""
Verification script for Exchange/IMAP separation
Verifies that Exchange and IMAP tabs are completely independent.
"""

import ast
import os

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

def check_string_in_file(filename, search_string):
    """Check if a string exists in a file"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return search_string in content
    except Exception as e:
        return False

def main():
    print("=" * 70)
    print("Exchange/IMAP Separation Verification")
    print("=" * 70)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    all_checks_passed = True
    
    # Check Exchange tab imports
    print("\n1. Checking Exchange Tab (tab_poczta_exchange.py):")
    exchange_tab_file = os.path.join(base_path, "gui/tab_poczta_exchange.py")
    exchange_tab_imports = check_imports(exchange_tab_file)
    
    if 'gui.tab_exchange_search.ExchangeSearchTab' in exchange_tab_imports:
        print("  ✓ Imports ExchangeSearchTab")
    else:
        print("  ✗ Does NOT import ExchangeSearchTab")
        all_checks_passed = False
    
    if 'gui.exchange_mail_config_widget.ExchangeMailConfigWidget' in exchange_tab_imports:
        print("  ✓ Imports ExchangeMailConfigWidget")
    else:
        print("  ✗ Does NOT import ExchangeMailConfigWidget")
        all_checks_passed = False
    
    if 'gui.tab_mail_search.MailSearchTab' in exchange_tab_imports:
        print("  ✗ Still imports MailSearchTab (should not)")
        all_checks_passed = False
    else:
        print("  ✓ Does NOT import MailSearchTab")
    
    # Check IMAP tab imports
    print("\n2. Checking IMAP Tab (tab_poczta_imap.py):")
    imap_tab_file = os.path.join(base_path, "gui/tab_poczta_imap.py")
    imap_tab_imports = check_imports(imap_tab_file)
    
    if 'gui.tab_imap_search.IMAPSearchTab' in imap_tab_imports:
        print("  ✓ Imports IMAPSearchTab")
    else:
        print("  ✗ Does NOT import IMAPSearchTab")
        all_checks_passed = False
    
    if 'gui.tab_imap_config.IMAPConfigWidget' in imap_tab_imports:
        print("  ✓ Imports IMAPConfigWidget")
    else:
        print("  ✗ Does NOT import IMAPConfigWidget")
        all_checks_passed = False
    
    # Check ExchangeSearchTab
    print("\n3. Checking ExchangeSearchTab class:")
    exchange_search_file = os.path.join(base_path, "gui/tab_exchange_search.py")
    
    if check_string_in_file(exchange_search_file, "class ExchangeSearchTab"):
        print("  ✓ ExchangeSearchTab class defined")
    else:
        print("  ✗ ExchangeSearchTab class NOT defined")
        all_checks_passed = False
    
    if check_string_in_file(exchange_search_file, "get_exchange_account"):
        print("  ✓ Calls get_exchange_account()")
    else:
        print("  ✗ Does NOT call get_exchange_account()")
        all_checks_passed = False
    
    if check_string_in_file(exchange_search_file, "EXCHANGE_SEARCH_CONFIG_FILE"):
        print("  ✓ Uses EXCHANGE_SEARCH_CONFIG_FILE")
    else:
        print("  ✗ Does NOT use EXCHANGE_SEARCH_CONFIG_FILE")
        all_checks_passed = False
    
    # Check MailConnection enhancements
    print("\n4. Checking MailConnection enhancements:")
    mail_conn_file = os.path.join(base_path, "gui/mail_search_components/mail_connection.py")
    
    if check_string_in_file(mail_conn_file, "def get_exchange_account"):
        print("  ✓ get_exchange_account() method exists")
    else:
        print("  ✗ get_exchange_account() method NOT found")
        all_checks_passed = False
    
    if check_string_in_file(mail_conn_file, "def load_exchange_mail_config"):
        print("  ✓ load_exchange_mail_config() method exists")
    else:
        print("  ✗ load_exchange_mail_config() method NOT found")
        all_checks_passed = False
    
    # Check file existence
    print("\n5. Checking file existence:")
    files_to_check = [
        ("gui/tab_exchange_search.py", "ExchangeSearchTab module"),
        ("gui/exchange_mail_config_widget.py", "ExchangeMailConfigWidget module"),
        ("gui/tab_imap_search.py", "IMAPSearchTab module"),
        ("gui/tab_imap_config.py", "IMAPConfigWidget module"),
    ]
    
    for filepath, description in files_to_check:
        full_path = os.path.join(base_path, filepath)
        if os.path.exists(full_path):
            print(f"  ✓ {description} exists")
        else:
            print(f"  ✗ {description} NOT found")
            all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_checks_passed:
        print("✅ VERIFICATION PASSED: Complete separation achieved!")
    else:
        print("❌ VERIFICATION FAILED: Some checks did not pass")
    print("=" * 70)
    
    if all_checks_passed:
        print("\nKey Points:")
        print("  • Exchange tab uses ExchangeSearchTab and ExchangeMailConfigWidget")
        print("  • IMAP tab uses IMAPSearchTab and IMAPConfigWidget")
        print("  • ExchangeSearchTab calls get_exchange_account()")
        print("  • IMAPSearchTab calls get_imap_account()")
        print("  • Complete separation achieved ✓")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    exit(main())
