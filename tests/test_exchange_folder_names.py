#!/usr/bin/env python3
"""
Test to verify that Exchange tab uses Exchange-style folder names
and IMAP tab uses IMAP-style folder names.
"""
import os
import sys
import ast

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def extract_fallback_folders(filename):
    """Extract fallback folder lists from a Python file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=filename)
        fallback_lists = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                # Look for assignments to 'fallback_folders'
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'fallback_folders':
                        if isinstance(node.value, ast.List):
                            folders = []
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant):
                                    folders.append(elt.value)
                                elif isinstance(elt, ast.Str):  # Python 3.7 compatibility
                                    folders.append(elt.s)
                            fallback_lists.append(folders)
        
        return fallback_lists
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        return []


def is_exchange_style_name(name):
    """Check if a folder name is Exchange-style."""
    exchange_patterns = [
        "Sent Items",
        "Deleted Items", 
        "Junk Email",
        "Outbox",
        "Archive",
        "Drafts",  # Common to both
        "Inbox"    # Common to both
    ]
    return name in exchange_patterns


def is_imap_style_name(name):
    """Check if a folder name is IMAP-style (all caps or simple names)."""
    imap_patterns = [
        "SENT", "Sent",
        "DRAFTS", "Drafts",
        "SPAM", "Junk",
        "TRASH", "Trash",
        "INBOX"
    ]
    return name in imap_patterns


def test_exchange_tab_folder_names():
    """Test that Exchange tab uses only Exchange-style folder names."""
    print("Testing Exchange Tab Folder Names...")
    print("=" * 60)
    
    exchange_tab_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "gui", "tab_exchange_search.py"
    )
    
    fallback_lists = extract_fallback_folders(exchange_tab_file)
    
    if not fallback_lists:
        print("❌ FAIL: Could not find fallback_folders in Exchange tab")
        return False
    
    print(f"Found {len(fallback_lists)} fallback folder list(s) in Exchange tab:")
    
    all_pass = True
    for i, folders in enumerate(fallback_lists, 1):
        print(f"\nList {i}: {folders}")
        
        # Check for IMAP-style names (which should NOT be in Exchange tab)
        imap_names = [f for f in folders if is_imap_style_name(f) and not is_exchange_style_name(f)]
        if imap_names:
            print(f"  ❌ FAIL: Found IMAP-style names in Exchange tab: {imap_names}")
            all_pass = False
        else:
            print(f"  ✓ PASS: No IMAP-style names found")
        
        # Check that we have Exchange-style names
        exchange_names = [f for f in folders if is_exchange_style_name(f)]
        if exchange_names:
            print(f"  ✓ PASS: Found Exchange-style names: {exchange_names}")
        else:
            print(f"  ⚠️  WARNING: No Exchange-style names found (might be OK for custom folders)")
    
    return all_pass


def test_imap_tab_folder_names():
    """Test that IMAP tab uses IMAP-style folder names."""
    print("\n\nTesting IMAP Tab Folder Names...")
    print("=" * 60)
    
    imap_tab_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "gui", "tab_imap_search.py"
    )
    
    fallback_lists = extract_fallback_folders(imap_tab_file)
    
    if not fallback_lists:
        print("❌ FAIL: Could not find fallback_folders in IMAP tab")
        return False
    
    print(f"Found {len(fallback_lists)} fallback folder list(s) in IMAP tab:")
    
    all_pass = True
    for i, folders in enumerate(fallback_lists, 1):
        print(f"\nList {i}: {folders}")
        
        # Check that we have IMAP-style names
        imap_names = [f for f in folders if is_imap_style_name(f)]
        if imap_names:
            print(f"  ✓ PASS: Found IMAP-style names: {imap_names}")
        else:
            print(f"  ⚠️  WARNING: No IMAP-style names found")
    
    return all_pass


def test_no_mixed_styles():
    """Test that Exchange tab doesn't mix Exchange and IMAP styles."""
    print("\n\nTesting for Mixed Styles...")
    print("=" * 60)
    
    exchange_tab_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "gui", "tab_exchange_search.py"
    )
    
    fallback_lists = extract_fallback_folders(exchange_tab_file)
    
    all_pass = True
    for i, folders in enumerate(fallback_lists, 1):
        exchange_count = sum(1 for f in folders if is_exchange_style_name(f))
        imap_count = sum(1 for f in folders if is_imap_style_name(f) and not is_exchange_style_name(f))
        
        if exchange_count > 0 and imap_count > 0:
            print(f"  ❌ FAIL: List {i} mixes Exchange ({exchange_count}) and IMAP ({imap_count}) styles")
            all_pass = False
        else:
            print(f"  ✓ PASS: List {i} is consistent (Exchange: {exchange_count}, IMAP: {imap_count})")
    
    return all_pass


def main():
    """Run all tests."""
    print("=" * 60)
    print("Exchange vs IMAP Folder Name Test Suite")
    print("=" * 60)
    print()
    
    test1 = test_exchange_tab_folder_names()
    test2 = test_imap_tab_folder_names()
    test3 = test_no_mixed_styles()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Exchange Tab Names Test: {'✓ PASS' if test1 else '❌ FAIL'}")
    print(f"IMAP Tab Names Test:     {'✓ PASS' if test2 else '❌ FAIL'}")
    print(f"No Mixed Styles Test:    {'✓ PASS' if test3 else '❌ FAIL'}")
    print("=" * 60)
    
    if test1 and test3:  # test2 is informational only
        print("\n✅ ALL CRITICAL TESTS PASSED")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
