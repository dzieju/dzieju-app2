# Quick Start: Thunderbird Folder Filtering

## What Changed? 🎯

The application now filters folders like Thunderbird does - showing only mail-related folders and hiding technical folders (Calendar, Contacts, Tasks, etc.).

## Before vs After

### ❌ Before
```
18 folders shown (including Calendar, Contacts, Tasks, Notes, Journal, Conversation History)
↓
Cluttered, confusing view
```

### ✅ After  
```
12 folders shown (only mail folders)
↓
Clean, Thunderbird-like view
```

## What's Hidden Now?

### Exchange Accounts
- 📅 Calendar
- 👥 Contacts
- ✓ Tasks
- 📓 Notes
- 📔 Journal
- 💬 Conversation History
- ⚙️ Sync Issues (and subfolders)

### IMAP Accounts
- Folders with `\Noselect` flag
- Calendar, Contacts, Notes, Tasks, Journal

## What's Still Visible?

✅ **All mail folders:**
- 📥 Inbox (Odebrane)
- 📤 Sent Items (Wysłane)
- 📝 Drafts (Szkice)
- 🗑️ Deleted Items (Kosz)
- ⚠️ Junk Email (Spam)
- 📮 Outbox
- 📦 Archive (Archiwum)
- 📁 All your custom folders

## How to Verify It Works

1. **Open the application**
2. **Go to folder view** (Exchange or IMAP tab)
3. **Click "Odśwież foldery" (Refresh folders)**
4. **Check the status line:**
   - Should show fewer folders (e.g., "Znaleziono 12 folderów" instead of 18)
5. **Verify technical folders are hidden:**
   - Calendar ❌
   - Contacts ❌
   - Tasks ❌
   - etc.

## Troubleshooting

### "I need to see technical folders"

Currently, technical folders are always hidden. Future enhancement planned to add a checkbox "Show all folders" for advanced users.

### "My custom folder is hidden"

If your custom folder name contains words like "Calendar", "Contacts", "Tasks", "Notes", or "Journal", it will be filtered. This is intentional to match Thunderbird's behavior.

**Workaround:** Rename the folder to not include these keywords.

### "Check the logs"

Look for messages like:
```
[MAIL CONNECTION] Skipping non-mail folder: Calendar (class: IPF.Appointment)
[MAIL CONNECTION] Skipping technical folder: Conversation History
```

This confirms filtering is working.

## Testing

### Run Tests
```bash
# Test filtering logic
python -m unittest tests.test_folder_filtering -v

# Test folder detection
python -m unittest tests.test_folder_detection_logic -v
```

### Expected Results
```
✅ 6 filtering tests passing
✅ 21 detection tests passing
```

## Benefits

### User Experience
- 📉 **33% fewer folders** to scroll through
- 🎯 **Only relevant folders** shown
- ✅ **Less confusion** about technical folders
- 🚀 **Faster navigation**

### Performance
- ⚡ **Faster loading** - fewer folders to process
- 💾 **Less memory** - smaller folder tree
- 🔄 **Quicker refresh** - skip technical folders

### Compatibility
- 🔧 **Thunderbird-like** - familiar behavior
- 📧 **Standards-based** - RFC 6154, Exchange folder classes
- 🌍 **Multi-language** - Polish and English

## Technical Details

### Exchange Filtering

**By Folder Class:**
```python
EXCLUDED_FOLDER_CLASSES = [
    'IPF.Appointment',   # Calendar
    'IPF.Contact',       # Contacts
    'IPF.Task',          # Tasks
    'IPF.StickyNote',    # Notes
    'IPF.Journal',       # Journal
]
```

**By Folder Name:**
```python
EXCLUDED_FOLDER_NAMES = [
    'Conversation History',
    'Sync Issues',
    'Conflicts',
    'Local Failures',
    'Server Failures',
]
```

### IMAP Filtering

**By Flag:**
- Skip folders with `\Noselect` flag

**By Pattern:**
```python
EXCLUDED_FOLDER_PATTERNS = [
    'Calendar',
    'Contacts',
    'Notes',
    'Tasks',
    'Journal',
]
```

## Documentation

### Full Guides
- 📖 `THUNDERBIRD_FOLDER_FILTERING.md` - Complete implementation guide
- 📊 `THUNDERBIRD_FILTERING_VISUAL_COMPARISON.md` - Before/After comparison
- 📝 `PR_SUMMARY_THUNDERBIRD_FILTERING.md` - PR summary and impact analysis

### Quick Reference
This file! Pin it for easy access.

## FAQ

### Q: Can I see technical folders if I need them?
**A:** Not yet. Future enhancement planned to add "Show all folders" checkbox.

### Q: Will this affect my email search?
**A:** No. Hidden folders can still be searched if explicitly specified.

### Q: Is this safe?
**A:** Yes. Filtering only affects display, not data. Technical folders are hidden, not deleted.

### Q: Can I customize what's filtered?
**A:** Not yet. Future enhancement planned for user-configurable exclusion lists.

### Q: Does this work with all account types?
**A:** Yes. Exchange ✅ | IMAP ✅ | POP3 ✅ (POP3 only has INBOX, so not affected)

### Q: What if I have a folder named "Calendar" with mail?
**A:** It will be filtered. Workaround: Rename to avoid keyword conflicts.

---

## Need Help?

1. **Check logs** for filtering messages
2. **Run tests** to verify functionality
3. **Read full documentation** for details
4. **Report issues** if something doesn't work as expected

---

**Version:** 2025-10-10  
**Status:** ✅ Production Ready  
**Compatibility:** Exchange, IMAP, POP3
