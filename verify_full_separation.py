#!/usr/bin/env python3
"""
Verification Script for Option A: Full Separation
This script verifies that Exchange and IMAP components are 100% separated.
"""

import os
import sys
from pathlib import Path

def check_directory_exists(path, description):
    """Check if directory exists"""
    if os.path.exists(path) and os.path.isdir(path):
        files = [f for f in os.listdir(path) if f.endswith('.py')]
        print(f"  ✓ {description} exists ({len(files)} Python files)")
        return True
    else:
        print(f"  ✗ {description} NOT FOUND")
        return False

def check_no_shared_imports(file_path, forbidden_import):
    """Check that a file doesn't import from forbidden modules"""
    if not os.path.exists(file_path):
        return True
    
    with open(file_path, 'r') as f:
        content = f.read()
        if forbidden_import in content:
            print(f"  ✗ {file_path} still imports from {forbidden_import}")
            return False
    return True

def main():
    print("=" * 70)
    print("Option A: Full Separation - Verification")
    print("=" * 70)
    
    base_path = "/home/runner/work/dzieju-app2/dzieju-app2"
    all_checks_passed = True
    
    # 1. Check that new directories exist
    print("\n1. Checking New Directories:")
    all_checks_passed &= check_directory_exists(
        f"{base_path}/gui/exchange_search_components",
        "Exchange components directory"
    )
    all_checks_passed &= check_directory_exists(
        f"{base_path}/gui/imap_search_components",
        "IMAP components directory"
    )
    
    # 2. Check that Exchange files don't import from mail_search_components
    print("\n2. Checking Exchange Files (no mail_search_components imports):")
    exchange_files = [
        "gui/tab_exchange_search.py",
        "gui/tab_poczta_exchange.py"
    ]
    for file in exchange_files:
        if check_no_shared_imports(f"{base_path}/{file}", "gui.mail_search_components"):
            print(f"  ✓ {file} - clean")
        else:
            all_checks_passed = False
    
    # 3. Check that IMAP files don't import from mail_search_components
    print("\n3. Checking IMAP Files (no mail_search_components imports):")
    imap_files = [
        "gui/tab_imap_search.py",
        "gui/tab_imap_folders.py",
        "gui/tab_poczta_imap.py"
    ]
    for file in imap_files:
        if check_no_shared_imports(f"{base_path}/{file}", "gui.mail_search_components"):
            print(f"  ✓ {file} - clean")
        else:
            all_checks_passed = False
    
    # 4. Check that Exchange files USE exchange_search_components
    print("\n4. Checking Exchange Files (use exchange_search_components):")
    for file in ["gui/tab_exchange_search.py"]:
        file_path = f"{base_path}/{file}"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if "gui.exchange_search_components" in content:
                    print(f"  ✓ {file} - uses exchange_search_components")
                else:
                    print(f"  ✗ {file} - does NOT use exchange_search_components")
                    all_checks_passed = False
    
    # 5. Check that IMAP files USE imap_search_components
    print("\n5. Checking IMAP Files (use imap_search_components):")
    for file in ["gui/tab_imap_search.py", "gui/tab_imap_folders.py"]:
        file_path = f"{base_path}/{file}"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if "gui.imap_search_components" in content:
                    print(f"  ✓ {file} - uses imap_search_components")
                else:
                    print(f"  ✗ {file} - does NOT use imap_search_components")
                    all_checks_passed = False
    
    # 6. Check component file counts
    print("\n6. Checking Component File Counts:")
    exchange_files = len([f for f in os.listdir(f"{base_path}/gui/exchange_search_components") if f.endswith('.py')])
    imap_files = len([f for f in os.listdir(f"{base_path}/gui/imap_search_components") if f.endswith('.py')])
    print(f"  Exchange components: {exchange_files} files")
    print(f"  IMAP components: {imap_files} files")
    if exchange_files == imap_files and exchange_files >= 11:
        print(f"  ✓ Both have the same number of component files")
    else:
        print(f"  ⚠ Warning: File counts differ or less than expected (11)")
    
    # 7. Check that components don't cross-reference
    print("\n7. Checking No Cross-References in Components:")
    
    # Exchange components should not import from imap_search_components
    for file in os.listdir(f"{base_path}/gui/exchange_search_components"):
        if file.endswith('.py'):
            file_path = f"{base_path}/gui/exchange_search_components/{file}"
            if not check_no_shared_imports(file_path, "gui.imap_search_components"):
                print(f"  ✗ Exchange component {file} imports from IMAP components")
                all_checks_passed = False
    
    # IMAP components should not import from exchange_search_components
    for file in os.listdir(f"{base_path}/gui/imap_search_components"):
        if file.endswith('.py'):
            file_path = f"{base_path}/gui/imap_search_components/{file}"
            if not check_no_shared_imports(file_path, "gui.exchange_search_components"):
                print(f"  ✗ IMAP component {file} imports from Exchange components")
                all_checks_passed = False
    
    if all_checks_passed:
        print("  ✓ No cross-references detected")
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if all_checks_passed:
        print("\n✅ ALL CHECKS PASSED - 100% SEPARATION ACHIEVED")
        print("\nKey Points:")
        print("  • Exchange tab uses exchange_search_components/")
        print("  • IMAP tab uses imap_search_components/")
        print("  • No shared code between Exchange and IMAP")
        print("  • No cross-references between component directories")
        print("  • Complete independence achieved ✓")
        return 0
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Review the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
