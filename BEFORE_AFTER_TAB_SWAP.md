# Before/After Comparison - Tab Configuration Swap

## Issue Request

**Zamiana miejsc zakładek Konfiguracja Poczty między IMAP a Exchange**

The issue requested swapping the configuration tabs between the IMAP and Exchange sections.

## Before the Swap

### Tab Structure
```
Main Window
├── Poczta Exchange
│   ├── Wyszukiwanie (Search)
│   └── Konfiguracja poczty (ExchangeMailConfigWidget)
│       → Used exchange_mail_config.json
│       → Exchange-specific configuration
├── Poczta IMAP
│   ├── Wyszukiwanie (Search)
│   └── Konfiguracja poczty (MailConfigWidget)
│       → Used mail_config.json
│       → IMAP/SMTP configuration
```

### Code Before
**gui/tab_poczta_exchange.py:**
```python
from gui.exchange_mail_config_widget import ExchangeMailConfigWidget
# ...
config_tab = ExchangeMailConfigWidget(notebook)
```

**gui/tab_poczta_imap.py:**
```python
from gui.mail_config_widget import MailConfigWidget
# ...
config_tab = MailConfigWidget(notebook)
```

## After the Swap

### Tab Structure
```
Main Window
├── Poczta Exchange
│   ├── Wyszukiwanie (Search)
│   └── Konfiguracja poczty (MailConfigWidget) ← SWAPPED
│       → Now uses mail_config.json
│       → Now uses IMAP/SMTP configuration
├── Poczta IMAP
│   ├── Wyszukiwanie (Search)
│   └── Konfiguracja poczty (ExchangeMailConfigWidget) ← SWAPPED
│       → Now uses exchange_mail_config.json
│       → Now uses Exchange-specific configuration
```

### Code After
**gui/tab_poczta_exchange.py:**
```python
from gui.mail_config_widget import MailConfigWidget
# ...
config_tab = MailConfigWidget(notebook)
```

**gui/tab_poczta_imap.py:**
```python
from gui.exchange_mail_config_widget import ExchangeMailConfigWidget
# ...
config_tab = ExchangeMailConfigWidget(notebook)
```

## Summary of Changes

| Aspect | Before | After |
|--------|--------|-------|
| Exchange → Config Widget | ExchangeMailConfigWidget | MailConfigWidget |
| Exchange → Config File | exchange_mail_config.json | mail_config.json |
| IMAP → Config Widget | MailConfigWidget | ExchangeMailConfigWidget |
| IMAP → Config File | mail_config.json | exchange_mail_config.json |
| Lines Changed | - | 4 (2 per file) |
| Files Modified | - | 2 |
| Functionality Changes | - | None (only location swap) |

## Impact

### Technical Impact
- **Minimal code changes**: Only 2 imports and 2 widget instantiations changed
- **No breaking changes**: Both widgets continue to work as before
- **Configuration separation maintained**: Each widget still uses its own config file
- **Backward compatibility**: Full (widgets are functionally identical)

### User Impact
- Users accessing "Poczta Exchange" tab will now see IMAP/SMTP configuration
- Users accessing "Poczta IMAP" tab will now see Exchange configuration
- The tabs have been swapped as requested, but all functionality remains intact

## Compliance

✅ **Requirement 1**: Przenieś zakładkę "Konfiguracja poczty" z IMAP do Exchange
- MailConfigWidget (originally in IMAP) is now in Exchange tab

✅ **Requirement 2**: Przenieś zakładkę "Konfiguracja poczty" z Exchange do IMAP
- ExchangeMailConfigWidget (originally in Exchange) is now in IMAP tab

✅ **Requirement 3**: Nie zmieniaj funkcji ani logiki
- No changes to widget implementations
- No changes to functionality
- Only the parent tab (location) was swapped
