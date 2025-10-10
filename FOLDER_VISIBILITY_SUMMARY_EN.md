# Folder Visibility Summary (English)

## Quick Reference

This document provides a concise English summary of the comprehensive Polish documentation `OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md`.

---

## Key Findings

### Exchange Mail Tab

**What IS displayed:**
- ✅ All system folders (Inbox, Sent Items, Drafts, Deleted Items, Junk Email, Outbox, Archive)
- ✅ All user-created folders (at all hierarchy levels)
- ✅ All subfolders (recursive)
- ⚠️ Technical folders (Calendar, Contacts, Tasks, Notes, Journal, Conversation History)

**Detection mechanism:**
- Starts from `account.root` (Top of Information Store)
- Depth-first recursive traversal
- Well-known folder fallback
- Full hierarchy preserved

### IMAP Mail Tab

**What IS displayed:**
- ✅ All system folders (INBOX, SENT, DRAFTS, TRASH, SPAM, ARCHIVE)
- ✅ All user-created folders (at all hierarchy levels)
- ✅ All subfolders (recursive)
- ✅ RFC 6154 SPECIAL-USE flag detection

**Detection mechanism:**
- IMAP LIST command
- Server-dependent delimiter (`.` or `/`)
- Automatic hierarchy parsing
- Multi-server support (Gmail, Dovecot, Exchange IMAP)

---

## Problem Identified

**Issue:** "Program displays too many folders on mail accounts"

**Root cause:** Exchange technical folders are visible
- Calendar (IPF.Appointment)
- Contacts (IPF.Contact)
- Tasks (IPF.Task)
- Notes (IPF.Note)
- Journal (IPF.Journal)
- Conversation History

**Why it's a problem:** These folders **do not contain email messages**, they contain other Exchange object types (calendar events, contacts, tasks, etc.).

---

## Answers to Issue Questions

| Question | Answer |
|----------|--------|
| **Are system folders displayed?** | ✅ YES - All standard system folders are shown |
| **Are hidden/system folders that shouldn't be visible displayed?** | ⚠️ PARTIALLY - Exchange technical folders are shown (Calendar, Contacts, Tasks) |
| **Are user folders displayed?** | ✅ YES - All user-created folders at all levels |
| **Are technical/archive folders displayed?** | ✅ YES - Archive folders are shown as system folders |
| **Are subfolders displayed?** | ✅ YES - Full recursive hierarchy |
| **Is folder hierarchy readable?** | ✅ YES - Tree structure with indentation, icons, and logical sorting |

---

## Recommendations

### High Priority
1. **Filter Exchange technical folders by `folder_class`**
   - Only show folders with mail content (`IPF.Note`)
   - Hide Calendar, Contacts, Tasks, Journal, Notes

2. **Add GUI checkbox: "Show only mail folders"**
   - Default: checked (hides technical folders)
   - Unchecked: shows everything for advanced users

### Medium Priority
3. **Default exclusion list**
   - "Conversation History", "Sync Issues"
   - Configurable in settings

4. **Folder count display in GUI**
   - "Showing X of Y folders (Z hidden)"

### Low Priority
5. **Tooltips with additional info**
   - Explanations for system folders
   - Warnings for technical folders

---

## Code References

**Exchange folder detection:**
- File: `gui/exchange_search_components/mail_connection.py`
- Methods:
  - `_get_exchange_available_folders()` (lines 763-856)
  - `_get_exchange_folders_with_details()` (lines 298-387)
  - `_get_all_subfolders_recursive()` (lines 661-684)

**IMAP folder detection:**
- File: `gui/exchange_search_components/mail_connection.py`
- Methods:
  - `_get_imap_available_folders()` (lines 857-927)

**Folder display components:**
- Exchange: `gui/exchange_search_components/folder_browser.py`
- IMAP: `gui/imap_search_components/folder_browser.py`
- Class: `FolderInfo` with special folder detection

---

## Current Status

✅ **Documentation complete**
✅ **Problem identified**: Exchange technical folders are unnecessarily visible
✅ **Solution proposed**: Filter by `folder_class` to show only mail folders
✅ **All issue questions answered**

The current implementation correctly displays:
- All system mail folders
- All user-created folders
- Complete folder hierarchy

The only improvement needed is filtering out Exchange non-mail folders (Calendar, Contacts, Tasks, etc.) to reduce visual clutter and improve user experience.

---

**Document created**: 2025-10-09  
**Related Polish document**: `OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md`  
**Status**: ✅ Analysis complete
