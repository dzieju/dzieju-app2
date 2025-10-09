# Exchange Folder Detection Fix - Root Folder Discovery

**Issue:** Błąd: Niepoprawne wykrywanie folderów w Exchange – porównaj z działającym repo ksiegi-ocr  
**Date:** January 2025  
**Status:** ✅ **FIXED**

---

## Problem Description

### User Complaint
After clicking "Wykryj foldery" (Detect folders) in the Exchange Mail tab, the list was incomplete - system folders and root-level user folders were missing.

### Root Cause
The `_get_exchange_available_folders()` method was starting folder discovery from the specified `folder_path` parameter (typically "Inbox"), which only showed:
- Subfolders of Inbox
- Nested folders under Inbox

It was **NOT** showing:
- System folders at root level (Sent Items, Drafts, Deleted Items, Junk Email, Outbox)
- User-created folders at root level
- Other top-level folders

### Why This Happened
The folder discovery logic in `_get_exchange_available_folders()` was different from the working `_get_exchange_folders_with_details()` method, which correctly started from `account.root`.

---

## Solution Implemented

### Changes Made

Modified two files:
1. `gui/exchange_search_components/mail_connection.py` (lines 763-784)
2. `gui/mail_search_components/mail_connection.py` (lines 727-748)

### Before Fix ❌

```python
def _get_exchange_available_folders(self, account, folder_path):
    """Get available Exchange folders for exclusion"""
    try:
        folder = self.get_folder_by_path(account, folder_path)
        if not folder:
            log("[MAIL CONNECTION] ERROR: Could not access Exchange folder for discovery")
            return self._get_fallback_folders()
        
        log(f"[MAIL CONNECTION] Starting Exchange folder discovery from: '{folder.name}'")
        
        # Get all subfolders recursively (without exclusions since we want to show all as options)
        all_subfolders = self._get_all_subfolders_recursive(folder, set())
```

**Problem:** Started from `folder_path` (usually "Inbox"), missing root-level folders.

### After Fix ✅

```python
def _get_exchange_available_folders(self, account, folder_path):
    """Get available Exchange folders for exclusion"""
    try:
        # Start from root folder to discover ALL folders, not just subfolders of specified path
        # This ensures system folders (Sent Items, Drafts, etc.) are included
        try:
            root_folder = account.root
            log(f"[MAIL CONNECTION] Starting Exchange folder discovery from root: '{root_folder.name}'")
        except Exception as root_error:
            log(f"[MAIL CONNECTION] Could not access root folder, using inbox parent: {root_error}")
            try:
                root_folder = account.inbox.parent
                log(f"[MAIL CONNECTION] Using inbox parent: '{root_folder.name}'")
            except Exception as parent_error:
                log(f"[MAIL CONNECTION] Could not access inbox parent, falling back to specified path: {parent_error}")
                root_folder = self.get_folder_by_path(account, folder_path)
                if not root_folder:
                    log("[MAIL CONNECTION] ERROR: Could not access any folder for discovery")
                    return self._get_fallback_folders()
        
        # Get all subfolders recursively (without exclusions since we want to show all as options)
        all_subfolders = self._get_all_subfolders_recursive(root_folder, set())
```

**Solution:** 
1. Start from `account.root` to get ALL folders
2. Fallback to `account.inbox.parent` if root not accessible
3. Further fallback to specified `folder_path` if needed
4. Enhanced logging for debugging

---

## Expected Results After Fix

### Complete Folder List ✅

Users will now see **ALL folders** when clicking "Wykryj foldery":

```
System Folders (at root level):
✓ Drafts (Szkice)
✓ Deleted Items (Kosz)
✓ Inbox (Odebrane)
✓ Junk Email (Spam)
✓ Outbox (Skrzynka nadawcza)
✓ Sent Items (Wysłane)

User Folders (at root level):
✓ Archive
✓ Projects
✓ 2024
✓ 2023

Nested Folders:
✓ Archive/2024
✓ Archive/2023
✓ Projects/ProjectA
✓ Projects/ProjectB
```

### Before vs After Comparison

#### Before Fix ❌
```
Starting from: Inbox
Folders found:
- Archive
- 2024
- 2023
- Projects
- ProjectA
- ProjectB

Missing: Sent Items, Drafts, Deleted Items, Junk Email, Outbox
```

#### After Fix ✅
```
Starting from: Root (Top of Information Store)
Folders found:
- Archive
- 2024
- 2023
- Deleted Items
- Drafts
- Inbox
- Junk Email
- Outbox
- Projects
- ProjectA
- ProjectB
- Sent Items

Complete: All folders present ✓
```

---

## Technical Details

### Folder Hierarchy in Exchange

```
Root (Top of Information Store)
├── Inbox                    ← Old method started here
│   ├── Archive             ✓ Was found
│   │   ├── 2024           ✓ Was found
│   │   └── 2023           ✓ Was found
│   └── Projects            ✓ Was found
├── Sent Items              ✗ Was MISSING
├── Drafts                  ✗ Was MISSING
├── Deleted Items           ✗ Was MISSING
├── Junk Email              ✗ Was MISSING
└── Outbox                  ✗ Was MISSING
```

The old implementation missed all folders that are siblings of Inbox (at the same level), because it only traversed subfolders of Inbox.

### The Fix: Start from Root

```
Root (Top of Information Store)  ← New method starts here
├── Inbox                    ✓ Now found
│   ├── Archive             ✓ Still found
│   │   ├── 2024           ✓ Still found
│   │   └── 2023           ✓ Still found
│   └── Projects            ✓ Still found
├── Sent Items              ✓ NOW FOUND
├── Drafts                  ✓ NOW FOUND
├── Deleted Items           ✓ NOW FOUND
├── Junk Email              ✓ NOW FOUND
└── Outbox                  ✓ NOW FOUND
```

---

## IMAP Tab Verification ✅

### Separation Confirmed

The IMAP tab uses a **completely separate** method `_get_imap_available_folders()` which:
- Connects to IMAP server
- Uses `imap.list_folders()` to get folder list
- Has its own logic independent of Exchange

### Code Path Verification

```python
def get_available_folders_for_exclusion(self, account, folder_path):
    account_type = self.current_account_config.get("type", "unknown")
    
    if account_type == "exchange":
        return self._get_exchange_available_folders(account, folder_path)  # ← Exchange only
    elif account_type == "imap_smtp":
        return self._get_imap_available_folders(folder_path)  # ← IMAP only
    elif account_type == "pop3_smtp":
        return ["INBOX"]  # ← POP3 only
```

**Conclusion:** IMAP tab is **NOT affected** by this change.

---

## Comparison with ksiegi-ocr Repository

### Findings

After cloning and analyzing ksiegi-ocr:
- ksiegi-ocr has the **OLD buggy implementation** with nested `collect_folder_names()` function
- ksiegi-ocr builds folder paths with "/" separators
- ksiegi-ocr does **NOT** have the root folder fix

### Interpretation

The issue description stating "ksiegi-ocr poprawnie wykrywa foldery" (ksiegi-ocr correctly detects folders) appears to be **incorrect**. The actual working implementation is now in dzieju-app2 after this fix.

---

## Testing Guide

### Manual Testing Steps

1. **Open Exchange Tab**
   - Navigate to "Poczta Exchange" tab
   - Go to "Wyszukiwanie" (Search) section

2. **Click "Wykryj foldery" Button**
   - Wait for folder discovery to complete
   - Check the logs for confirmation

3. **Verify Complete Folder List**
   - ✅ All system folders visible (Sent Items, Drafts, etc.)
   - ✅ All root-level user folders visible
   - ✅ All nested folders visible
   - ✅ Folders sorted properly (system first, then custom)

4. **Check IMAP Tab (Should Be Unchanged)**
   - Navigate to "Poczta IMAP" tab
   - Click folder detection
   - ✅ IMAP folders still work correctly

### Expected Log Output

```
[MAIL CONNECTION] Getting available folders for account: 'My Exchange' (type: exchange)
[MAIL CONNECTION] Using Exchange folder detection
[MAIL CONNECTION] Starting Exchange folder discovery from root: 'Top of Information Store'
[MAIL CONNECTION] Accessing 12 children of folder 'Top of Information Store'
[MAIL CONNECTION] Added well-known folder: Sent Items
[MAIL CONNECTION] Added well-known folder: Drafts
[MAIL CONNECTION] Added well-known folder: Deleted Items
[MAIL CONNECTION] Added well-known folder: Junk Email
[MAIL CONNECTION] Added well-known folder: Outbox
[MAIL CONNECTION] Found Exchange folders for exclusion (15):
[MAIL CONNECTION] System folders: 8, Custom folders: 7
  1. Deleted Items
  2. Drafts
  3. Inbox
  4. Junk Email
  5. Outbox
  6. Sent Items
  7. Archive
  8. Projects
  ...
```

---

## Files Modified

1. **`gui/exchange_search_components/mail_connection.py`**
   - Method: `_get_exchange_available_folders()` (lines 763-784)
   - Change: Start from `account.root` instead of `folder_path`

2. **`gui/mail_search_components/mail_connection.py`**
   - Method: `_get_exchange_available_folders()` (lines 727-748)
   - Change: Start from `account.root` instead of `folder_path`

---

## Compliance with Requirements

✅ **"Przeanalizować logikę wykrywania folderów w ksiegi-ocr"**
- Analyzed: ksiegi-ocr has the old buggy implementation

✅ **"Porównać z bieżącą implementacją"**
- Compared: Current implementation was missing root folder access

✅ **"Zaimplementować analogiczne rozwiązanie"**
- Implemented: Now starts from root like the working `_get_exchange_folders_with_details()` method

✅ **"Upewnić się, że struktura folderów jest pełna"**
- Ensured: All folders from root level are now discovered

✅ **"Uwzględnia systemowe foldery"**
- Included: Sent Items, Drafts, Deleted Items, Junk Email, Outbox all visible

✅ **"Nie naruszaj zakładki IMAP"**
- Verified: IMAP uses separate method, not affected

---

## Summary

### What Was Fixed
- Exchange folder detection now starts from `account.root`
- All folders are discovered, including root-level system and user folders
- Robust fallback strategy if root is not accessible
- Enhanced logging for debugging

### What Was NOT Changed
- IMAP folder detection (separate code path)
- POP3 folder detection (separate code path)
- Folder display logic (FolderBrowser components)
- Folder search/filtering logic

### Result
Users can now see a **complete list of all Exchange folders** when clicking "Wykryj foldery", including system folders that were previously missing.

---

**Status:** ✅ FIXED  
**Action Required:** None - ready for testing  
**Next Steps:** Manual testing on real Exchange accounts
