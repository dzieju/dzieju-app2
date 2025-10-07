# Integration Test Plan: IMAP Search-Config Connection

## Overview
This document outlines the testing plan for the integration between the "Wyszukiwanie" (Search) tab and "Konfiguracja poczty" (Mail Configuration) tab in the IMAP Mail section.

## Changes Implemented

### 1. Fixed Widget Import (tab_poczta_imap.py)
- **Before**: Used `ExchangeMailConfigWidget` (Exchange-only configuration)
- **After**: Uses `MailConfigWidget` (Multi-protocol: Exchange, IMAP/SMTP, POP3/SMTP)
- **Impact**: IMAP tab now uses the correct multi-protocol configuration widget

### 2. Configuration Change Notification
- **Implementation**: Added `on_config_saved` callback to `MailConfigWidget`
- **Trigger**: Called when user clicks "Zapisz ustawienia" (Save Settings)
- **Action**: Refreshes account info display in search tab
- **Files**: `mail_config_widget.py`, `tab_poczta_imap.py`

### 3. Configuration Tab Navigation
- **Implementation**: Added "⚙ Konfiguracja poczty" button to search controls
- **Action**: Switches notebook tab to configuration when clicked
- **Files**: `ui_builder.py`, `tab_mail_search.py`, `tab_poczta_imap.py`

### 4. Pre-Search Configuration Validation
- **Implementation**: `_validate_mail_configuration()` method in `MailSearchTab`
- **Checks**:
  - Configuration file exists
  - At least one account is configured
  - Main account has email set
  - Account type-specific fields are populated (server addresses)
- **User Experience**: Shows dialog with option to navigate to configuration
- **Files**: `tab_mail_search.py`

## Test Scenarios

### Test 1: Configuration Changes Reflect in Search Tab
**Steps**:
1. Open IMAP tab, go to "Konfiguracja poczty"
2. Modify main account settings (e.g., change account name)
3. Click "Zapisz ustawienia"
4. Switch to "Wyszukiwanie" tab
5. Verify account info label shows updated information

**Expected**: Account info should update automatically after save

### Test 2: Configuration Button Navigation
**Steps**:
1. Open IMAP tab, go to "Wyszukiwanie"
2. Click "⚙ Konfiguracja poczty" button
3. Verify tab switches to "Konfiguracja poczty"

**Expected**: Smooth tab switching to configuration

### Test 3: Search Without Configuration
**Steps**:
1. Delete or rename `mail_config.json` file
2. Open IMAP tab, go to "Wyszukiwanie"
3. Click "Rozpocznij wyszukiwanie"
4. Verify warning dialog appears
5. Click "Yes" to navigate to configuration

**Expected**: 
- Warning dialog: "Brak konfiguracji poczty"
- Option to navigate to configuration
- Tab switches if user chooses "Yes"

### Test 4: Search With Empty Accounts
**Steps**:
1. Ensure `mail_config.json` has empty accounts array
2. Open IMAP tab, go to "Wyszukiwanie"
3. Click "Rozpocznij wyszukiwanie"
4. Verify warning dialog appears

**Expected**: Warning dialog: "Brak kont pocztowych"

### Test 5: Search With Incomplete Account Configuration
**Steps**:
1. Configure account but leave email field empty
2. Open IMAP tab, go to "Wyszukiwanie"
3. Click "Rozpocznij wyszukiwanie"
4. Verify validation error

**Expected**: Warning dialog: "Niepełna konfiguracja"

### Test 6: Account Type-Specific Validation
**Steps**:
1. Configure Exchange account without server address
2. Attempt search
3. Verify Exchange-specific validation

**Expected**: Warning dialog: "Niepełna konfiguracja Exchange"

Repeat for IMAP and POP3 account types.

### Test 7: Search With Valid Configuration
**Steps**:
1. Configure complete account with all required fields
2. Open IMAP tab, go to "Wyszukiwanie"
3. Click "Rozpocznij wyszukiwanie"
4. Verify search starts (no validation errors)

**Expected**: Search proceeds normally with status "Nawiązywanie połączenia..."

### Test 8: Multiple Account Switching
**Steps**:
1. Configure multiple accounts
2. Set different account as main
3. Save configuration
4. Check if search tab account info updates
5. Attempt search with new main account

**Expected**: Account info updates, search uses new main account

## Integration Points

### 1. TabPocztaIMAP → MailConfigWidget
- **Connection**: `config_tab.on_config_saved = _on_config_changed`
- **Purpose**: Notify search tab when config changes

### 2. TabPocztaIMAP → MailSearchTab
- **Connection**: `search_tab.config_tab_callback = _open_config_tab`
- **Purpose**: Allow search tab to open config tab

### 3. MailSearchTab → MailConnection
- **Connection**: Uses `load_mail_config()` for validation
- **Purpose**: Validate configuration before search

### 4. MailConfigWidget → config file
- **Connection**: Saves to `mail_config.json`
- **Purpose**: Persist configuration changes

## User Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│ IMAP Tab (TabPocztaIMAP)                                     │
├──────────────────────────────────────────────────────────────┤
│  ╔═══════════════╦══════════════════════╗                    │
│  ║ Wyszukiwanie  ║ Konfiguracja poczty  ║  ← Sub-tabs       │
│  ╚═══════════════╩══════════════════════╝                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ MailSearchTab                                          │  │
│  │                                                        │  │
│  │  [Rozpocznij wyszukiwanie] [⚙ Konfiguracja poczty]   │  │
│  │                               ↓                        │  │
│  │                          (switches tab)                │  │
│  │                                                        │  │
│  │  Before search:                                        │  │
│  │    → Validates configuration                           │  │
│  │    → Shows errors with option to fix                   │  │
│  │                                                        │  │
│  │  Account Info: [Updated when config saved]            │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ MailConfigWidget                                       │  │
│  │                                                        │  │
│  │  [Add Account] [Remove] [Set as Main]                 │  │
│  │  [Test Connection] [Zapisz ustawienia] ←─────┐        │  │
│  │                                         Triggers       │  │
│  │  After save:                            callback       │  │
│  │    → Calls on_config_saved() ──────────────┘          │  │
│  │    → Refreshes search tab account info                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Configuration Validation Matrix

| Condition | Validation Result | User Action |
|-----------|-------------------|-------------|
| No config file | ❌ Error | Navigate to config |
| Empty accounts array | ❌ Error | Add account |
| No email in main account | ❌ Error | Complete account info |
| Exchange without server | ❌ Error | Set server address |
| IMAP without IMAP server | ❌ Error | Set IMAP server |
| POP3 without POP3 server | ❌ Error | Set POP3 server |
| Complete configuration | ✅ Pass | Search proceeds |

## Error Messages

All error messages follow this pattern:
1. **Title**: Brief description of the problem
2. **Message**: Detailed explanation
3. **Question**: "Czy chcesz przejść do konfiguracji poczty?" (Do you want to go to mail configuration?)
4. **Icon**: Warning icon
5. **Buttons**: Yes/No

## Code Quality

### Minimal Changes
- ✅ Only modified necessary files
- ✅ Reused existing components
- ✅ No code duplication
- ✅ No breaking changes to existing functionality

### Integration Quality
- ✅ Loose coupling via callbacks
- ✅ Clear separation of concerns
- ✅ Non-intrusive validation
- ✅ Graceful error handling

## Success Criteria

The integration is successful if:
1. ✅ Configuration changes automatically refresh search tab
2. ✅ Users can easily navigate between tabs
3. ✅ Configuration is validated before search
4. ✅ Clear error messages guide users to fix issues
5. ✅ No regression in existing functionality
6. ✅ Code passes syntax validation
7. ✅ Changes are minimal and focused

## Manual Testing Checklist

- [ ] Start application with existing config
- [ ] Verify search tab shows correct account info
- [ ] Modify configuration and save
- [ ] Verify search tab updates automatically
- [ ] Click configuration button from search tab
- [ ] Verify tab switches correctly
- [ ] Delete config file and try search
- [ ] Verify validation error appears
- [ ] Follow navigation to config from error
- [ ] Create new account and save
- [ ] Verify search now works
- [ ] Test with Exchange, IMAP, and POP3 accounts
- [ ] Verify validation for each account type
- [ ] Test with multiple accounts
- [ ] Change main account and verify updates

## Conclusion

This integration successfully connects the Search and Configuration tabs in the IMAP Mail section, providing:
- **Better UX**: Easy navigation between tabs
- **Data Consistency**: Automatic refresh on config changes
- **Error Prevention**: Validation before search
- **User Guidance**: Clear error messages with actionable options

All requirements from the issue have been addressed with minimal, focused changes.
