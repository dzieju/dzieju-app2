"""
Test suite for folder detection logic
Tests both IMAP and Exchange folder detection
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.imap_search_components.folder_browser import FolderInfo as IMAPFolderInfo
from gui.exchange_search_components.folder_browser import FolderInfo as ExchangeFolderInfo


class TestIMAPFolderDetection(unittest.TestCase):
    """Test IMAP folder detection logic"""
    
    def test_inbox_detection_with_flag(self):
        """Test inbox detection with SPECIAL-USE flag"""
        folder = IMAPFolderInfo(
            name="INBOX",
            display_name="INBOX",
            flags=['\\Inbox']
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')
    
    def test_inbox_detection_polish_name(self):
        """Test inbox detection with Polish name"""
        folder = IMAPFolderInfo(
            name="Odebrane",
            display_name="Odebrane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')
    
    def test_inbox_detection_hierarchical_path(self):
        """Test inbox detection with hierarchical path"""
        folder = IMAPFolderInfo(
            name="recepcja@woox.pl/Odebrane",
            display_name="recepcja@woox.pl/Odebrane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')
    
    def test_sent_detection_polish_wyslane(self):
        """Test sent folder detection with Polish name 'Wyslane'"""
        folder = IMAPFolderInfo(
            name="Wyslane",
            display_name="Wyslane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'sent')
        self.assertEqual(folder.icon, '📤')
        self.assertEqual(folder.get_display_name_polish(), 'Wysłane')
    
    def test_sent_detection_polish_wysłane(self):
        """Test sent folder detection with Polish name 'Wysłane' (with diacritic)"""
        folder = IMAPFolderInfo(
            name="Wysłane",
            display_name="Wysłane",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'sent')
        self.assertEqual(folder.icon, '📤')
        self.assertEqual(folder.get_display_name_polish(), 'Wysłane')
    
    def test_sent_detection_sent_items(self):
        """Test sent folder detection with 'Sent Items' name"""
        folder = IMAPFolderInfo(
            name="Sent Items",
            display_name="Sent Items",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'sent')
        self.assertEqual(folder.icon, '📤')
        self.assertEqual(folder.get_display_name_polish(), 'Wysłane')
    
    def test_drafts_detection_polish(self):
        """Test drafts folder detection with Polish name"""
        folder = IMAPFolderInfo(
            name="Szkice",
            display_name="Szkice",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'drafts')
        self.assertEqual(folder.icon, '📝')
        self.assertEqual(folder.get_display_name_polish(), 'Szkice')
    
    def test_trash_detection_polish(self):
        """Test trash folder detection with Polish name"""
        folder = IMAPFolderInfo(
            name="Kosz",
            display_name="Kosz",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'trash')
        self.assertEqual(folder.icon, '🗑️')
        self.assertEqual(folder.get_display_name_polish(), 'Kosz')
    
    def test_archive_detection_polish(self):
        """Test archive folder detection with Polish name"""
        folder = IMAPFolderInfo(
            name="Archiwum",
            display_name="Archiwum",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'archive')
        self.assertEqual(folder.icon, '📦')
        self.assertEqual(folder.get_display_name_polish(), 'Archiwum')
    
    def test_spam_detection_english(self):
        """Test spam folder detection with English name"""
        folder = IMAPFolderInfo(
            name="Spam",
            display_name="Spam",
            flags=[]
        )
        self.assertEqual(folder.is_special, 'spam')
        self.assertEqual(folder.icon, '⚠️')
        self.assertEqual(folder.get_display_name_polish(), 'Spam')
    
    def test_custom_folder_detection(self):
        """Test that custom folders are not detected as special"""
        folder = IMAPFolderInfo(
            name="Projects",
            display_name="Projects",
            flags=[]
        )
        self.assertIsNone(folder.is_special)
        self.assertEqual(folder.icon, '📁')
        self.assertEqual(folder.get_display_name_polish(), 'Projects')
    
    def test_flag_based_detection_without_name_match(self):
        """Test detection based on flags when name doesn't match"""
        folder = IMAPFolderInfo(
            name="CustomInbox",
            display_name="CustomInbox",
            flags=['\\Inbox']
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
    
    def test_size_formatting_bytes(self):
        """Test size formatting for bytes"""
        folder = IMAPFolderInfo(
            name="Test",
            display_name="Test",
            size=512
        )
        self.assertEqual(folder.format_size(), "512 B")
    
    def test_size_formatting_kb(self):
        """Test size formatting for kilobytes"""
        folder = IMAPFolderInfo(
            name="Test",
            display_name="Test",
            size=1024 * 150
        )
        self.assertEqual(folder.format_size(), "150.0 KB")
    
    def test_size_formatting_mb(self):
        """Test size formatting for megabytes"""
        folder = IMAPFolderInfo(
            name="Test",
            display_name="Test",
            size=1024 * 1024 * 48.8
        )
        formatted = folder.format_size()
        self.assertTrue(formatted.startswith("48."))
        self.assertTrue(formatted.endswith(" MB"))
    
    def test_size_formatting_gb(self):
        """Test size formatting for gigabytes"""
        folder = IMAPFolderInfo(
            name="Test",
            display_name="Test",
            size=1024 * 1024 * 1024 * 6.1
        )
        formatted = folder.format_size()
        self.assertTrue(formatted.startswith("6."))
        self.assertTrue(formatted.endswith(" GB"))
    
    def test_size_formatting_zero(self):
        """Test size formatting for zero size"""
        folder = IMAPFolderInfo(
            name="Test",
            display_name="Test",
            size=0
        )
        self.assertEqual(folder.format_size(), "0 B")


class TestExchangeFolderDetection(unittest.TestCase):
    """Test Exchange folder detection logic (should work same as IMAP)"""
    
    def test_inbox_detection_with_flag(self):
        """Test inbox detection with Exchange flag"""
        folder = ExchangeFolderInfo(
            name="Inbox",
            display_name="Inbox",
            flags=['\\Inbox']
        )
        self.assertEqual(folder.is_special, 'inbox')
        self.assertEqual(folder.icon, '📥')
        self.assertEqual(folder.get_display_name_polish(), 'Odebrane')
    
    def test_sent_items_detection(self):
        """Test Sent Items detection (Exchange standard name)"""
        folder = ExchangeFolderInfo(
            name="Sent Items",
            display_name="Sent Items",
            flags=['\\Sent']
        )
        self.assertEqual(folder.is_special, 'sent')
        self.assertEqual(folder.icon, '📤')
        self.assertEqual(folder.get_display_name_polish(), 'Wysłane')
    
    def test_drafts_detection(self):
        """Test Drafts detection"""
        folder = ExchangeFolderInfo(
            name="Drafts",
            display_name="Drafts",
            flags=['\\Drafts']
        )
        self.assertEqual(folder.is_special, 'drafts')
        self.assertEqual(folder.icon, '📝')
        self.assertEqual(folder.get_display_name_polish(), 'Szkice')
    
    def test_deleted_items_detection(self):
        """Test Deleted Items detection (Exchange standard name)"""
        folder = ExchangeFolderInfo(
            name="Deleted Items",
            display_name="Deleted Items",
            flags=['\\Trash']
        )
        self.assertEqual(folder.is_special, 'trash')
        self.assertEqual(folder.icon, '🗑️')
        self.assertEqual(folder.get_display_name_polish(), 'Kosz')


if __name__ == '__main__':
    unittest.main()
