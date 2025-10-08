"""
Test suite for folder detection logic (without GUI dependencies)
Tests the core detection logic without importing tkinter
"""
import unittest


class FolderInfoMock:
    """Mock FolderInfo class for testing detection logic"""
    
    def __init__(self, name, display_name, message_count=0, size=0, flags=None, delimiter='/'):
        self.name = name
        self.display_name = display_name
        self.message_count = message_count
        self.size = size
        self.flags = flags or []
        self.delimiter = delimiter
        self.is_special = self._detect_special_folder()
        self.icon = self._get_icon()
    
    def _detect_special_folder(self):
        """Detect if this is a special folder based on flags and name"""
        # Build flag string (empty if no flags)
        flag_str = ' '.join(str(f) for f in self.flags).upper() if self.flags else ''
        name_upper = self.name.upper()
        
        # Extract last part of folder path for better detection
        # e.g., "recepcja@woox.pl/Odebrane" -> "ODEBRANE"
        folder_basename = name_upper.split('/')[-1].split('.')[-1]
        
        # SPECIAL-USE flags (RFC 6154) OR name-based detection (English and Polish)
        if '\\INBOX' in flag_str or name_upper == 'INBOX' or folder_basename == 'ODEBRANE':
            return 'inbox'
        elif '\\SENT' in flag_str or 'SENT' in name_upper or folder_basename in ('WYSLANE', 'WYSŁANE', 'SENT ITEMS'):
            return 'sent'
        elif '\\DRAFTS' in flag_str or 'DRAFT' in name_upper or folder_basename == 'SZKICE':
            return 'drafts'
        elif '\\TRASH' in flag_str or 'TRASH' in name_upper or 'DELETED' in name_upper or folder_basename == 'KOSZ':
            return 'trash'
        elif '\\JUNK' in flag_str or 'SPAM' in name_upper or 'JUNK' in name_upper:
            return 'spam'
        elif '\\ARCHIVE' in flag_str or 'ARCHIVE' in name_upper or folder_basename == 'ARCHIWUM':
            return 'archive'
        
        return None
    
    def _get_icon(self):
        """Get icon/emoji for folder type"""
        if self.is_special == 'inbox':
            return '📥'
        elif self.is_special == 'sent':
            return '📤'
        elif self.is_special == 'drafts':
            return '📝'
        elif self.is_special == 'trash':
            return '🗑️'
        elif self.is_special == 'spam':
            return '⚠️'
        elif self.is_special == 'archive':
            return '📦'
        else:
            return '📁'
    
    def get_display_name_polish(self):
        """Get Polish display name for system folders"""
        if self.is_special == 'inbox':
            return 'Odebrane'
        elif self.is_special == 'sent':
            return 'Wysłane'
        elif self.is_special == 'drafts':
            return 'Szkice'
        elif self.is_special == 'trash':
            return 'Kosz'
        elif self.is_special == 'spam':
            return 'Spam'
        elif self.is_special == 'archive':
            return 'Archiwum'
        else:
            return self.display_name
    
    def format_size(self):
        """Format size in human-readable format"""
        if self.size == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(self.size)
        unit_index = 0
        
        while size >= 1024.0 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"


class TestFolderDetectionLogic(unittest.TestCase):
    """Test folder detection logic"""
    
    def test_inbox_detection_with_flag(self):
        """Test inbox detection with SPECIAL-USE flag"""
        folder = FolderInfoMock(
            name="INBOX",
            display_name="INBOX",
            flags=['\\Inbox']
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')
    
    def test_inbox_detection_polish_name(self):
        """Test inbox detection with Polish name"""
        folder = FolderInfoMock(
            name="Odebrane",
            display_name="Odebrane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')
    
    def test_inbox_detection_hierarchical_path(self):
        """Test inbox detection with hierarchical path"""
        folder = FolderInfoMock(
            name="recepcja@woox.pl/Odebrane",
            display_name="recepcja@woox.pl/Odebrane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')
    
    def test_sent_detection_polish_wyslane(self):
        """Test sent folder detection with Polish name 'Wyslane'"""
        folder = FolderInfoMock(
            name="Wyslane",
            display_name="Wyslane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'sent')
        self.assertEqual(folder.icon, '📤')
        self.assertEqual(folder.get_display_name_polish(), 'Wysłane')
    
    def test_sent_detection_polish_wysłane(self):
        """Test sent folder detection with Polish name 'Wysłane' (with diacritic)"""
        folder = FolderInfoMock(
            name="Wysłane",
            display_name="Wysłane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'sent')
        self.assertEqual(folder.icon, '📤')
        self.assertEqual(folder.get_display_name_polish(), 'Wysłane')
    
    def test_sent_detection_sent_items(self):
        """Test sent folder detection with 'Sent Items' name"""
        folder = FolderInfoMock(
            name="Sent Items",
            display_name="Sent Items",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'sent')
        self.assertEqual(folder.icon, '📤')
        self.assertEqual(folder.get_display_name_polish(), 'Wysłane')
    
    def test_drafts_detection_polish(self):
        """Test drafts folder detection with Polish name"""
        folder = FolderInfoMock(
            name="Szkice",
            display_name="Szkice",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'drafts')
        self.assertEqual(folder.icon, '📝')
        self.assertEqual(folder.get_display_name_polish(), 'Szkice')
    
    def test_trash_detection_polish(self):
        """Test trash folder detection with Polish name"""
        folder = FolderInfoMock(
            name="Kosz",
            display_name="Kosz",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'trash')
        self.assertEqual(folder.icon, '🗑️')
        self.assertEqual(folder.get_display_name_polish(), 'Kosz')
    
    def test_trash_detection_deleted_items(self):
        """Test trash detection with 'Deleted Items' name"""
        folder = FolderInfoMock(
            name="Deleted Items",
            display_name="Deleted Items",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'trash')
        self.assertEqual(folder.icon, '🗑️')
        self.assertEqual(folder.get_display_name_polish(), 'Kosz')
    
    def test_archive_detection_polish(self):
        """Test archive folder detection with Polish name"""
        folder = FolderInfoMock(
            name="Archiwum",
            display_name="Archiwum",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'archive')
        self.assertEqual(folder.icon, '📦')
        self.assertEqual(folder.get_display_name_polish(), 'Archiwum')
    
    def test_spam_detection_english(self):
        """Test spam folder detection with English name"""
        folder = FolderInfoMock(
            name="Spam",
            display_name="Spam",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'spam')
        self.assertEqual(folder.icon, '⚠️')
        self.assertEqual(folder.get_display_name_polish(), 'Spam')
    
    def test_spam_detection_junk(self):
        """Test spam folder detection with 'Junk' name"""
        folder = FolderInfoMock(
            name="Junk",
            display_name="Junk",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'spam')
        self.assertEqual(folder.icon, '⚠️')
        self.assertEqual(folder.get_display_name_polish(), 'Spam')
    
    def test_custom_folder_detection(self):
        """Test that custom folders are not detected as special"""
        folder = FolderInfoMock(
            name="Projects",
            display_name="Projects",
            flags=[]
        )
        self.assertIsNone(folder.is_special)
        self.assertEqual(folder.icon, '📁')
        self.assertEqual(folder.get_display_name_polish(), 'Projects')
    
    def test_flag_based_detection_without_name_match(self):
        """Test detection based on flags when name doesn't match"""
        folder = FolderInfoMock(
            name="CustomInbox",
            display_name="CustomInbox",
            flags=['\\Inbox']
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
    
    def test_size_formatting_bytes(self):
        """Test size formatting for bytes"""
        folder = FolderInfoMock(
            name="Test",
            display_name="Test",
            size=512
        )
        self.assertEqual(folder.format_size(), "512 B")
    
    def test_size_formatting_kb(self):
        """Test size formatting for kilobytes"""
        folder = FolderInfoMock(
            name="Test",
            display_name="Test",
            size=1024 * 150
        )
        self.assertEqual(folder.format_size(), "150.0 KB")
    
    def test_size_formatting_mb(self):
        """Test size formatting for megabytes"""
        folder = FolderInfoMock(
            name="Test",
            display_name="Test",
            size=int(1024 * 1024 * 48.8)
        )
        formatted = folder.format_size()
        self.assertTrue(formatted.startswith("48."))
        self.assertTrue(formatted.endswith(" MB"))
    
    def test_size_formatting_gb(self):
        """Test size formatting for gigabytes"""
        folder = FolderInfoMock(
            name="Test",
            display_name="Test",
            size=int(1024 * 1024 * 1024 * 6.1)
        )
        formatted = folder.format_size()
        self.assertTrue(formatted.startswith("6."))
        self.assertTrue(formatted.endswith(" GB"))
    
    def test_size_formatting_zero(self):
        """Test size formatting for zero size"""
        folder = FolderInfoMock(
            name="Test",
            display_name="Test",
            size=0
        )
        self.assertEqual(folder.format_size(), "0 B")
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive"""
        folder_lower = FolderInfoMock(name="inbox", display_name="inbox", flags=[])
        folder_upper = FolderInfoMock(name="INBOX", display_name="INBOX", flags=[])
        folder_mixed = FolderInfoMock(name="InBox", display_name="InBox", flags=[])
        
        self.assertEqual(folder_lower.is_special, 'inbox')
        self.assertEqual(folder_upper.is_special, 'inbox')
        self.assertEqual(folder_mixed.is_special, 'inbox')
    
    def test_multiple_folder_path_levels(self):
        """Test detection with multiple path levels"""
        folder = FolderInfoMock(
            name="email@domain.com/subfolder/Odebrane",
            display_name="email@domain.com/subfolder/Odebrane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
