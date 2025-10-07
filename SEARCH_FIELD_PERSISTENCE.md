# Search Field Persistence Implementation

## Overview

This document describes the implementation of search field persistence in the Exchange mail search tab. This feature ensures that all search criteria entered by the user are automatically saved and restored when the application is closed and reopened.

## Problem Statement

Previously, after closing the application, users had to re-enter all search criteria in the Exchange mail tab, including:
- Sender email addresses
- Subject keywords
- Body search text
- PDF search text
- Attachment filters
- Date period selections
- Checkbox options (unread only, attachments required, etc.)

This was time-consuming and reduced productivity, especially for users who frequently search for similar emails.

## Solution

The implementation extends the existing configuration save/load system to include all search field values. The configuration is:
- **Automatically saved** when the application closes (no popup messages)
- **Automatically loaded** when the application starts
- **Manually saveable** via the existing "Zapisz ustawienia" button (shows confirmation message)

## Implementation Details

### Files Modified

- `gui/tab_mail_search.py` - Extended save/load configuration methods

### Changes Made

#### 1. Extended `save_mail_search_config()` Method

**New parameter:**
- `show_message` (bool, default=True): Controls whether to show popup messages

**New fields saved:**
- `folder_path` - Selected mail folder path
- `subject_search` - Subject search keywords
- `body_search` - Body search text
- `pdf_search_text` - Text to search within PDFs
- `sender` - Sender email filter
- `unread_only` - Unread messages only checkbox
- `attachments_required` - Attachments required checkbox
- `no_attachments_only` - No attachments only checkbox
- `attachment_name` - Attachment name filter
- `attachment_extension` - Attachment extension filter
- `selected_period` - Selected date period

**Previous fields (unchanged):**
- `excluded_folders` - List of excluded folders
- `exclusion_section_visible` - Visibility state of folder exclusion section
- `pdf_save_directory` - PDF save directory path
- `skip_searched_pdfs` - Skip already searched PDFs checkbox

#### 2. Extended `load_mail_search_config()` Method

Loads all the above fields from the configuration file. The implementation:
- Checks if each field exists before loading (backward compatibility)
- Uses conditional loading for string values (only sets if not empty)
- Uses existence check for boolean values (explicit check in config)
- Maintains default values if fields are missing

#### 3. Modified `destroy()` Method

The tab's `destroy()` method now:
1. Cancels any running search threads (existing behavior)
2. **Automatically saves configuration** with `show_message=False` (new)
3. Calls parent's destroy method (existing behavior)

## Configuration File

### File Location
`mail_search_config.json` in the application root directory

### File Format
```json
{
  "excluded_folders": ["Trash", "Spam"],
  "exclusion_section_visible": true,
  "pdf_save_directory": "/path/to/pdfs",
  "skip_searched_pdfs": false,
  "folder_path": "Skrzynka odbiorcza",
  "subject_search": "faktura",
  "body_search": "proforma",
  "pdf_search_text": "FV",
  "sender": "kontrahent@firma.pl",
  "unread_only": false,
  "attachments_required": true,
  "no_attachments_only": false,
  "attachment_name": "faktura",
  "attachment_extension": ".pdf",
  "selected_period": "ostatni_miesiac"
}
```

## Backward Compatibility

The implementation is fully backward compatible:

1. **Old configuration files** (without new search fields) work without errors
2. **Missing fields** are handled gracefully - default values are used
3. **Existing functionality** is unchanged - manual save still works with confirmation messages

## User Experience Improvements

### Before
1. Open application
2. Navigate to Exchange mail search tab
3. Enter sender email: `kontrahent@firma.pl`
4. Enter subject keywords: `faktura`
5. Select date period: "Ostatni miesiąc"
6. Check "Attachments required"
7. Click "Rozpocznij wyszukiwanie"
8. **Close application** → All settings lost
9. **Reopen application** → Must re-enter all settings (repeat steps 3-7)

### After
1. Open application
2. Navigate to Exchange mail search tab
3. **All previous search criteria are already filled in**
4. Optionally modify criteria or click "Rozpocznij wyszukiwanie"
5. **Close application** → Settings automatically saved
6. **Reopen application** → Settings automatically restored

## Testing

### Test Coverage

1. **Configuration Save/Load Test**
   - Verifies all 15 configuration fields are saved correctly
   - Verifies all fields are loaded correctly
   - Status: ✓ PASSED

2. **Backward Compatibility Test**
   - Verifies old configuration format still works
   - Verifies missing fields don't cause errors
   - Status: ✓ PASSED

3. **Full Workflow Test**
   - Simulates user entering search criteria
   - Simulates application close (auto-save)
   - Simulates application restart (auto-load)
   - Verifies data integrity
   - Status: ✓ PASSED

4. **Empty Values Test**
   - Verifies empty strings and default values are handled
   - Status: ✓ PASSED

### Manual Testing Steps

To manually test the feature:

1. Open the application
2. Navigate to "Przeszukiwanie Poczty" tab
3. Enter various search criteria:
   - Set folder path
   - Enter sender email
   - Enter subject keywords
   - Enter body search text
   - Select a date period
   - Check/uncheck various options
4. Close the application
5. Reopen the application
6. Navigate to "Przeszukiwanie Poczty" tab
7. **Verify**: All previously entered values are restored

## Code Examples

### Automatic Save (Silent Mode)
```python
# Called when application closes
def destroy(self):
    """Cleanup on destroy"""
    if self.search_engine.search_thread and self.search_engine.search_thread.is_alive():
        self.search_engine.cancel_search()
    # Save configuration automatically when closing
    self.save_mail_search_config(show_message=False)  # Silent mode
    super().destroy()
```

### Manual Save (With Confirmation)
```python
# Called when user clicks "Zapisz ustawienia" button
save_button.config(command=self.save_mail_search_config)  # Uses default show_message=True
```

### Loading Configuration
```python
def load_mail_search_config(self):
    """Load mail search configuration from config file"""
    try:
        if os.path.exists(MAIL_SEARCH_CONFIG_FILE):
            with open(MAIL_SEARCH_CONFIG_FILE, "r", encoding='utf-8') as f:
                config = json.load(f)
                
                # Load each field with appropriate handling
                folder_path = config.get("folder_path")
                if folder_path:
                    self.vars['folder_path'].set(folder_path)
                
                # ... (similar for other fields)
                
    except Exception as e:
        print(f"Błąd ładowania konfiguracji wyszukiwania: {e}")
```

## Benefits

1. **Time Savings**: Users don't need to re-enter search criteria after each restart
2. **Better UX**: Seamless continuation of work between sessions
3. **Productivity**: Faster access to frequently used search configurations
4. **No Learning Curve**: Feature works automatically, no user action required
5. **Non-Intrusive**: Silent auto-save on close doesn't interrupt workflow

## Future Enhancements

Potential future improvements could include:
- Multiple saved search profiles
- Export/import search configurations
- Search history with timestamps
- Search templates/favorites
- Per-folder default search criteria

## Troubleshooting

### Configuration Not Saving
- Check file permissions for `mail_search_config.json`
- Check console output for error messages
- Verify `destroy()` method is being called on application close

### Configuration Not Loading
- Verify `mail_search_config.json` exists and is valid JSON
- Check console output for loading errors
- Verify file encoding is UTF-8

### Unexpected Values
- Check the JSON file content manually
- Verify field names match exactly
- Ensure boolean values are `true`/`false` (not `"true"`/`"false"`)

## Related Files

- `gui/tab_mail_search.py` - Main implementation
- `mail_search_config.json` - Configuration storage
- `README.md` - General documentation
- `FOLDER_EXCLUSION_IMPLEMENTATION.md` - Related feature documentation

## Changelog

### Version 1.0.0 (Current Implementation)
- Added automatic save on application close
- Extended configuration to include all search fields
- Maintained backward compatibility with existing configurations
- Added silent mode for auto-save (no popups)
