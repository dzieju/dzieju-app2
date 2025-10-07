# Visual Representation of Tab Swap

## Before the Swap

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Window                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┬──────────────┬─────────┬────────┐        │
│  │Poczta        │Poczta IMAP   │Zakupy   │System  │        │
│  │Exchange      │              │         │        │        │
│  └──────────────┴──────────────┴─────────┴────────┘        │
│                                                              │
│  ┌──────────────────────────────────────────────┐           │
│  │  Poczta Exchange Tab                         │           │
│  │  ┌──────────────┬──────────────────────┐    │           │
│  │  │Wyszukiwanie  │Konfiguracja poczty   │    │           │
│  │  └──────────────┴──────────────────────┘    │           │
│  │                                              │           │
│  │  ┌────────────────────────────────────┐     │           │
│  │  │ ExchangeMailConfigWidget           │     │           │
│  │  │                                    │     │           │
│  │  │ • Exchange-specific config         │     │           │
│  │  │ • Uses: exchange_mail_config.json  │     │           │
│  │  └────────────────────────────────────┘     │           │
│  └──────────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────┐           │
│  │  Poczta IMAP Tab                             │           │
│  │  ┌──────────────┬──────────────────────┐    │           │
│  │  │Wyszukiwanie  │Konfiguracja poczty   │    │           │
│  │  └──────────────┴──────────────────────┘    │           │
│  │                                              │           │
│  │  ┌────────────────────────────────────┐     │           │
│  │  │ MailConfigWidget                   │     │           │
│  │  │                                    │     │           │
│  │  │ • IMAP/SMTP config                 │     │           │
│  │  │ • Uses: mail_config.json           │     │           │
│  │  └────────────────────────────────────┘     │           │
│  └──────────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## After the Swap ✅

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Window                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┬──────────────┬─────────┬────────┐        │
│  │Poczta        │Poczta IMAP   │Zakupy   │System  │        │
│  │Exchange      │              │         │        │        │
│  └──────────────┴──────────────┴─────────┴────────┘        │
│                                                              │
│  ┌──────────────────────────────────────────────┐           │
│  │  Poczta Exchange Tab                         │           │
│  │  ┌──────────────┬──────────────────────┐    │           │
│  │  │Wyszukiwanie  │Konfiguracja poczty   │    │           │
│  │  └──────────────┴──────────────────────┘    │           │
│  │                                              │           │
│  │  ┌────────────────────────────────────┐     │           │
│  │  │ MailConfigWidget          ◄─────┐  │     │  SWAPPED  │
│  │  │                                 │  │     │           │
│  │  │ • IMAP/SMTP config              │  │     │           │
│  │  │ • Uses: mail_config.json        │  │     │           │
│  │  └────────────────────────────────────┘     │           │
│  └──────────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                                                     │
                                                     │  SWAP
                                                     │
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────┐           │
│  │  Poczta IMAP Tab                             │           │
│  │  ┌──────────────┬──────────────────────┐    │           │
│  │  │Wyszukiwanie  │Konfiguracja poczty   │    │           │
│  │  └──────────────┴──────────────────────┘    │           │
│  │                                              │           │
│  │  ┌────────────────────────────────────┐     │           │
│  │  │ ExchangeMailConfigWidget  ◄──────┘ │     │  SWAPPED  │
│  │  │                                    │     │           │
│  │  │ • Exchange-specific config         │     │           │
│  │  │ • Uses: exchange_mail_config.json  │     │           │
│  │  └────────────────────────────────────┘     │           │
│  └──────────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Changes Visualization

### gui/tab_poczta_exchange.py
```diff
  """
  Tab for Exchange mail with sub-tabs for search and configuration
  """
  import tkinter as tk
  from tkinter import ttk
  from gui.tab_mail_search import MailSearchTab
- from gui.exchange_mail_config_widget import ExchangeMailConfigWidget
+ from gui.mail_config_widget import MailConfigWidget

  class TabPocztaExchange(ttk.Frame):
      """
      Exchange mail tab with sub-tabs:
      - Wyszukiwanie (Search)
      - Konfiguracja poczty (Mail Configuration)
      """
      def __init__(self, master=None, **kwargs):
          super().__init__(master, **kwargs)
          
          # Create a notebook for sub-tabs
          notebook = ttk.Notebook(self)
          notebook.pack(fill="both", expand=True)
          
          # Sub-tab: Wyszukiwanie (Search)
          search_tab = MailSearchTab(notebook)
          notebook.add(search_tab, text="Wyszukiwanie")
          
          # Sub-tab: Konfiguracja poczty (Mail Configuration)
-         config_tab = ExchangeMailConfigWidget(notebook)
+         config_tab = MailConfigWidget(notebook)
          notebook.add(config_tab, text="Konfiguracja poczty")
```

### gui/tab_poczta_imap.py
```diff
  import tkinter as tk
  from tkinter import ttk
  from gui.tab_mail_search import MailSearchTab
- from gui.mail_config_widget import MailConfigWidget
+ from gui.exchange_mail_config_widget import ExchangeMailConfigWidget

  class TabPocztaIMAP(ttk.Frame):
      def __init__(self, master=None, **kwargs):
          super().__init__(master, **kwargs)
          
          # Create a notebook for sub-tabs
          notebook = ttk.Notebook(self)
          notebook.pack(fill="both", expand=True)
          
          # Sub-tab: Wyszukiwanie (Search)
          search_tab = MailSearchTab(notebook)
          notebook.add(search_tab, text="Wyszukiwanie")
          
          # Sub-tab: Konfiguracja poczty (Mail Configuration)
-         config_tab = MailConfigWidget(notebook)
+         config_tab = ExchangeMailConfigWidget(notebook)
          notebook.add(config_tab, text="Konfiguracja poczty")
```

## Summary

**What Changed:**
- 4 lines of code (2 imports + 2 widget instantiations)
- Location of configuration widgets swapped
- Zero functionality changes

**What Stayed the Same:**
- Widget implementations unchanged
- Configuration files unchanged
- Search functionality unchanged
- All other tabs unchanged
- User workflows remain the same (just in different tabs)

**Impact:**
- Minimal code change
- Maximum maintainability
- Zero breaking changes
- Full backward compatibility
