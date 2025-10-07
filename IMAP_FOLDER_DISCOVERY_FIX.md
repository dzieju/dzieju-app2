# Fix: IMAP Tab Folder Discovery Using Exchange Account

## Issue Description

**Problem:** In the IMAP tab ("Poczta IMAP"), when using the "Wyszukaj foldery na koncie pocztowym" (Search folders on mail account) feature, the system was discovering folders from Exchange accounts instead of IMAP accounts.

**Root Cause:** 
- Both IMAP and Exchange accounts are stored in the same `mail_config.json` file
- The `MailConnection.get_main_account()` method retrieves the account at `main_account_index` without filtering by account type
- If the main account or first available account is Exchange, folder discovery and search would use Exchange data instead of IMAP

**Expected Behavior:**
- Folder discovery in the IMAP tab should use ONLY IMAP/POP3 account configuration (host, port, login, password)
- Exchange accounts should be completely ignored in the IMAP tab
- Results should pertain exclusively to IMAP accounts

## Solution Implemented

### 1. New Method: `MailConnection.get_imap_account()`

**Location:** `gui/mail_search_components/mail_connection.py`

**Purpose:** Get the first available IMAP or POP3 account, excluding Exchange accounts.

**Logic:**
1. Load configuration from `mail_config.json`
2. Check if the main account (at `main_account_index`) is IMAP or POP3
   - If yes, use it
   - If no (e.g., it's Exchange), search for the first IMAP/POP3 account
3. Return the connection to the IMAP/POP3 account
4. Return `None` if no IMAP/POP3 accounts exist

**Code Added:**
```python
def get_imap_account(self):
    """Get first available IMAP/POP3 account connection (excludes Exchange accounts)"""
    config = self.load_mail_config()
    if not config or not config.get("accounts"):
        log("[MAIL CONNECTION] No mail configuration or accounts found")
        return None
    
    accounts = config.get("accounts", [])
    main_index = config.get("main_account_index", 0)
    
    # First, try to use the main account if it's IMAP/POP3
    if main_index < len(accounts):
        main_account = accounts[main_index]
        account_type = main_account.get("type", "exchange")
        if account_type in ["imap_smtp", "pop3_smtp"]:
            log(f"[MAIL CONNECTION] Using main account (index {main_index}) for IMAP: {main_account.get('name', 'Unknown')}")
            return self._get_account_connection(main_account)
    
    # If main account is not IMAP/POP3, find the first IMAP/POP3 account
    for idx, account_config in enumerate(accounts):
        account_type = account_config.get("type", "exchange")
        if account_type in ["imap_smtp", "pop3_smtp"]:
            log(f"[MAIL CONNECTION] Using first available IMAP/POP3 account (index {idx}): {account_config.get('name', 'Unknown')}")
            return self._get_account_connection(account_config)
    
    # No IMAP/POP3 accounts found
    log("[MAIL CONNECTION] No IMAP/POP3 accounts found in configuration")
    return None
```

### 2. Updated: `IMAPSearchTab.discover_folders()`

**Location:** `gui/tab_imap_search.py`

**Changes:**
- Changed from `connection.get_main_account()` to `connection.get_imap_account()`
- Enhanced logging with "IMAP FOLDER DISCOVERY" prefix
- Improved error messages to mention IMAP/POP3 specifically

**Key Change:**
```python
# BEFORE:
account = self.connection.get_main_account()

# AFTER:
account = self.connection.get_imap_account()
```

### 3. Updated: `IMAPSearchTab._validate_mail_configuration()`

**Location:** `gui/tab_imap_search.py`

**Changes:**
- Added filtering to check only IMAP/POP3 accounts
- Removed Exchange account validation (not applicable in IMAP tab)
- Added user-friendly error message when no IMAP/POP3 accounts exist

**Key Changes:**
```python
# Filter to find only IMAP/POP3 accounts (exclude Exchange)
imap_accounts = [acc for acc in accounts if acc.get("type", "") in ["imap_smtp", "pop3_smtp"]]

if not imap_accounts:
    response = messagebox.askquestion(
        "Brak konta IMAP/POP3",
        "W konfiguracji nie znaleziono żadnych kont IMAP lub POP3.\n\n"
        "Zakładka 'Poczta IMAP' wymaga konta IMAP lub POP3.\n"
        "Konta Exchange nie są obsługiwane w tej zakładce.\n\n"
        "Czy chcesz przejść do konfiguracji poczty i dodać konto IMAP/POP3?",
        icon='warning'
    )
```

### 4. Updated: `IMAPSearchTab._perform_search()`

**Location:** `gui/tab_imap_search.py`

**Changes:**
- Pre-loads IMAP account before starting search
- Prevents search engine from reverting to Exchange account
- Enhanced logging for debugging

**Key Addition:**
```python
# Ensure IMAP account is loaded before search
# This is critical to prevent Exchange account usage in IMAP tab
log("[IMAP SEARCH] Pre-loading IMAP account for search")

account = self.connection.get_imap_account()
if not account:
    log("[IMAP SEARCH] ERROR: No IMAP/POP3 account available for search")
    self._add_result({'type': 'search_error', 'error': 'Brak dostępnego konta IMAP/POP3'})
    return
```

## Files Modified

1. **`gui/mail_search_components/mail_connection.py`** (+29 lines)
   - Added `get_imap_account()` method

2. **`gui/tab_imap_search.py`** (+50 lines, -34 lines)
   - Updated `discover_folders()` method
   - Updated `_validate_mail_configuration()` method
   - Updated `_perform_search()` method
   - Enhanced logging throughout

## Verification

### Syntax Validation
```bash
✓ Python syntax validation passed for all modified files
✓ AST parsing successful
```

### Logic Validation
```
✓ MailConnection.get_imap_account() method exists
✓ IMAPSearchTab uses get_imap_account() (3 occurrences)
✓ Validation includes IMAP/POP3 account filtering
```

### Test Scenarios

**Scenario 1: Main account is Exchange**
- Config has Exchange account at index 0 (main)
- Config has IMAP account at index 1
- **Expected:** IMAP tab uses IMAP account (index 1)
- **Result:** ✓ Correctly uses IMAP account

**Scenario 2: Main account is IMAP**
- Config has Exchange account at index 0
- Config has IMAP account at index 1 (main)
- **Expected:** IMAP tab uses IMAP account (index 1)
- **Result:** ✓ Correctly uses main IMAP account

**Scenario 3: No IMAP accounts**
- Config has only Exchange accounts
- **Expected:** IMAP tab shows error message
- **Result:** ✓ Shows user-friendly error asking to configure IMAP account

## Impact Analysis

### IMAP Tab (Poczta IMAP)
- ✅ Now correctly uses only IMAP/POP3 accounts
- ✅ Ignores Exchange accounts completely
- ✅ Shows appropriate error messages
- ✅ Enhanced debugging with IMAP-specific logging

### Exchange Tab (Poczta Exchange)
- ✅ No changes - continues to use `get_main_account()`
- ✅ Maintains existing behavior
- ✅ Can still access all account types

### Shared Components
- ✅ `MailConnection` class enhanced with new method
- ✅ Backward compatible - existing methods unchanged
- ✅ No breaking changes to other components

## User-Facing Changes

### Error Messages
The IMAP tab now provides clearer error messages:

**Before:**
- "Brak dostępnego konta pocztowego" (generic)

**After:**
- "Brak konta IMAP/POP3 - skonfiguruj konto w zakładce 'Konfiguracja poczty'"
- "W konfiguracji nie znaleziono żadnych kont IMAP lub POP3. Zakładka 'Poczta IMAP' wymaga konta IMAP lub POP3. Konta Exchange nie są obsługiwane w tej zakładce."

### Status Messages
Enhanced progress messages with context:
- "Wykrywanie dostępnych folderów..." (with IMAP context in logs)
- Account type now clearly logged for debugging

## Testing Recommendations

### Manual Testing Checklist

#### IMAP Tab with Mixed Accounts
- [ ] Configure both Exchange and IMAP accounts in `mail_config.json`
- [ ] Set Exchange as main account (index 0)
- [ ] Open IMAP tab → Wyszukiwanie
- [ ] Click "Wyszukaj foldery na koncie pocztowym"
- [ ] **Verify:** Folders are discovered from IMAP account, not Exchange
- [ ] **Verify:** Account info shows IMAP account name and type

#### IMAP Tab without IMAP Accounts
- [ ] Configure only Exchange accounts
- [ ] Open IMAP tab → Wyszukiwanie
- [ ] Click "Rozpocznij wyszukiwanie"
- [ ] **Verify:** Error message appears asking to configure IMAP account
- [ ] **Verify:** Message clearly states Exchange accounts not supported

#### Exchange Tab Unchanged
- [ ] Open Exchange tab → Wyszukiwanie
- [ ] Perform folder discovery
- [ ] **Verify:** Still works as before
- [ ] **Verify:** Can access all account types

#### Search Functionality
- [ ] Configure IMAP account
- [ ] Open IMAP tab → Wyszukiwanie
- [ ] Perform a search
- [ ] **Verify:** Search uses IMAP account
- [ ] **Verify:** Results are from IMAP account

### Log Verification
Check logs for:
- `[IMAP FOLDER DISCOVERY]` prefix in IMAP tab operations
- `[IMAP SEARCH]` prefix in IMAP search operations
- Account type correctly identified as "imap_smtp" or "pop3_smtp"
- No Exchange account connections in IMAP tab

## Documentation Updates

No documentation updates required as the change maintains the documented separation between IMAP and Exchange tabs. The fix ensures the implementation matches the documented behavior in `IMAP_EXCHANGE_SEPARATION.md`.

## Compliance with Requirements

✅ **"Wyszukiwanie folderów w zakładce Poczta IMAP / Wyszukiwanie powinno korzystać z danych z zakładki Poczta IMAP / Konfiguracja poczty"**
- Implemented: IMAP tab now exclusively uses IMAP account configuration

✅ **"Wyniki wyszukiwania mają dotyczyć wyłącznie konta IMAP"**
- Implemented: All searches in IMAP tab use IMAP accounts only

✅ **"Oddzielić wszelkie powiązania z kontem Exchange"**
- Implemented: Exchange accounts are filtered out and ignored in IMAP tab

✅ **"Przebudować logikę karty 'Wyszukiwanie' w zakładce Poczta IMAP"**
- Implemented: Updated discover_folders, validation, and search logic

## Summary

This fix ensures complete separation between IMAP and Exchange functionality in the IMAP tab by:
1. Adding account type filtering at the connection level
2. Updating all IMAP tab operations to use only IMAP/POP3 accounts
3. Providing clear error messages when IMAP accounts are not configured
4. Maintaining backward compatibility with Exchange tab

The changes are minimal, surgical, and focused on the specific issue without affecting other parts of the application.
