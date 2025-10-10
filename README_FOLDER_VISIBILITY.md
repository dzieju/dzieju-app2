# README: Dokumentacja widoczności folderów

## 🎯 Szybki start

Dokumentacja odpowiadająca na issue: **"Wyświetlanie zbyt wielu folderów na koncie poczty – opis widocznych typów folderów"**

### 📖 Zacznij tutaj:

**👉 [FOLDER_VISIBILITY_INDEX.md](FOLDER_VISIBILITY_INDEX.md)** - główny punkt wejścia z nawigacją i podsumowaniem

---

## 📚 Wszystkie dokumenty:

| Dokument | Rozmiar | Opis | Dla kogo |
|----------|---------|------|----------|
| **[FOLDER_VISIBILITY_INDEX.md](FOLDER_VISIBILITY_INDEX.md)** | 8.7KB | 📋 Spis treści i nawigacja | Wszyscy |
| **[OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md](OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md)** | 15KB | 📖 Pełna analiza (polski) | Team/eksperci |
| **[FOLDER_VISIBILITY_SUMMARY_EN.md](FOLDER_VISIBILITY_SUMMARY_EN.md)** | 4.2KB | 📝 Podsumowanie (angielski) | Deweloperzy |
| **[FOLDER_STRUCTURE_DIAGRAM.md](FOLDER_STRUCTURE_DIAGRAM.md)** | 8.4KB | 🎨 Diagramy wizualne | Wszyscy |

**Łącznie:** 36.3 KB, 1,030 linii dokumentacji

---

## ⚡ Szybkie odpowiedzi:

### Czy program prawidłowo wyświetla foldery?
**✅ TAK** - z jednym wyjątkiem (patrz niżej)

### Co działa dobrze?
- ✅ Wszystkie foldery systemowe (Inbox, Sent, Drafts, Trash, Spam, Outbox, Archive)
- ✅ Wszystkie foldery użytkownika (pełna hierarchia)
- ✅ Czytelna struktura drzewa z ikonami

### Jaki jest problem?
**⚠️ Exchange wyświetla foldery techniczne:**
- Calendar, Contacts, Tasks, Notes, Journal
- Te foldery **NIE zawierają maili**
- Powodują niepotrzebny bałagan w liście

### Jak to naprawić?
💡 **Filtrować po `folder_class`** - pokazać tylko foldery z mailami (`IPF.Note`)

Szczegóły: [OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md - Sekcja 6](OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md#6-potencjalne-problemy-i-propozycje-usprawnień)

---

## 🎓 Ścieżki czytania:

### 5 minut - podstawy:
1. Ten plik (README)
2. [FOLDER_STRUCTURE_DIAGRAM.md](FOLDER_STRUCTURE_DIAGRAM.md) - diagramy

### 15 minut - szczegóły:
1. [FOLDER_VISIBILITY_INDEX.md](FOLDER_VISIBILITY_INDEX.md)
2. [FOLDER_VISIBILITY_SUMMARY_EN.md](FOLDER_VISIBILITY_SUMMARY_EN.md)

### 30+ minut - pełna analiza:
1. [OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md](OPIS_TYPOW_FOLDEROW_WIDOCZNYCH.md)
2. Kod źródłowy w `gui/exchange_search_components/mail_connection.py`

---

## 📊 Podsumowanie odpowiedzi na pytania z issue:

| Pytanie | Odpowiedź |
|---------|-----------|
| Czy wyświetlane są foldery systemowe? | ✅ TAK |
| Czy widoczne są foldery ukryte? | ⚠️ Częściowo (techniczne Exchange) |
| Czy prezentowane są foldery użytkownika? | ✅ TAK |
| Czy wyświetlane są subfoldery? | ✅ TAK |
| Jak wygląda hierarchia? | ✅ Czytelna |

---

## 🔧 Następne kroki:

### Dla użytkownika:
1. Przeczytaj dokumentację aby zrozumieć, które foldery są widoczne
2. Użyj funkcji "Wyklucz te foldery:" aby ukryć niepotrzebne foldery

### Dla dewelopera:
1. Przejrzyj propozycje w sekcji 6 głównego dokumentu
2. Rozważ implementację filtrowania po `folder_class`
3. Opcjonalnie: dodaj checkbox "Tylko foldery z wiadomościami"

---

## 📞 Informacje:

**Issue:** "Wyświetlanie zbyt wielu folderów na koncie poczty"  
**Branch:** `copilot/clarify-mail-folder-types`  
**Status:** ✅ Dokumentacja kompletna  
**Data:** 2025-10-09  

**Utworzone przez:** Copilot AI Assistant  
**Co-authored-by:** dzieju <11342285+dzieju@users.noreply.github.com>

---

## 🎉 Dokumentacja gotowa!

Wszystkie pytania z issue zostały szczegółowo opisane i udokumentowane. Problem został zidentyfikowany i zaproponowano rozwiązanie.

**Zacznij od:** [FOLDER_VISIBILITY_INDEX.md](FOLDER_VISIBILITY_INDEX.md)
