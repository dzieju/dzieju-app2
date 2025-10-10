# PDF Attachment Search Fix

## Problem Description

The application was not finding emails with the subject "Play - e-korekta do pobrania" containing PDF attachment "KOREKTA-K_00025405_10_25-KONTO_12629296.pdf" when searching for NIP numbers in PDF files, even though the NIP existed in the PDF content.

## Root Cause Analysis

The issue was caused by the way Exchange messages were being fetched from the server. When using exchangelib's `.filter()` or `.all()` methods without specifying which fields to load, the library uses a minimal property loading strategy (IdOnly shape by default). This means:

1. Messages are fetched with only basic properties (id, subject, etc.)
2. **Attachments are NOT loaded by default**
3. When the code tried to access `message.attachments`, it would return `None` or an empty list
4. As a result, PDF search would skip these messages entirely

### Code Before Fix

```python
messages = search_folder.filter(combined_query).order_by('-datetime_received')
```

This fetched messages without attachment data.

### Code After Fix

```python
messages = search_folder.filter(combined_query).only(
    'subject', 'sender', 'datetime_received', 'is_read', 
    'has_attachments', 'attachments', 'id'
).order_by('-datetime_received')
```

This explicitly requests attachment data to be loaded with the messages.

## Solution Implemented

### Changes Made

1. **Added `.only()` method calls** to all Exchange message queries in three search components:
   - `gui/exchange_search_components/search_engine.py`
   - `gui/mail_search_components/search_engine.py`
   - `gui/imap_search_components/search_engine.py`

2. **Specified required fields** in `.only()` call:
   - `subject` - Email subject line
   - `sender` - Email sender information
   - `datetime_received` - When email was received
   - `is_read` - Read/unread status
   - `has_attachments` - Boolean flag for attachment presence
   - `attachments` - **Critical: The actual attachment data**
   - `id` - Message identifier

3. **Added debug logging** to track attachment loading:
   ```python
   log(f"[PDF SEARCH] Sprawdzanie {attachment_count} załączników w wiadomości: {message.subject[:50]}...")
   ```

### Locations Fixed

Each search component had 4 locations where messages were fetched:
- Primary query with filters
- Fallback query (all messages)
- No-filter query (all messages)
- Alternative query method

All 12 locations across 3 files were updated with the `.only()` method.

## Testing

### Automated Tests

Created `tests/test_pdf_attachment_loading.py` with 4 test cases:

1. **test_message_with_pdf_attachment_is_accessible** - Verifies PDF attachments are accessible
2. **test_message_without_attachments** - Verifies empty attachment handling
3. **test_message_with_multiple_pdf_attachments** - Verifies multiple attachment handling
4. **test_exchange_query_includes_attachments_field** - Verifies `.only()` includes 'attachments'

All tests pass successfully.

### Existing Tests

Ran full test suite - all tests continue to pass except one unrelated tkinter import issue.

## Expected Behavior After Fix

1. **Attachments are now loaded** when messages are fetched from Exchange
2. **PDF search will now work** for all emails with PDF attachments
3. The email "Play - e-korekta do pobrania" with "KOREKTA-K_00025405_10_25-KONTO_12629296.pdf" will now be found when searching for NIP in PDFs
4. **Debug logging** provides visibility into attachment processing

## Performance Considerations

- Loading attachments adds some overhead to message fetching
- However, this is necessary for PDF search functionality to work
- The `.only()` method limits the fields loaded, keeping overhead minimal
- Only the specific fields needed are fetched, not all possible message properties

## Verification Steps

To verify the fix works:

1. Open the application
2. Navigate to email search with PDF content search
3. Enter a NIP number that exists in "KOREKTA-K_00025405_10_25-KONTO_12629296.pdf"
4. Search in the folder containing "Play - e-korekta do pobrania" email
5. Verify the email is now found in results
6. Check logs for "[PDF SEARCH]" entries showing attachment processing

## Technical Details

### Exchange Web Services (EWS) Property Loading

ExchangeLib uses EWS to communicate with Exchange servers. By default:
- Messages use "IdOnly" shape (minimal data)
- Attachments require explicit loading
- `.only()` method specifies which properties to include in the request
- This reduces the number of round trips to the server

### Why This Wasn't Caught Earlier

1. In some Exchange configurations, attachments might be loaded automatically
2. The issue depends on server version and configuration
3. Testing may have been done with IMAP (which has different behavior)
4. The bug manifested only when PDF search was used with Exchange accounts

## Future Improvements

Consider:
1. Add configuration option to control which fields are loaded
2. Implement attachment lazy loading for better performance
3. Add more comprehensive logging around attachment access
4. Create integration tests with actual Exchange server

## References

- ExchangeLib documentation: https://ecederstrand.github.io/exchangelib/
- Exchange Web Services (EWS) documentation
- Issue: "Błąd: Przeszukiwanie NIP w plikach PDF z załączników"
