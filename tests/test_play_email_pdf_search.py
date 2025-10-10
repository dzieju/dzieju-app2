"""
Test for the specific case mentioned in the issue:
Email with subject "Play - e-korekta do pobrania"
Attachment "KOREKTA-K_00025405_10_25-KONTO_12629296.pdf"
Should be found when searching for NIP in the PDF content.

This test validates that the V1 and V2 fixes work correctly for this specific scenario.
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
    """Mock attachment object that mimics Exchange attachment"""
    def __init__(self, name, content):
        self.name = name
        self.content = content


class MockMessage:
    """Mock message object that mimics Exchange message"""
    def __init__(self, subject, has_attachments, attachments):
        self.subject = subject
        self.has_attachments = has_attachments
        self._attachments = attachments
        self.datetime_received = None
        self.sender = None
    
    @property
    def attachments(self):
        """Return attachments - mimics Exchange lazy loading"""
        return self._attachments


class TestPlayEmailPDFSearch(unittest.TestCase):
    """
    Test the specific case from the issue:
    - Subject: "Play - e-korekta do pobrania"
    - Attachment: "KOREKTA-K_00025405_10_25-KONTO_12629296.pdf"
    - Should be detected when searching for NIP in PDF
    """
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = EmailSearchEngine(
            progress_callback=lambda x: None,
            result_callback=lambda x: None
        )
    
    def test_play_email_with_pdf_attachment_is_processed(self):
        """
        Test that an email with subject "Play - e-korekta do pobrania"
        and PDF attachment is properly processed for search.
        
        This validates:
        1. has_attachments flag is checked correctly
        2. attachments list is properly evaluated
        3. PDF attachment is detected
        4. No early returns that would skip the search
        """
        # Create mock PDF attachment with the exact name from the issue
        pdf_attachment = MockAttachment(
            name="KOREKTA-K_00025405_10_25-KONTO_12629296.pdf",
            content=b"Mock PDF content with some data"
        )
        
        # Create mock message with the exact subject from the issue
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[pdf_attachment]
        )
        
        # Search for some text (NIP would be here in real scenario)
        result = self.search_engine._check_pdf_content(message, "test_search_text")
        
        # Should NOT return early with these error codes
        self.assertNotEqual(result['method'], 'no_attachments_flag', 
                           "Should not skip due to has_attachments=False")
        self.assertNotEqual(result['method'], 'attachments_not_loaded',
                           "Should not skip due to empty attachments list")
        self.assertNotEqual(result['method'], 'attachment_access_error',
                           "Should not skip due to attachment access error")
        
        # The method should be one of these valid processing states
        valid_methods = ['not_found_in_pdfs', 'missing_dependencies', 'text_extraction', 'ocr']
        self.assertIn(result['method'], valid_methods,
                     f"Method should be one of {valid_methods}, got: {result['method']}")
    
    def test_play_email_with_empty_attachments_despite_flag(self):
        """
        Test the bug scenario: has_attachments=True but attachments is empty
        This was the V2 fix - should be detected and logged
        """
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[]  # Empty despite flag being True
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should detect this inconsistency
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'attachments_not_loaded',
                        "Should detect and report when attachments aren't loaded despite flag")
    
    def test_play_email_with_none_attachments_despite_flag(self):
        """
        Test the bug scenario: has_attachments=True but attachments is None
        This was also part of the V2 fix
        """
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=None  # None despite flag being True
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should detect this inconsistency
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'attachments_not_loaded',
                        "Should detect and report when attachments is None despite flag")
    
    def test_play_email_without_attachments(self):
        """
        Test normal case: has_attachments=False, no search needed
        """
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=False,
            attachments=None
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should return early with no_attachments_flag
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'no_attachments_flag')
    
    def test_play_email_with_non_pdf_attachment(self):
        """
        Test that non-PDF attachments are skipped correctly
        """
        doc_attachment = MockAttachment(
            name="document.docx",
            content=b"Document content"
        )
        
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[doc_attachment]
        )
        
        result = self.search_engine._check_pdf_content(message, "5732475751")
        
        # Should process but not find (no PDF)
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'not_found_in_pdfs')
    
    def test_play_email_with_multiple_pdfs(self):
        """
        Test handling of multiple PDF attachments
        """
        pdf1 = MockAttachment(
            name="KOREKTA-K_00025405_10_25-KONTO_12629296.pdf",
            content=b"PDF 1 content"
        )
        pdf2 = MockAttachment(
            name="invoice.pdf",
            content=b"PDF 2 content"
        )
        
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[pdf1, pdf2]
        )
        
        result = self.search_engine._check_pdf_content(message, "test")
        
        # Should process without errors
        self.assertNotEqual(result['method'], 'attachments_not_loaded')
        self.assertNotEqual(result['method'], 'attachment_access_error')
    
    def test_empty_search_text_returns_early(self):
        """
        Test that empty search text causes early return before attachment processing
        """
        pdf_attachment = MockAttachment(
            name="KOREKTA-K_00025405_10_25-KONTO_12629296.pdf",
            content=b"PDF content"
        )
        
        message = MockMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[pdf_attachment]
        )
        
        result = self.search_engine._check_pdf_content(message, "")
        
        # Should return early with no_search_text
        self.assertFalse(result['found'])
        self.assertEqual(result['method'], 'no_search_text')


class TestExchangeQueryIncludesAttachments(unittest.TestCase):
    """
    Test that Exchange queries include 'attachments' field
    This validates the V1 fix
    """
    
    def test_only_method_includes_attachments_field(self):
        """
        Verify that the .only() method includes 'attachments' in the field list
        This is critical for the V1 fix to work
        """
        # Read the search_engine.py file to verify the fix is in place
        search_engine_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'gui', 
            'exchange_search_components', 
            'search_engine.py'
        )
        
        with open(search_engine_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that .only() calls include 'attachments'
        self.assertIn(".only(", content, 
                     "Exchange queries should use .only() method")
        
        # Check for the pattern: .only( ... 'attachments' ... )
        # This is a simplified check - the actual implementation has the full list
        only_calls = content.count(".only(")
        attachments_in_only = content.count("'attachments'")
        
        # There should be multiple .only() calls (we know there are at least 4)
        self.assertGreater(only_calls, 3, 
                          "Should have multiple .only() calls for different query paths")
        
        # There should be at least as many 'attachments' references as .only() calls
        # (actually more, but at least this many in the .only() calls)
        self.assertGreaterEqual(attachments_in_only, only_calls,
                               "Each .only() call should include 'attachments' field")


if __name__ == '__main__':
    unittest.main()
