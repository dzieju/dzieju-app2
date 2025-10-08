# Diagram Architektury Obecnej - Exchange i IMAP

## Obecna Struktura (z Współdzielonymi Komponentami)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          APLIKACJA GŁÓWNA (main.py)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
        ┌───────────▼──────────┐           ┌───────────▼──────────┐
        │  Zakładka Exchange   │           │   Zakładka IMAP      │
        │ (tab_poczta_exchange)│           │  (tab_poczta_imap)   │
        └───────────┬──────────┘           └───────────┬──────────┘
                    │                                   │
        ┌───────────┴─────────┐           ┌───────────┴──────────┐
        │                     │           │                      │
┌───────▼─────────┐  ┌────────▼────────┐  ┌──────▼──────┐  ┌────▼─────────┐
│ Exchange Search │  │ Exchange Config │  │ IMAP Search │  │ IMAP Config  │
│ (tab_exchange_  │  │ (exchange_mail_ │  │ (tab_imap_  │  │ (tab_imap_   │
│  search.py)     │  │  config_widget) │  │  search.py) │  │  config.py)  │
└───────┬─────────┘  └─────────────────┘  └─────┬───────┘  └──────────────┘
        │                                        │
        │            ┌───────────────────────────┘
        │            │                    
        │            │         ┌──────────────────┐
        └────────────┴─────────►  IMAP Folders   │
                     │         │ (tab_imap_       │
                     │         │  folders.py)     │
                     │         └──────────────────┘
                     │
                     │
        ┌────────────▼───────────────┐
        │                            │
        │  ⚠️  WSPÓŁDZIELONE         │
        │  mail_search_components/   │
        │                            │
        │  ┌──────────────────────┐  │
        │  │ MailConnection       │  │ ◄── Używane przez Exchange i IMAP
        │  │ - get_imap_account() │  │
        │  │ - get_exchange_..()  │  │
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │ EmailSearchEngine    │  │ ◄── Używane przez Exchange i IMAP
        │  │ - search_emails()    │  │
        │  │ - process_pdfs()     │  │
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │ ResultsDisplay       │  │ ◄── Używane przez Exchange i IMAP
        │  │ - display_results()  │  │
        │  │ - handle_selection() │  │
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │ MailSearchUI         │  │ ◄── Używane przez Exchange i IMAP
        │  │ - create_widgets()   │  │
        │  │ - build_layout()     │  │
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │ PDFProcessor         │  │ ◄── Używane przez Exchange i IMAP
        │  │ PDFHistoryManager    │  │
        │  │ PDFHistoryDisplay    │  │
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │ FolderBrowser        │  │ ◄── Używane tylko przez IMAP
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │ datetime_utils       │  │ ◄── Używane pośrednio
        │  └──────────────────────┘  │
        │                            │
        └────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼─────────┐
│ Config Exchange  │    │  Config IMAP     │
│ - exchange_mail_ │    │  - mail_config   │
│   config.json    │    │    .json         │
│ - exchange_      │    │  - imap_search_  │
│   search_config  │    │    config.json   │
│   .json          │    │                  │
└──────────────────┘    └──────────────────┘
```

## Legenda

- `┌─┐` - Komponenty/Moduły
- `│` `─` - Zależności/Importy
- `◄──` - "Używane przez"
- `⚠️` - Ostrzeżenie o współdzielonych komponentach

## Problem

**Wszystkie moduły wyszukiwania (ExchangeSearchTab, IMAPSearchTab) importują i używają tych samych klas z `mail_search_components/`**, co prowadzi do:

1. **Coupling** - Zmiana w jednym komponencie wpływa na obie zakładki
2. **Brak izolacji** - Niemożliwe jest niezależne testowanie
3. **Ryzyko regresji** - Poprawka dla IMAP może zepsuć Exchange lub odwrotnie
4. **Wspólna historia PDF** - Obie zakładki dzielą tę samą historię przeszukanych PDF

## Mapa Importów

### Exchange Search (tab_exchange_search.py)
```python
❌ from gui.mail_search_components.mail_connection import MailConnection
❌ from gui.mail_search_components.search_engine import EmailSearchEngine
❌ from gui.mail_search_components.results_display import ResultsDisplay
❌ from gui.mail_search_components.ui_builder import MailSearchUI
❌ from gui.mail_search_components.pdf_history_manager import PDFHistoryManager
❌ from gui.mail_search_components.pdf_history_display import PDFHistoryDisplayWindow
❌ from gui.mail_search_components.mail_connection import FolderNameMapper
```

### IMAP Search (tab_imap_search.py)
```python
❌ from gui.mail_search_components.mail_connection import MailConnection
❌ from gui.mail_search_components.search_engine import EmailSearchEngine
❌ from gui.mail_search_components.results_display import ResultsDisplay
❌ from gui.mail_search_components.ui_builder import MailSearchUI
❌ from gui.mail_search_components.pdf_history_manager import PDFHistoryManager
❌ from gui.mail_search_components.pdf_history_display import PDFHistoryDisplayWindow
❌ from gui.mail_search_components.mail_connection import FolderNameMapper
```

### IMAP Folders (tab_imap_folders.py)
```python
❌ from gui.mail_search_components.folder_browser import FolderBrowser
❌ from gui.mail_search_components.mail_connection import MailConnection
```

**❌ = Współdzielony import (narusza separację)**

## Poziom Separacji

### ✅ Całkowicie Oddzielone:
- Konfiguracje kont (pliki JSON)
- Konfiguracje wyszukiwania (pliki JSON)
- Widgety konfiguracji kont (ExchangeMailConfigWidget, IMAPConfigWidget)
- Główne kontenery zakładek (TabPocztaExchange, TabPocztaIMAP)

### ⚠️ Pozornie Oddzielone (osobne pliki, ale wspólne zależności):
- Moduły wyszukiwania (ExchangeSearchTab, IMAPSearchTab)
- Przeglądarka folderów IMAP (IMAPFoldersTab)

### ❌ Całkowicie Współdzielone:
- Zarządzanie połączeniami (MailConnection)
- Silnik wyszukiwania (EmailSearchEngine)
- Wyświetlanie wyników (ResultsDisplay)
- Builder UI (MailSearchUI)
- Przetwarzanie PDF (PDFProcessor, PDFHistoryManager, PDFHistoryDisplay)
- Przeglądarka folderów (FolderBrowser)
- Narzędzia daty (datetime_utils)

---

## Porównanie: Co Powinno Być vs Co Jest

### Idealny Stan (Pełna Separacja):

```
┌─────────────────────────────────────┐    ┌─────────────────────────────────┐
│         ZAKŁADKA EXCHANGE           │    │         ZAKŁADKA IMAP           │
│                                     │    │                                 │
│  ┌───────────────────────────────┐  │    │  ┌──────────────────────────┐  │
│  │ tab_exchange_search.py        │  │    │  │ tab_imap_search.py       │  │
│  └─────────────┬─────────────────┘  │    │  └────────────┬─────────────┘  │
│                │                    │    │               │                │
│  ┌─────────────▼─────────────────┐  │    │  ┌────────────▼─────────────┐  │
│  │ exchange_search_components/   │  │    │  │ imap_search_components/  │  │
│  │                               │  │    │  │                          │  │
│  │ - ExchangeConnection          │  │    │  │ - IMAPConnection         │  │
│  │ - ExchangeSearchEngine        │  │    │  │ - IMAPSearchEngine       │  │
│  │ - ExchangeResultsDisplay      │  │    │  │ - IMAPResultsDisplay     │  │
│  │ - ExchangeSearchUI            │  │    │  │ - IMAPSearchUI           │  │
│  │ - ExchangePDFProcessor        │  │    │  │ - IMAPPDFProcessor       │  │
│  └───────────────────────────────┘  │    │  └──────────────────────────┘  │
│                                     │    │                                 │
│  ┌───────────────────────────────┐  │    │  ┌──────────────────────────┐  │
│  │ exchange_mail_config.json     │  │    │  │ mail_config.json         │  │
│  │ exchange_search_config.json   │  │    │  │ imap_search_config.json  │  │
│  └───────────────────────────────┘  │    │  └──────────────────────────┘  │
└─────────────────────────────────────┘    └─────────────────────────────────┘
         NO SHARED CODE ✅                          NO SHARED CODE ✅
```

### Obecny Stan (Ze Współdzielonymi Komponentami):

```
┌─────────────────────────────────────┐    ┌─────────────────────────────────┐
│         ZAKŁADKA EXCHANGE           │    │         ZAKŁADKA IMAP           │
│                                     │    │                                 │
│  ┌───────────────────────────────┐  │    │  ┌──────────────────────────┐  │
│  │ tab_exchange_search.py        │  │    │  │ tab_imap_search.py       │  │
│  └─────────────┬─────────────────┘  │    │  └────────────┬─────────────┘  │
│                │                    │    │               │                │
│                └────────────────────┼────┼───────────────┘                │
│                                     │    │                                 │
└─────────────────────────────────────┘    └─────────────────────────────────┘
                 │                                      │
                 └──────────────┬───────────────────────┘
                                │
                  ┌─────────────▼──────────────┐
                  │  ⚠️  WSPÓŁDZIELONE         │
                  │  mail_search_components/   │
                  │                            │
                  │  - MailConnection          │
                  │  - EmailSearchEngine       │
                  │  - ResultsDisplay          │
                  │  - MailSearchUI            │
                  │  - PDFProcessor            │
                  │  - PDFHistoryManager       │
                  │  - etc.                    │
                  └────────────────────────────┘
                         SHARED CODE ❌
```

## Wnioski

1. **Separacja pozorna:** Chociaż istnieją osobne pliki dla Exchange i IMAP, korzystają one z tego samego kodu wewnętrznego
2. **Wysoki coupling:** Zmiana w jednym komponencie wpływa na obie zakładki
3. **Naruszenie wymagań:** Zadanie wymaga "całkowicie osobnych plików" - obecna implementacja tego nie spełnia
4. **Potrzeba refaktoryzacji:** Aby spełnić wymogi, konieczne jest rozdzielenie wspólnych komponentów

---

**Zalecenie:** Implementacja pełnej separacji zgodnie z diagramem "Idealny Stan"
