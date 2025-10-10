"""
Test suite to verify that Exchange folder search covers ALL folders, not just subfolders
of a specific path.

This test validates the fix for the issue where Exchange search only searched subfolders
of the specified folder_path (e.g., only Inbox subfolders), missing other important
folders like Sent Items, Drafts, Archive, etc.
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MockExchangeFolder:
    """Mock Exchange folder object"""
    def __init__(self, name, children=None):
        self.name = name
        self._children = children or []
    
    @property
    def children(self):
        return self._children


class MockExchangeAccount:
    """Mock Exchange account object"""
    def __init__(self, root_folder, inbox, sent=None, drafts=None, trash=None, junk=None):
        self.root = root_folder
        self.inbox = inbox
        self.sent = sent
        self.drafts = drafts
        self.trash = trash
        self.junk = junk


class TestExchangeFolderSearchCoverage(unittest.TestCase):
    """Test that Exchange search covers all folders"""
    
    def setUp(self):
        """Set up mock Exchange folder structure"""
        # Create a typical Exchange folder structure
        # Root
        #  ├── Inbox
        #  │   ├── Archive (subfolder of Inbox)
        #  │   └── Projects (subfolder of Inbox)
        #  ├── Sent Items (at root level)
        #  ├── Drafts (at root level)
        #  ├── Deleted Items (at root level)
        #  └── Custom Folder (at root level)
        
        self.inbox_archive = MockExchangeFolder("Archive")
        self.inbox_projects = MockExchangeFolder("Projects")
        self.inbox = MockExchangeFolder("Inbox", [self.inbox_archive, self.inbox_projects])
        
        self.sent_items = MockExchangeFolder("Sent Items")
        self.drafts = MockExchangeFolder("Drafts")
        self.deleted_items = MockExchangeFolder("Deleted Items")
        self.custom_folder = MockExchangeFolder("Custom Folder")
        
        self.root = MockExchangeFolder("Root", [
            self.inbox,
            self.sent_items,
            self.drafts,
            self.deleted_items,
            self.custom_folder
        ])
        
        self.account = MockExchangeAccount(
            root_folder=self.root,
            inbox=self.inbox,
            sent=self.sent_items,
            drafts=self.drafts,
            trash=self.deleted_items,
            junk=None
        )
    
    def test_exchange_search_covers_all_folders(self):
        """Test that Exchange search returns ALL folders, not just subfolders of specified path"""
        # Mock dependencies before import
        sys.modules['imapclient'] = Mock()
        sys.modules['exchangelib'] = Mock()
        sys.modules['tools.logger'] = Mock()
        sys.modules['tkinter'] = Mock()
        
        # Create mock log function
        mock_log = Mock()
        sys.modules['tools.logger'].log = mock_log
        
        from gui.exchange_search_components.mail_connection import MailConnection
        
        connection = MailConnection()
        connection.current_account_config = {"type": "exchange"}
        
        # Call the method that should search ALL folders
        # The folder_path parameter should be ignored now
        folders = connection._get_exchange_folder_with_subfolders(
            self.account, 
            "Inbox",  # This parameter should be ignored
            excluded_folders=None
        )
        
        # Extract folder names for easier assertion
        folder_names = [f.name for f in folders]
        
        # Verify that ALL folders are included, not just Inbox and its subfolders
        self.assertIn("Root", folder_names, "Root folder should be included")
        self.assertIn("Inbox", folder_names, "Inbox should be included")
        self.assertIn("Archive", folder_names, "Inbox subfolder should be included")
        self.assertIn("Projects", folder_names, "Inbox subfolder should be included")
        self.assertIn("Sent Items", folder_names, "Sent Items (root level) should be included")
        self.assertIn("Drafts", folder_names, "Drafts (root level) should be included")
        self.assertIn("Deleted Items", folder_names, "Deleted Items (root level) should be included")
        self.assertIn("Custom Folder", folder_names, "Custom folders (root level) should be included")
        
        # Verify we got all expected folders
        self.assertGreaterEqual(len(folders), 7, "Should have at least 7 folders (Root + all subfolders)")
        
        print(f"✓ Test passed: Found {len(folders)} folders including all root-level folders")
        print(f"  Folders: {', '.join(folder_names)}")
    
    def test_exchange_search_with_exclusions(self):
        """Test that excluded folders are properly excluded from search"""
        # Mock dependencies before import
        sys.modules['imapclient'] = Mock()
        sys.modules['exchangelib'] = Mock()
        sys.modules['tools.logger'] = Mock()
        sys.modules['tkinter'] = Mock()
        
        from gui.exchange_search_components.mail_connection import MailConnection
        
        connection = MailConnection()
        connection.current_account_config = {"type": "exchange"}
        
        # Exclude some folders
        folders = connection._get_exchange_folder_with_subfolders(
            self.account,
            "Inbox",
            excluded_folders="Drafts, Archive"
        )
        
        folder_names = [f.name for f in folders]
        
        # Verify excluded folders are not in the list
        self.assertNotIn("Drafts", folder_names, "Drafts should be excluded")
        self.assertNotIn("Archive", folder_names, "Archive should be excluded")
        
        # Verify other folders are still included
        self.assertIn("Inbox", folder_names, "Inbox should still be included")
        self.assertIn("Sent Items", folder_names, "Sent Items should still be included")
        self.assertIn("Projects", folder_names, "Non-excluded subfolder should still be included")
        
        print(f"✓ Test passed: Exclusions work correctly, {len(folders)} folders after excluding 2")
        print(f"  Folders: {', '.join(folder_names)}")
    
    def test_mail_search_components_version(self):
        """Test that mail_search_components version also covers all folders"""
        # Mock dependencies before import
        sys.modules['imapclient'] = Mock()
        sys.modules['exchangelib'] = Mock()
        sys.modules['tools.logger'] = Mock()
        sys.modules['tkinter'] = Mock()
        
        from gui.mail_search_components.mail_connection import MailConnection
        
        connection = MailConnection()
        connection.current_account_config = {"type": "exchange"}
        
        folders = connection._get_exchange_folder_with_subfolders(
            self.account,
            "Inbox",
            excluded_folders=None
        )
        
        folder_names = [f.name for f in folders]
        
        # Verify comprehensive coverage
        self.assertIn("Sent Items", folder_names, "Sent Items should be included in mail_search_components version")
        self.assertIn("Drafts", folder_names, "Drafts should be included in mail_search_components version")
        self.assertIn("Deleted Items", folder_names, "Deleted Items should be included in mail_search_components version")
        
        self.assertGreaterEqual(len(folders), 7, "Should have comprehensive folder coverage")
        
        print(f"✓ Test passed: mail_search_components version also covers all folders ({len(folders)} folders)")


class TestExchangeFolderSearchFallback(unittest.TestCase):
    """Test fallback behavior when root access fails"""
    
    def test_fallback_to_inbox_parent(self):
        """Test that search falls back to inbox.parent if root access fails"""
        # Mock dependencies before import
        sys.modules['imapclient'] = Mock()
        sys.modules['exchangelib'] = Mock()
        sys.modules['tools.logger'] = Mock()
        sys.modules['tkinter'] = Mock()
        
        from gui.exchange_search_components.mail_connection import MailConnection
        
        # Create account with no root access
        inbox = MockExchangeFolder("Inbox")
        inbox_parent = MockExchangeFolder("Top of Information Store", [inbox])
        inbox.parent = inbox_parent
        
        account = Mock()
        account.root = None  # Simulate root access failure
        account.inbox = inbox
        account.sent = None
        account.drafts = None
        account.trash = None
        account.junk = None
        
        # Mock the root property to raise exception
        type(account).root = property(lambda self: (_ for _ in ()).throw(Exception("Root not accessible")))
        
        connection = MailConnection()
        connection.current_account_config = {"type": "exchange"}
        
        # Should not crash, should use inbox.parent fallback
        folders = connection._get_exchange_folder_with_subfolders(account, "Inbox", None)
        
        # Should have at least inbox from fallback
        self.assertGreaterEqual(len(folders), 1, "Should have at least 1 folder from fallback")
        
        print(f"✓ Test passed: Fallback mechanism works correctly")


if __name__ == '__main__':
    unittest.main(verbosity=2)
