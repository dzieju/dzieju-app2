# Opis typów folderów widocznych w programie

## Cel dokumentu
Szczegółowy opis typów folderów wyświetlanych w programie dzieju-app2 w zakładkach Exchange i IMAP, wraz z analizą, które foldery są widoczne dla użytkownika i jakie kryteria decydują o ich wyświetlaniu.

---

## 1. Poczta Exchange (zakładka "Poczta Exchange")

### 1.1 Mechanizm wykrywania folderów

Program wykrywa foldery Exchange poprzez:
- **Punkt startowy**: katalog główny konta (`account.root` - "Top of Information Store")
- **Metoda**: rekurencyjne przeszukiwanie całego drzewa folderów
- **Algorytm**: głębokość-pierwsze (depth-first) rekurencyjne przechodzenie

### 1.2 Typy folderów widocznych

#### 1.2.1 Foldery systemowe Exchange
Program wyświetla **wszystkie** standardowe foldery systemowe Exchange:

| Nazwa angielska | Nazwa polska | Ikona | Opis |
|----------------|--------------|-------|------|
| **Inbox** | Odebrane | 📥 | Skrzynka odbiorcza - wiadomości przychodzące |
| **Sent Items** | Wysłane | 📤 | Wiadomości wysłane |
| **Drafts** | Szkice | 📝 | Wersje robocze wiadomości |
| **Deleted Items** | Kosz | 🗑️ | Elementy usunięte |
| **Junk Email** | Spam | ⚠️ | Wiadomości-śmieci, niechciana poczta |
| **Outbox** | Skrzynka nadawcza | 📮 | Wiadomości oczekujące na wysłanie |
| **Archive** | Archiwum | 📦 | Wiadomości zarchiwizowane |

**Źródło**: 
- Foldery wykrywane automatycznie przez traversal drzewa od korzenia
- Dodatkowo program próbuje dostępu do dobrze znanych folderów przez `account.sent`, `account.drafts`, `account.trash`, `account.junk`, `account.outbox`
- Fallback: jeśli foldery nie zostaną znalezione, dodawane są z listy standardowych folderów Exchange

**Kod źródłowy**: `gui/exchange_search_components/mail_connection.py`, metody:
- `_get_exchange_available_folders()` (linie 763-856)
- `_get_exchange_folders_with_details()` (linie 298-387)

#### 1.2.2 Foldery użytkownika (własne/niestandardowe)
Program wyświetla **wszystkie** foldery utworzone przez użytkownika:

- **Foldery główne**: foldery utworzone na poziomie głównym (root level)
  - Przykłady: "Projekty", "2024", "2023", "Faktury"
  
- **Subfoldery/zagnieżdżone**: foldery wewnątrz innych folderów
  - Przykłady: "Projekty/ProjectA", "Archiwum/2024", "Faktury/VAT"

**Hierarchia**: Program zachowuje i wyświetla pełną strukturę hierarchiczną folderów.

#### 1.2.3 Foldery techniczne/specjalne

Program **może wyświetlać** następujące foldery techniczne Exchange, jeśli istnieją w koncie:

| Nazwa folderu | Opis | Czy powinien być widoczny? |
|--------------|------|---------------------------|
| **Conversation History** | Historia konwersacji (Skype/Teams) | ⚠️ Techniczny - można ukryć |
| **Calendar** | Kalendarz | ⚠️ Nie dotyczy poczty - można ukryć |
| **Contacts** | Kontakty | ⚠️ Nie dotyczy poczty - można ukryć |
| **Tasks** | Zadania | ⚠️ Nie dotyczy poczty - można ukryć |
| **Notes** | Notatki | ⚠️ Nie dotyczy poczty - można ukryć |
| **Journal** | Dziennik | ⚠️ Nie dotyczy poczty - można ukryć |

**Uwaga**: Te foldery są wykrywane, ponieważ znajdują się w drzewie folderów Exchange, ale **nie zawierają wiadomości e-mail** - są to kontenery dla innych typów obiektów Exchange (wydarzenia kalendarza, kontakty, zadania).

### 1.3 Kryteria sortowania i wyświetlania

#### Kolejność wyświetlania:
1. **Najpierw**: Foldery systemowe (alfabetycznie w ramach tej grupy)
2. **Następnie**: Foldery użytkownika (alfabetycznie)

#### Wykrywanie folderów systemowych:
Program rozpoznaje folder jako systemowy jeśli jego nazwa (lowercase) zawiera którykolwiek z wzorców:
- `inbox`, `sent`, `draft`, `trash`, `deleted`, `junk`, `spam`, `outbox`, `archive`

#### Hierarchia w drzewie:
- Foldery systemowe zawsze wyświetlane są na poziomie głównym
- Foldery użytkownika wyświetlane są w hierarchii (z wcięciami dla subfolderów)
- Separator hierarchii: `/` (slash)

### 1.4 Foldery ukryte/niedostępne

Program **NIE wyświetla** następujących typów folderów:
- ❌ Foldery systemowe Exchange z flagą "Hidden"
- ❌ Foldery bez uprawnień dostępu dla użytkownika
- ❌ Foldery, które nie są dostępne przez API exchangelib

**Mechanizm wykluczenia**: 
- Użytkownik może ręcznie wykluczyć foldery poprzez pole "Wyklucz te foldery:" (oddzielone przecinkami)
- Wykluczone foldery NIE są przeszukiwane podczas wyszukiwania wiadomości

---

## 2. Poczta IMAP (zakładka "Poczta IMAP")

### 2.1 Mechanizm wykrywania folderów

Program wykrywa foldery IMAP poprzez:
- **Metoda**: `imap.list_folders()` - standardowe zapytanie IMAP LIST
- **Zwracane dane**: tupla (flags, delimiter, folder_name)

### 2.2 Typy folderów widocznych

#### 2.2.1 Foldery systemowe IMAP

Program wyświetla foldery systemowe wykryte na podstawie:
- **RFC 6154 SPECIAL-USE flags** (preferowane)
- **Analiza nazwy folderu** (fallback)

| Flaga RFC 6154 | Nazwa polska | Ikona | Możliwe nazwy serwerowe |
|---------------|--------------|-------|------------------------|
| `\Inbox` | Odebrane | 📥 | INBOX, Odebrane, Przychodzące |
| `\Sent` | Wysłane | 📤 | SENT, Sent Items, Wysłane, Wysłano |
| `\Drafts` | Szkice | 📝 | DRAFTS, Drafts, Szkice, Robocze |
| `\Trash` | Kosz | 🗑️ | TRASH, Deleted Items, Kosz, Śmieci |
| `\Junk` | Spam | ⚠️ | SPAM, Junk, Junk Email |
| `\Archive` | Archiwum | 📦 | ARCHIVE, Archiwum |

**Detekcja**: 
```python
# Kod: gui/imap_search_components/folder_browser.py, linie 23-47
def _detect_special_folder(self):
    # 1. Sprawdzenie flag SPECIAL-USE (RFC 6154)
    # 2. Jeśli brak flag - analiza nazwy folderu
    # 3. Rozpoznawanie nazw polskich i angielskich
```

#### 2.2.2 Foldery użytkownika IMAP

Program wyświetla **wszystkie** foldery utworzone przez użytkownika na serwerze IMAP:
- Foldery główne (root level)
- Subfoldery z pełną hierarchią
- Separator hierarchii: zazwyczaj `/` lub `.` (zależnie od serwera)

#### 2.2.3 Specyfika różnych serwerów IMAP

Program obsługuje różne konwencje nazewnictwa:

**Przykład 1: Gmail**
- Używa etykiet jako folderów
- Widoczne: "[Gmail]/Sent Mail", "[Gmail]/Trash", "[Gmail]/Spam"
- Hierarchia z prefiksem "[Gmail]/"

**Przykład 2: Dovecot/Courier**
- Separator: `.` (kropka)
- Hierarchia: "INBOX.Archive.2024"

**Przykład 3: Microsoft Exchange IMAP**
- Separator: `/` (slash)
- Prefiks emaila: "user@domain.com/Inbox"

### 2.3 Kryteria sortowania i wyświetlania

#### Kolejność wyświetlania:
1. **Najpierw**: Foldery systemowe (w predefinowanej kolejności: inbox, drafts, sent, spam, trash, archive)
2. **Następnie**: Foldery użytkownika (alfabetycznie)

#### Hierarchia w drzewie:
- Wykrywanie hierarchii na podstawie delimitera zwróconego przez serwer
- Wyświetlanie tylko ostatniej części nazwy dla subfolderów
- Przykład: folder "Archive/2024" wyświetlany jako "2024" (z wcięciem pod "Archive")

### 2.4 Foldery ukryte/specjalne IMAP

Program automatycznie **POMIJA** następujące foldery:

| Wzorzec | Opis | Powód pominięcia |
|---------|------|------------------|
| Puste nazwy | `""` | Nieprawidłowe |
| Aktualny folder wyszukiwania | Folder wskazany w polu "Folder" | Uniknięcie samo-wykluczenia |
| Foldery z flagą `\Noselect` | Foldery bez wiadomości | Tylko kontenery dla hierarchii |

---

## 3. Porównanie Exchange vs IMAP

| Aspekt | Exchange | IMAP |
|--------|----------|------|
| **Punkt startowy** | `account.root` (katalog główny) | `list_folders()` (wszystkie foldery) |
| **Detekcja systemowych** | Po nazwie + well-known folders | RFC 6154 flags + analiza nazwy |
| **Separator hierarchii** | `/` (slash) | Zależny od serwera (`.` lub `/`) |
| **Mapowanie nazw** | Angielski → Polski | Server → Polski |
| **Foldery techniczne** | Tak (Calendar, Contacts, etc.) | Nie |
| **Fallback foldery** | Standardowe foldery Exchange | Standardowe foldery IMAP |

---

## 4. Funkcjonalność wykluczania folderów

### 4.1 Mechanizm wykluczania

Użytkownik może wykluczyć foldery z przeszukiwania poprzez:
- **Pole tekstowe**: "Wyklucz te foldery:" (w sekcji Wyszukiwanie)
- **Format**: Nazwy folderów oddzielone przecinkami
- **Przykład**: `Archiwum, Spam, TEST`

### 4.2 Efekt wykluczenia

- Wykluczone foldery **NIE są przeszukiwane** podczas wyszukiwania wiadomości
- Wykluczone subfoldery **również są pomijane** (rekurencyjnie)
- Informacja o wykluczeniu jest logowana w konsoli

**Kod**: `gui/exchange_search_components/mail_connection.py`, metoda `_get_all_subfolders_recursive()` (linie 661-684)

---

## 5. Wyświetlanie w interfejsie użytkownika

### 5.1 Komponenty GUI

#### FolderBrowser (przeglądarki folderów)
- **Lokalizacja Exchange**: `gui/exchange_search_components/folder_browser.py`
- **Lokalizacja IMAP**: `gui/imap_search_components/folder_browser.py`

#### Struktura wyświetlania:
```
🌳 Treeview (drzewo folderów)
├── Kolumna 1: Nazwa folderu (z ikoną)
├── Kolumna 2: Liczba wiadomości
└── Kolumna 3: Szacowany rozmiar
```

### 5.2 Ikony folderów

| Ikona | Typ folderu | Kod Unicode |
|-------|-------------|-------------|
| 📥 | Inbox (Odebrane) | U+1F4E5 |
| 📤 | Sent (Wysłane) | U+1F4E4 |
| 📝 | Drafts (Szkice) | U+1F4DD |
| 🗑️ | Trash (Kosz) | U+1F5D1 |
| ⚠️ | Spam | U+26A0 |
| 📦 | Archive (Archiwum) | U+1F4E6 |
| 📮 | Outbox | U+1F4EE |
| 📁 | Folder niestandardowy | U+1F4C1 |

### 5.3 Informacje o folderze (double-click)

Po dwukrotnym kliknięciu folder wyświetla się dialog z informacjami:
- Nazwa wyświetlana (polska)
- Pełna ścieżka na serwerze
- Liczba wiadomości
- Szacowany rozmiar
- Typ: "Systemowy" lub "Własny"

**Kod**: `folder_browser.py`, metoda `on_folder_double_click()` (linie 319-343)

---

## 6. Potencjalne problemy i propozycje usprawnień

### 6.1 Zbyt wiele folderów - analiza

#### Problem zgłoszony:
> "Program wyświetla zbyt dużą liczbę folderów na koncie poczty"

#### Możliwe przyczyny:
1. **Foldery techniczne Exchange** - Calendar, Contacts, Tasks, Journal, Notes
   - **Nie powinny być widoczne** w kontekście wyszukiwania e-maili
   - Propozycja: Filtrowanie po `folder_class` (tylko `IPF.Note` dla maili)

2. **Subfoldery zagnieżdżone** - wszystkie poziomy hierarchii
   - **Są potrzebne** dla precyzyjnego wyszukiwania
   - Obecne zachowanie: **prawidłowe**

3. **Foldery historii/logów** - Conversation History, Sync Issues
   - **Można ukryć** domyślnie
   - Propozycja: Lista wykluczonych wzorców folderów

### 6.2 Propozycje filtrowania

#### Opcja A: Filtrowanie technicznych folderów Exchange
```python
# Dodać do _get_exchange_folders_with_details()
EXCLUDED_FOLDER_CLASSES = [
    'IPF.Appointment',  # Calendar
    'IPF.Contact',      # Contacts
    'IPF.Task',         # Tasks
    'IPF.Journal',      # Journal
    'IPF.Note',         # Notes
]

# Filtrować foldery, które nie są IPF.Note (mail folders)
if folder_class and folder_class not in ['IPF.Note', 'IPF.']:
    continue  # Skip non-mail folders
```

#### Opcja B: Lista domyślnie ukrytych folderów
```python
DEFAULT_HIDDEN_FOLDERS = [
    'Calendar',
    'Contacts', 
    'Tasks',
    'Notes',
    'Journal',
    'Conversation History',
    'Sync Issues',
]
```

#### Opcja C: Checkbox w GUI - "Pokaż tylko foldery z wiadomościami"
- Domyślnie: zaznaczony (ukrywa foldery techniczne)
- Odznaczony: pokazuje wszystko

### 6.3 Foldery ukryte/systemowe

#### Obecnie NIE wykrywane przez program:
- ❌ Foldery z flagą "Hidden" w Exchange
- ❌ Foldery systemowe Exchange niedostępne przez API
- ❌ Foldery z flagą `\Noselect` w IMAP (już implementowane)

#### Rekomendacja:
Program **prawidłowo** nie wyświetla folderów ukrytych przez serwer.

---

## 7. Podsumowanie odpowiedzi na pytania z issue

### ✅ Czy wyświetlane są foldery systemowe?
**TAK** - Wszystkie standardowe foldery systemowe:
- Exchange: Inbox, Sent Items, Drafts, Deleted Items, Junk Email, Outbox, Archive
- IMAP: INBOX, SENT, DRAFTS, TRASH, SPAM, ARCHIVE

### ⚠️ Czy widoczne są foldery ukryte/systemowe, które nie powinny być dostępne?
**CZĘŚCIOWO** - Exchange może pokazywać foldery techniczne:
- Calendar, Contacts, Tasks, Notes, Journal, Conversation History
- **Rekomendacja**: Dodać filtrowanie po `folder_class` dla Exchange

### ✅ Czy prezentowane są foldery użytkownika?
**TAK** - Wszystkie foldery utworzone przez użytkownika na wszystkich poziomach hierarchii.

### ✅ Czy wyświetlane są subfoldery?
**TAK** - Pełna hierarchia folderów z rekurencyjnym przeszukiwaniem.

### ✅ Jak wygląda hierarchia folderów?
**CZYTELNA** - Drzewo z wcięciami, ikony, sortowanie (systemowe → użytkownika).

### 📋 Czy wyświetlane są foldery archiwalne?
**TAK** - Foldery archiwum są wykrywane i wyświetlane jako systemowe.

### 📋 Czy wyświetlane są foldery techniczne?
**TAK (Exchange)** - Foldery takie jak Calendar, Contacts mogą być widoczne.
**NIE (IMAP)** - Brak takich folderów w protokole IMAP.

---

## 8. Rekomendacje dla dalszego rozwoju

### Priorytet wysoki:
1. ✅ **Filtrowanie folderów technicznych Exchange** po `folder_class`
   - Ukryć Calendar, Contacts, Tasks, Journal, Notes
   - Pokazać tylko foldery z mailami (`IPF.Note`)

2. ✅ **Dodać checkbox "Tylko foldery z wiadomościami"**
   - Domyślnie zaznaczony
   - Pozwala na wyłączenie filtra dla zaawansowanych użytkowników

### Priorytet średni:
3. ⚠️ **Lista domyślnie wykluczonych wzorców**
   - "Conversation History", "Sync Issues"
   - Edytowalna w konfiguracji

4. ⚠️ **Licznik w GUI**
   - "Wyświetlono X z Y folderów (Z ukrytych)"

### Priorytet niski:
5. ℹ️ **Tooltip z dodatkową informacją**
   - Wskazówki dla folderów systemowych
   - Ostrzeżenia dla folderów technicznych

---

## 9. Wnioski

### Aktualny stan:
- ✅ Program **prawidłowo** wykrywa i wyświetla foldery systemowe
- ✅ Program **prawidłowo** wykrywa i wyświetla foldery użytkownika
- ✅ Hierarchia folderów jest **czytelna** i **dobrze zorganizowana**
- ⚠️ Program **może wyświetlać zbyt wiele** folderów technicznych Exchange (Calendar, Contacts, etc.)

### Główny problem:
Foldery techniczne Exchange (Calendar, Contacts, Tasks, Journal, Notes) są wykrywane i wyświetlane, mimo że **nie zawierają wiadomości e-mail**.

### Rozwiązanie:
Dodać filtrowanie po `folder_class` w Exchange, aby wyświetlać tylko foldery z mailami (`IPF.Note`).

---

**Data utworzenia dokumentu**: 2025-10-09  
**Wersja programu**: dzieju-app2 (bieżąca wersja)  
**Autor analizy**: Copilot AI Assistant  
**Status**: ✅ Kompletna analiza i dokumentacja
