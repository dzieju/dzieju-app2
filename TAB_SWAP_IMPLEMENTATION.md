# Mail Configuration Tab Swap Implementation

## Issue Requirements

**Zamiana miejsc zakładek Konfiguracja Poczty między IMAP a Exchange**

### Requested Changes
1. ✅ Przenieś zakładkę "Konfiguracja poczty" z sekcji Poczta IMAP do sekcji Poczta Exchange
2. ✅ Przenieś zakładkę "Konfiguracja poczty" z sekcji Poczta Exchange do sekcji Poczta IMAP  
3. ✅ Nie zmieniaj funkcji ani logiki tych zakładek — mają pozostać identyczne funkcjonalnie, tylko zmienić miejsce występowania

## Implementation Summary

### Changes Made

#### Modified Files

**1. `gui/tab_poczta_exchange.py`** (2 lines changed)
- Changed import: `from gui.exchange_mail_config_widget import ExchangeMailConfigWidget` → `from gui.mail_config_widget import MailConfigWidget`
- Changed widget: `config_tab = ExchangeMailConfigWidget(notebook)` → `config_tab = MailConfigWidget(notebook)`

**2. `gui/tab_poczta_imap.py`** (2 lines changed)
- Changed import: `from gui.mail_config_widget import MailConfigWidget` → `from gui.exchange_mail_config_widget import ExchangeMailConfigWidget`
- Changed widget: `config_tab = MailConfigWidget(notebook)` → `config_tab = ExchangeMailConfigWidget(notebook)`

### Architecture After Swap

```
Main Window
├── Poczta Exchange (TabPocztaExchange)
│   ├── Wyszukiwanie (MailSearchTab)
│   └── Konfiguracja poczty (MailConfigWidget) ← SWAPPED (now uses IMAP widget)
├── Poczta IMAP (TabPocztaIMAP)
│   ├── Wyszukiwanie (MailSearchTab)
│   └── Konfiguracja poczty (ExchangeMailConfigWidget) ← SWAPPED (now uses Exchange widget)
├── Zakupy
└── System
```

### Configuration Files

After the swap:

| Tab Section | Widget Used | Config File |
|-------------|-------------|-------------|
| Poczta Exchange → Konfiguracja | `MailConfigWidget` | `mail_config.json` |
| Poczta IMAP → Konfiguracja | `ExchangeMailConfigWidget` | `exchange_mail_config.json` |

### Compliance with Requirements

✅ **Requirement 1:** Przeniesienie zakładki z IMAP do Exchange
- The MailConfigWidget (originally in IMAP) is now in Exchange tab

✅ **Requirement 2:** Przeniesienie zakładki z Exchange do IMAP  
- The ExchangeMailConfigWidget (originally in Exchange) is now in IMAP tab

✅ **Requirement 3:** Nie zmieniaj funkcji ani logiki
- No changes to the widgets themselves
- No changes to functionality or logic
- Only the location (parent tab) changed

## Code Changes

### Diff Summary
```diff
# gui/tab_poczta_exchange.py
-from gui.exchange_mail_config_widget import ExchangeMailConfigWidget
+from gui.mail_config_widget import MailConfigWidget

-config_tab = ExchangeMailConfigWidget(notebook)
+config_tab = MailConfigWidget(notebook)

# gui/tab_poczta_imap.py
-from gui.mail_config_widget import MailConfigWidget
+from gui.exchange_mail_config_widget import ExchangeMailConfigWidget

-config_tab = MailConfigWidget(notebook)
+config_tab = ExchangeMailConfigWidget(notebook)
```

## Testing

### Syntax Validation
```bash
python3 -m py_compile gui/tab_poczta_exchange.py
python3 -m py_compile gui/tab_poczta_imap.py
python3 -m py_compile gui/main_window.py
# Result: ✓ All files pass syntax validation
```

### Structure Validation
- ✓ Exchange tab now uses MailConfigWidget (IMAP widget)
- ✓ IMAP tab now uses ExchangeMailConfigWidget (Exchange widget)
- ✓ No changes to widget functionality
- ✓ Proper tab nesting structure maintained
- ✓ Search tabs remain unchanged in both sections

## Impact Analysis

### Code Impact
- Files modified: 2
- Lines changed: 4 (2 per file)
- Breaking changes: None
- Backward compatibility: Full (widgets remain functional)

### User Impact
- Configuration tabs are now swapped between Exchange and IMAP
- IMAP users will now see Exchange-style configuration in their tab
- Exchange users will now see IMAP-style configuration in their tab
- Configuration files remain separate (no data mixing)

## Conclusion

The implementation successfully:
- ✅ Swaps the configuration tabs between IMAP and Exchange
- ✅ Maintains all existing functionality
- ✅ Makes minimal surgical changes (4 lines total)
- ✅ Preserves backward compatibility
- ✅ Keeps configuration files separate

The solution is minimal, surgical, and meets all requirements specified in the issue.
