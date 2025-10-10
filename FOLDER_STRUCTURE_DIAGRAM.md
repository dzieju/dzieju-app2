# Diagram struktury folderów w programie

## Poczta Exchange - struktura folderów

```
📁 Top of Information Store (Root)
│
├── 📥 Inbox (Odebrane) ✅ SYSTEMOWY - WYŚWIETLANY
│   ├── 📁 Archive (użytkownika)
│   │   ├── 📁 2024
│   │   └── 📁 2023
│   └── 📁 Projects (użytkownika)
│       ├── 📁 ProjectA
│       └── 📁 ProjectB
│
├── 📤 Sent Items (Wysłane) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── 📝 Drafts (Szkice) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── 🗑️ Deleted Items (Kosz) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── ⚠️ Junk Email (Spam) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── 📮 Outbox (Skrzynka nadawcza) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── 📦 Archive (Archiwum) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── 📅 Calendar ⚠️ TECHNICZNY - OBECNIE WYŚWIETLANY (problem)
│
├── 👥 Contacts ⚠️ TECHNICZNY - OBECNIE WYŚWIETLANY (problem)
│
├── ✓ Tasks ⚠️ TECHNICZNY - OBECNIE WYŚWIETLANY (problem)
│
├── 📓 Notes ⚠️ TECHNICZNY - OBECNIE WYŚWIETLANY (problem)
│
├── 📔 Journal ⚠️ TECHNICZNY - OBECNIE WYŚWIETLANY (problem)
│
└── 💬 Conversation History ⚠️ TECHNICZNY - OBECNIE WYŚWIETLANY (problem)
```

---

## Poczta IMAP - struktura folderów

```
📁 IMAP Server Root
│
├── 📥 INBOX (Odebrane) ✅ SYSTEMOWY - WYŚWIETLANY
│   └── 📁 Subfolder1 (użytkownika)
│
├── 📤 SENT (Wysłane) ✅ SYSTEMOWY - WYŚWIETLANY
│   └── 📁 Sent/2024
│
├── 📝 DRAFTS (Szkice) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── 🗑️ TRASH (Kosz) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── ⚠️ SPAM (Spam) ✅ SYSTEMOWY - WYŚWIETLANY
│
├── 📦 ARCHIVE (Archiwum) ✅ SYSTEMOWY - WYŚWIETLANY
│
└── 📁 Custom Folders (użytkownika)
    ├── 📁 Work
    ├── 📁 Personal
    └── 📁 Projects
```

---

## Legenda

| Symbol | Znaczenie |
|--------|-----------|
| ✅ SYSTEMOWY - WYŚWIETLANY | Folder systemowy z mailami, prawidłowo wyświetlany |
| ⚠️ TECHNICZNY | Folder techniczny bez maili, niepotrzebnie wyświetlany |
| 📁 | Folder użytkownika (własny) |
| 📥 📤 📝 🗑️ ⚠️ 📦 📮 | Ikony folderów systemowych |
| 📅 👥 ✓ 📓 📔 💬 | Ikony folderów technicznych Exchange |

---

## Wyświetlanie w interfejsie użytkownika (GUI)

### Okno "Foldery Exchange" / "Foldery IMAP"

```
┌─────────────────────────────────────────────────────────────┐
│ 🔄 Odśwież foldery          Konto: user@example.com         │
├─────────────────────────────────────────────────────────────┤
│ Znaleziono 15 folderów Exchange                             │
├─────────────────────────────────────────────────────────────┤
│ Nazwa folderu              │ Wiadomości │ Rozmiar           │
├────────────────────────────┼────────────┼───────────────────┤
│ 📥 Odebrane                │     1,234  │ 185.1 MB          │
│ 📝 Szkice                  │        12  │   1.8 MB          │
│ 📤 Wysłane                 │       567  │  85.1 MB          │
│ ⚠️ Spam                    │        45  │   6.8 MB          │
│ 🗑️ Kosz                    │        89  │  13.4 MB          │
│ 📮 Skrzynka nadawcza       │         0  │   0 B             │
│ 📦 Archiwum                │       234  │  35.1 MB          │
│ 📁 2023                    │        56  │   8.4 MB          │
│ 📁 2024                    │       123  │  18.5 MB          │
│ 📁 Projekty                │        78  │  11.7 MB          │
│   📁 ProjectA              │        34  │   5.1 MB          │
│   📁 ProjectB              │        44  │   6.6 MB          │
│ 📅 Calendar ⚠️              │         -  │   -               │
│ 👥 Contacts ⚠️              │         -  │   -               │
│ ✓ Tasks ⚠️                 │         -  │   -               │
└─────────────────────────────────────────────────────────────┘
```

**Uwaga**: Foldery techniczne (Calendar, Contacts, Tasks) nie mają liczby wiadomości, ponieważ nie zawierają maili.

---

## Hierarchia folderów - przed i po poprawce

### ❌ PRZED poprawką (stara wersja)
```
Rozpoczęcie od: Inbox
│
├── 📁 Archive
│   ├── 📁 2024
│   └── 📁 2023
└── 📁 Projects
    ├── 📁 ProjectA
    └── 📁 ProjectB

BRAKUJĄCE: Sent Items, Drafts, Deleted Items, Junk Email, Outbox
```

### ✅ PO poprawce (obecna wersja)
```
Rozpoczęcie od: Root (Top of Information Store)
│
├── 📥 Inbox
│   ├── 📁 Archive
│   │   ├── 📁 2024
│   │   └── 📁 2023
│   └── 📁 Projects
│       ├── 📁 ProjectA
│       └── 📁 ProjectB
├── 📤 Sent Items ✅ TERAZ WIDOCZNE
├── 📝 Drafts ✅ TERAZ WIDOCZNE
├── 🗑️ Deleted Items ✅ TERAZ WIDOCZNE
├── ⚠️ Junk Email ✅ TERAZ WIDOCZNE
├── 📮 Outbox ✅ TERAZ WIDOCZNE
├── 📦 Archive ✅ TERAZ WIDOCZNE
├── 📅 Calendar ⚠️ NIEPOŻĄDANE
├── 👥 Contacts ⚠️ NIEPOŻĄDANE
└── ✓ Tasks ⚠️ NIEPOŻĄDANE

KOMPLETNE: Wszystkie foldery widoczne
PROBLEM: Foldery techniczne są niepotrzebnie widoczne
```

---

## Proponowane rozwiązanie - filtrowanie folderów technicznych

### Po implementacji filtrowania (przyszła wersja):
```
Rozpoczęcie od: Root (Top of Information Store)
│
├── 📥 Inbox
│   ├── 📁 Archive
│   │   ├── 📁 2024
│   │   └── 📁 2023
│   └── 📁 Projects
│       ├── 📁 ProjectA
│       └── 📁 ProjectB
├── 📤 Sent Items
├── 📝 Drafts
├── 🗑️ Deleted Items
├── ⚠️ Junk Email
├── 📮 Outbox
└── 📦 Archive

[UKRYTE przez filtr folder_class]:
  Calendar (IPF.Appointment)
  Contacts (IPF.Contact)
  Tasks (IPF.Task)
  Notes (IPF.Note)
  Journal (IPF.Journal)

IDEALNE: Tylko foldery z mailami (IPF.Note)
```

---

## Kod filtrowania (propozycja)

```python
# W metodzie _get_exchange_folders_with_details()

# Lista klas folderów do pominięcia (nie-mailowe)
EXCLUDED_FOLDER_CLASSES = [
    'IPF.Appointment',  # Calendar
    'IPF.Contact',      # Contacts
    'IPF.Task',         # Tasks
    'IPF.StickyNote',   # Notes
    'IPF.Journal',      # Journal
]

for folder in all_folders:
    folder_class = getattr(folder, 'folder_class', None)
    
    # Pomiń foldery nie-mailowe
    if folder_class and folder_class in EXCLUDED_FOLDER_CLASSES:
        log(f"[MAIL CONNECTION] Skipping non-mail folder: {folder.name} (class: {folder_class})")
        continue
    
    # Tylko foldery z mailami (IPF.Note) lub bez określonej klasy
    if folder_class is None or folder_class.startswith('IPF.Note'):
        # Dodaj folder do listy
        folders_info.append(folder_info)
```

---

## Podsumowanie

### Stan obecny:
- ✅ **12 folderów mailowych** (systemowe + użytkownika) - prawidłowo wyświetlane
- ⚠️ **6 folderów technicznych** (Calendar, Contacts, Tasks, Notes, Journal, Conversation History) - niepotrzebnie wyświetlane

### Stan docelowy (po implementacji filtrowania):
- ✅ **12 folderów mailowych** - wyświetlane
- ✅ **6 folderów technicznych** - ukryte (opcjonalnie: checkbox "Pokaż wszystkie")

### Korzyści z filtrowania:
- 📉 Mniej wizualnego bałaganu
- 🎯 Lepsza czytelność listy folderów
- ✅ Tylko istotne foldery dla wyszukiwania maili
- 🚀 Szybsze wykrywanie folderów (mniej folderów do przetworzenia)

---

**Data utworzenia**: 2025-10-09  
**Powiązane dokumenty**:
- `OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md` (szczegóły)
- `FOLDER_VISIBILITY_SUMMARY_EN.md` (podsumowanie)
