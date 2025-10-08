# Manual Testing Guide - Folder Detection Verification

This guide describes how to manually test the folder detection improvements to ensure they work correctly with real mail accounts.

## What Was Fixed

### Critical Bug: Exchange Folder Browser
- **Problem:** Exchange folder browser was calling IMAP methods instead of Exchange methods
- **Fix:** Updated to use `get_exchange_account()` and added Exchange-specific folder retrieval
- **Impact:** Exchange folders can now be displayed and browsed correctly

### Verified Working: IMAP Folder Detection
- **Status:** Already working correctly
- **Features:** Polish names, SPECIAL-USE flags, hierarchical structure
- **Tested:** 21 unit tests all passing

## Testing Checklist

### 1. Exchange Folder Browser Testing

**Prerequisites:**
- Exchange account configured in `exchange_mail_config.json`
- Application running

**Steps:**
1. Open application
2. Navigate to "Poczta Exchange" tab
3. Click "🔄 Odśwież foldery" button

**Expected Results:**
✅ Account name and email displayed in header  
✅ Folder list appears with correct structure:
```
📥 Odebrane                     [count]    [size]
📤 Wysłane                      [count]    [size]
📝 Szkice                       [count]    [size]
🗑️ Kosz                         [count]    [size]
📁 [Custom folders...]          [count]    [size]
```
✅ Message counts are accurate  
✅ Size estimates are reasonable  
✅ Hierarchical folders are properly nested  
✅ Double-click on folder shows detailed information  

**Before Fix (Would Fail):**
❌ Error: "Brak konta IMAP/POP3 - skonfiguruj konto..."  
❌ Folders would not load  

**After Fix:**
✅ Folders load successfully  
✅ Error message would be: "Brak konta Exchange..." (if no account)  

### 2. IMAP Folder Browser Testing - Polish Account

**Test Case:** Polish email provider (woox.pl, onet.pl, interia.pl)

**Prerequisites:**
- IMAP account configured with Polish folder names
- Account with folders named: Odebrane, Wysłane, Szkice, Kosz

**Steps:**
1. Open application
2. Navigate to "Poczta IMAP" tab
3. Click "🔄 Odśwież foldery" button

**Expected Results:**
✅ Polish folder names are correctly detected:
- "Odebrane" → Shows as "📥 Odebrane" (recognized as Inbox)
- "Wysłane" or "Wyslane" → Shows as "📤 Wysłane" (recognized as Sent)
- "Szkice" → Shows as "📝 Szkice" (recognized as Drafts)
- "Kosz" → Shows as "🗑️ Kosz" (recognized as Trash)
- "Archiwum" → Shows as "📦 Archiwum" (recognized as Archive)

✅ System folders appear at top, before custom folders  
✅ Correct icons for each folder type  

### 3. IMAP Folder Browser Testing - International Account

**Test Case:** Gmail, Outlook.com, or other international provider

**Prerequisites:**
- IMAP account with English folder names

**Steps:**
1. Configure account
2. Navigate to "Poczta IMAP" tab
3. Click "🔄 Odśwież foldery"

**Expected Results:**
✅ English folder names are correctly detected:
- "INBOX" → Shows as "📥 Odebrane"
- "Sent" or "Sent Items" → Shows as "📤 Wysłane"
- "Drafts" → Shows as "📝 Szkice"
- "Trash" or "Deleted Items" → Shows as "🗑️ Kosz"
- "Spam" or "Junk" → Shows as "⚠️ Spam"
- "Archive" → Shows as "📦 Archiwum"

✅ SPECIAL-USE flags are honored (if provided by server)  

### 4. Hierarchical Folder Structure Testing

**Test Case:** Nested folder structure

**Prerequisites:**
- Account with nested folders (e.g., Projects/2024/Q1, Archive/2023)

**Expected Results:**
✅ Folders are displayed in tree hierarchy:
```
📁 Projects
  📁 2024
    📁 Q1
    📁 Q2
  📁 2025
📁 Archive
  📁 2023
  📁 2024
```
✅ Expand/collapse works correctly  
✅ Parent-child relationships are correct  
✅ Message counts shown for each folder  

### 5. Hierarchical Path Detection Testing

**Test Case:** Folders with email prefix (e.g., recepcja@woox.pl/Odebrane)

**Expected Results:**
✅ Folder "recepcja@woox.pl/Odebrane" is recognized as Inbox  
✅ Shows as "📥 Odebrane" (not generic 📁)  
✅ Basename detection works: "path/to/Odebrane" → detected as Inbox  

### 6. Size Estimation Verification

**Test Case:** Check if size estimates are reasonable

**Expected Results:**
✅ Empty folders show "0 B"  
✅ Small folders (<1MB) show in KB  
✅ Medium folders (1-1000 MB) show in MB  
✅ Large folders (>1 GB) show in GB  
✅ Estimate approximately: message_count × 150 KB  

**Example:**
- 100 messages → ~15 MB
- 1,000 messages → ~150 MB
- 10,000 messages → ~1.5 GB

### 7. Double-Click Information Dialog

**Steps:**
1. Double-click on any folder in the tree

**Expected Results:**
✅ Information dialog appears with:
- Folder name (Polish for system folders)
- Full path
- Message count
- Estimated size
- Type (Systemowy/Własny)

## Screenshots to Take

### Exchange Folder Browser
1. **Before fix:** Error message (if possible to recreate)
2. **After fix:** Successful folder list with Exchange account

### IMAP Folder Browser - Polish Account
1. Folder list showing Polish names correctly detected
2. Double-click information dialog for "Odebrane" folder

### IMAP Folder Browser - International Account
1. Folder list showing English names with Polish display
2. Hierarchical folder structure expanded

### Hierarchical Structure
1. Before expanding nested folders
2. After expanding nested folders showing tree structure

## Performance Testing

### Large Mailbox Test

**Test Case:** Account with many folders and messages

**Expected Results:**
✅ Folder discovery completes within reasonable time (< 30 seconds)  
✅ UI remains responsive during loading  
✅ Progress indicator shows "Pobieranie listy folderów..."  
✅ No timeout errors  

### Multiple Accounts Test

**Test Case:** Switch between different accounts

**Expected Results:**
✅ Folder list updates correctly for each account  
✅ No data from previous account shown  
✅ Account label shows current account name  

## Error Handling Testing

### No Account Configured

**Steps:**
1. Remove all accounts from config
2. Try to refresh folders

**Expected Results (Exchange):**
✅ Error: "Brak konta Exchange - skonfiguruj konto w zakładce 'Konfiguracja poczty'"  
✅ No crash  

**Expected Results (IMAP):**
✅ Error: "Brak konta IMAP/POP3 - skonfiguruj konto w zakładce 'Konfiguracja poczty'"  
✅ No crash  

### Network Error

**Steps:**
1. Disconnect from network
2. Try to refresh folders

**Expected Results:**
✅ Error message about connection failure  
✅ No crash  
✅ Refresh button becomes enabled again  

### Invalid Credentials

**Steps:**
1. Configure account with wrong password
2. Try to refresh folders

**Expected Results:**
✅ Authentication error message  
✅ No crash  
✅ Refresh button becomes enabled again  

## Regression Testing

### Existing Functionality Still Works

**Test Cases:**
1. ✅ Mail search still works
2. ✅ Folder exclusion still works
3. ✅ Email viewing still works
4. ✅ All other tabs function normally

## Reporting Issues

If you find any issues during testing, please report:

1. **Issue Type:** Bug / Enhancement / Question
2. **Component:** Exchange Folder Browser / IMAP Folder Browser
3. **Account Type:** Exchange / IMAP (Gmail/Outlook/Polish provider)
4. **Steps to Reproduce:**
   - Step 1
   - Step 2
   - Step 3
5. **Expected Behavior:** What should happen
6. **Actual Behavior:** What actually happened
7. **Screenshots:** If applicable
8. **Logs:** Check application logs for error messages

## Success Criteria

The folder detection verification is considered successful when:

✅ All manual test cases pass  
✅ Exchange folder browser loads folders correctly  
✅ IMAP folder browser detects Polish names correctly  
✅ IMAP folder browser detects English names correctly  
✅ Hierarchical structure displays correctly  
✅ Size estimates are reasonable  
✅ No crashes or errors with valid accounts  
✅ Error handling works for invalid accounts  
✅ Performance is acceptable for large mailboxes  

## Additional Notes

### Unit Tests
All 21 unit tests are passing:
```bash
cd /home/runner/work/dzieju-app2/dzieju-app2
python3 tests/test_folder_detection_logic.py
```

**Result:** All 21 tests passing ✓

### Code Changes Summary
- Fixed: `gui/exchange_search_components/folder_browser.py`
- Fixed: `gui/exchange_search_components/mail_connection.py`
- Verified: `gui/imap_search_components/folder_browser.py`
- Verified: `gui/mail_search_components/folder_browser.py`
- Added: Unit tests for folder detection logic

### Documentation
- `FOLDER_DETECTION_VERIFICATION_2025.md` - Technical analysis and verification
- `MANUAL_TESTING_GUIDE.md` - This document
