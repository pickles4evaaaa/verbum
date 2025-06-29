#!/usr/bin/env python3
"""
Demo script showing the profanity filter toggle functionality.
Run this to see how the filter behaves when enabled vs disabled.
"""

import os
import sys

def test_word_with_filter_setting(enable_filter):
    """Test a word with the profanity filter enabled or disabled."""
    
    # Set environment variable
    os.environ['ENABLE_PROFANITY_FILTER'] = str(enable_filter).lower()
    
    # Import after setting env var (this determines filter behavior)
    from app import sanitize_input, ENABLE_PROFANITY_FILTER
    
    test_word = "shit"  # A word that would be flagged by profanity filter
    result = sanitize_input(test_word)
    
    print(f"ENABLE_PROFANITY_FILTER = {ENABLE_PROFANITY_FILTER}")
    print(f"Input: '{test_word}' → Output: {result}")
    
    return result

if __name__ == '__main__':
    print("🔬 Profanity Filter Toggle Demo")
    print("=" * 40)
    
    print("\n1️⃣ Testing with profanity filter ENABLED:")
    result_enabled = test_word_with_filter_setting(True)
    
    print("\n2️⃣ Testing with profanity filter DISABLED:")
    result_disabled = test_word_with_filter_setting(False)
    
    print("\n📊 Summary:")
    print(f"Filter ENABLED:  Input blocked = {result_enabled is None}")
    print(f"Filter DISABLED: Input allowed = {result_disabled is not None}")
    
    print("\n💡 Use ENABLE_PROFANITY_FILTER environment variable to control this behavior!")
