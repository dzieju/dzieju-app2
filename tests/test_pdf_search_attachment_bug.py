"""
Test for PDF attachment search bug where has_attachments=True but attachments is empty/None
This tests the specific scenario reported in the issue.

This is a lightweight test that tests the logic without requiring full dependencies.
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock exchangelib before import
sys.modules['exchangelib'] = Mock()
sys.modules['exchangelib'].Q = Mock
sys.modules['exchangelib'].Message = Mock

# Mock IMAPClient
sys.modules['imapclient'] = Mock()
sys.modules['imapclient'].IMAPClient = Mock

from gui.exchange_search_components.search_engine import EmailSearchEngine


class MockAttachment:
    """Mock attachment object"""
    def __init__(self, name, content):
        self.name = name
        self.content = content


class MockMessage:
    """Mock message object that mimics Exchange message behavior"""
    def __init__(self, subject, has_attachments, attachments):
        self.subject = subject
        self.has_attachments = has_attachments
        self._attachments = attachments
        self.datetime_received = None
        self.sender = None
    
    @property
    def attachments(self):
        """Simulate lazy loading that can return None or empty list"""
        return self._attachments


class TestPDFSearchAttachmentBug(unittest.TestCase):
    """Test PDF search handles attachment access issues correctly"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = EmailSearchEngine(
            progress_callback=lambda x: None,
            result_callback=lambda x: None
        )
    
    def test_has_attachments_true_but_attachments_none(self):
        """
        Test the bug scenario: has_attachments=True but attachments property returns None
        This was the main issue causing PDF search to fail
        """
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=None  # Bug: attachments not loaded!
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should return proper error code instead of crashing
        self.assertFalse(result['found'])
        self.assertIn(result['method'], ['attachments_not_loaded', 'attachment_access_error'])
    
    def test_has_attachments_true_but_attachments_empty_list(self):
        """
        Test scenario: has_attachments=True but attachments is empty list
        Another manifestation of the same bug
        """
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[]  # Bug: empty list despite flag being True
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should detect this inconsistency and return appropriate error
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'attachments_not_loaded')
    
    def test_has_attachments_false_early_return(self):
        """
        Test that has_attachments=False causes early return without accessing attachments
        """
        message = MockMessage(
            subject="Test message",
            has_attachments=False,
            attachments=None  # Should not even be accessed
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'no_attachments_flag')
    
    def test_attachments_properly_loaded_with_pdf(self):
        """
        Test normal case: attachments properly loaded and contains PDF
        """
        pdf_attachment = MockAttachment(
            name="KOREKTA-K_00025405_10_25-KONTO_12629296.pdf",
            content=b"Mock PDF content with NIP 5732475751"
        )
        
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[pdf_attachment]
        )
        
        # Note: This test will fail because we don't have actual PDF processing
        # but it tests that we get to the PDF processor
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should not fail with attachment access error
        self.assertNotEqual(result['method'], 'attachment_access_error')
        self.assertNotEqual(result['method'], 'attachments_not_loaded')
    
    def test_attachments_exception_handling(self):
        """
        Test that exceptions during attachment access are handled gracefully
        """
        class BrokenAttachments:
            def __iter__(self):
                raise RuntimeError("Attachment access failed")
        
        message = MockMessage(
            subject="Test message",
            has_attachments=True,
            attachments=BrokenAttachments()
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should catch exception and return error
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'attachment_access_error')
        self.assertIn('error', result)
    
    def test_no_search_text_early_return(self):
        """
        Test that empty search text causes early return
        """
        message = MockMessage(
            subject="Test message",
            has_attachments=True,
            attachments=[MockAttachment("test.pdf", b"content")]
        )
        
        result = self.search_engine._check_pdf_content(message, "")
        
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'no_search_text')


if __name__ == '__main__':
    unittest.main()
