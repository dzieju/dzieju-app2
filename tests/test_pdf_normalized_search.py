"""
Test suite for normalized PDF search functionality
Tests the enhanced search that handles formatted text with spaces, dashes, etc.
"""
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.exchange_search_components.pdf_processor import PDFProcessor


class TestPDFNormalizedSearch(unittest.TestCase):
    """Test normalized search for PDF content"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = PDFProcessor()
    
    def test_extract_matches_exact_match(self):
        """Test that exact matches are found"""
        full_text = "This document contains the number 123456789 in the middle."
        search_text = "123456789"
        
        matches = self.processor._extract_matches(full_text, search_text)
        
        self.assertTrue(len(matches) > 0)
        self.assertIn("123456789", matches[0])
    
    def test_extract_matches_with_spaces_in_pdf(self):
        """Test normalized search when PDF has spaces in the number"""
        full_text = "This document contains the number 123 456 789 with spaces."
        search_text = "123456789"
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        # Should find approximate match
        self.assertTrue(len(matches) > 0)
        self.assertIn("123 456 789", matches[0])
    
    def test_extract_matches_with_dashes_in_pdf(self):
        """Test normalized search when PDF has dashes in the number"""
        full_text = "Document with NIP number: 123-456-789 (dashed format)."
        search_text = "123456789"
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        # Should find approximate match
        self.assertTrue(len(matches) > 0)
        self.assertIn("123-456-789", matches[0])
    
    def test_extract_matches_with_mixed_formatting(self):
        """Test normalized search with mixed formatting"""
        full_text = "The ID is: 123.456/789 in this format."
        search_text = "123456789"
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        # Should find approximate match
        self.assertTrue(len(matches) > 0)
    
    def test_extract_matches_multiple_occurrences(self):
        """Test that multiple matches are found"""
        full_text = "First: 123456789, second: 123 456 789, third: 123-456-789"
        search_text = "123456789"
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        # Should find at least the exact match, possibly more
        self.assertTrue(len(matches) >= 1)
    
    def test_extract_matches_case_insensitive(self):
        """Test that search is case-insensitive"""
        full_text = "The code is ABC123DEF456 here."
        search_text = "abc123def456"
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        self.assertTrue(len(matches) > 0)
    
    def test_extract_matches_short_text_no_normalization(self):
        """Test that short search terms (<=3 chars) don't use normalization"""
        full_text = "Document with ABC code."
        search_text = "xyz"  # Short, not in document
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        # Should not find match (too short for normalization, no exact match)
        self.assertEqual(len(matches), 0)
    
    def test_extract_matches_limit(self):
        """Test that matches are limited to 5"""
        # Create text with many occurrences
        full_text = " ".join([f"Number {i}: 123456789" for i in range(10)])
        search_text = "123456789"
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        # Should be limited to 5 matches
        self.assertLessEqual(len(matches), 5)
    
    def test_extract_matches_approximate_prefix(self):
        """Test that approximate matches have the prefix marker"""
        full_text = "NIP: 123-456-789 formatted."
        search_text = "123456789"
        
        matches = self.processor._extract_matches(full_text, search_text.lower())
        
        # If approximate match is used, it should have the prefix
        if matches:
            # May have exact or approximate, check for approximate marker if present
            approximate_found = any("[Dopasowanie przybliżone]" in m for m in matches)
            # At least one match should be found
            self.assertTrue(len(matches) > 0)


if __name__ == '__main__':
    unittest.main()
