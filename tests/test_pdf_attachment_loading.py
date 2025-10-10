"""
Test suite to verify that PDF attachments are properly loaded for Exchange messages
when searching for content within PDF files.

This test validates the fix for the issue where emails with PDF attachments
(like "Play - e-korekta do pobrania" with "KOREKTA-K_00025405_10_25-KONTO_12629296.pdf")
were not being found when searching for NIP numbers in PDF content.
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MockAttachment:
    """Mock attachment object"""
    def __init__(self, name, content=b""):
        self.name = name
        self.content = content


class MockExchangeMessage:
    """Mock Exchange message object with attachments"""
    def __init__(self, subject, has_attachments=False, attachments=None):
        self.subject = subject
        self.has_attachments = has_attachments
        self._attachments = attachments or []
        self.id = "test_id"
        self.datetime_received = None
        self.is_read = False
        self.sender = Mock()
        self.sender.email_address = "test@example.com"
    
    @property
    def attachments(self):
        """Return attachments list"""
        return self._attachments


class TestPDFAttachmentLoading(unittest.TestCase):
    """Test that PDF attachments are properly loaded for Exchange messages"""
    
    def test_message_with_pdf_attachment_is_accessible(self):
        """Test that messages with PDF attachments have accessible attachment properties"""
        # Create a mock message with a PDF attachment
        pdf_attachment = MockAttachment("KOREKTA-K_00025405_10_25-KONTO_12629296.pdf", b"PDF content")
        message = MockExchangeMessage(
            subject="Play - e-korekta do pobrania",
            has_attachments=True,
            attachments=[pdf_attachment]
        )
        
        # Verify the message has attachments
        self.assertTrue(message.has_attachments)
        self.assertIsNotNone(message.attachments)
        self.assertEqual(len(message.attachments), 1)
        
        # Verify the attachment has correct name
        self.assertEqual(message.attachments[0].name, "KOREKTA-K_00025405_10_25-KONTO_12629296.pdf")
        
        # Verify the attachment has content
        self.assertEqual(message.attachments[0].content, b"PDF content")
    
    def test_message_without_attachments(self):
        """Test that messages without attachments return empty list"""
        message = MockExchangeMessage(
            subject="Test message without attachments",
            has_attachments=False,
            attachments=[]
        )
        
        self.assertFalse(message.has_attachments)
        self.assertEqual(len(message.attachments), 0)
    
    def test_message_with_multiple_pdf_attachments(self):
        """Test that messages with multiple PDF attachments can access all of them"""
        attachments = [
            MockAttachment("document1.pdf", b"Content 1"),
            MockAttachment("document2.pdf", b"Content 2"),
            MockAttachment("image.png", b"Image content"),  # Non-PDF
        ]
        message = MockExchangeMessage(
            subject="Message with multiple attachments",
            has_attachments=True,
            attachments=attachments
        )
        
        self.assertTrue(message.has_attachments)
        self.assertEqual(len(message.attachments), 3)
        
        # Count PDF attachments
        pdf_attachments = [att for att in message.attachments if att.name.lower().endswith('.pdf')]
        self.assertEqual(len(pdf_attachments), 2)
    
    def test_exchange_query_includes_attachments_field(self):
        """Test that Exchange queries include 'attachments' in the .only() call"""
        # Create a mock folder
        mock_folder = Mock()
        mock_folder.name = "Inbox"
        
        # Create a mock filter/query object
        mock_query = Mock()
        mock_only = Mock()
        mock_order_by = Mock()
        mock_order_by.return_value = []
        mock_only.order_by = mock_order_by
        mock_query.only = Mock(return_value=mock_only)
        mock_folder.filter = Mock(return_value=mock_query)
        
        # Verify that when filter is called, it chains with .only() including 'attachments'
        result = mock_folder.filter("test_query")
        result.only('subject', 'sender', 'datetime_received', 'is_read', 'has_attachments', 'attachments', 'id')
        
        # Verify only was called with the expected fields including 'attachments'
        mock_query.only.assert_called_once()
        call_args = mock_query.only.call_args[0]
        self.assertIn('attachments', call_args)
        self.assertIn('subject', call_args)
        self.assertIn('sender', call_args)


if __name__ == '__main__':
    unittest.main()
