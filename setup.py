#!/usr/bin/env python3
"""
Setup script for Verbum Thesaurus App
D    print("Then open http://localhost:5020 in your browser.")wnloads required NLTK data and sets up the application.
"""

import nltk
import os

def setup_nltk():
    """Download required NLTK data."""
    print("Setting up NLTK data...")
    
    # Create NLTK data directory if it doesn't exist
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    if not os.path.exists(nltk_data_dir):
        os.makedirs(nltk_data_dir)
    
    # Download required corpora
    try:
        nltk.download('wordnet', quiet=False)
        nltk.download('omw-1.4', quiet=False)  # Open Multilingual Wordnet
        print("✓ NLTK data downloaded successfully!")
    except Exception as e:
        print(f"✗ Error downloading NLTK data: {e}")
        return False
    
    return True

def test_wordnet():
    """Test WordNet functionality."""
    print("Testing WordNet...")
    
    try:
        from nltk.corpus import wordnet
        
        # Test with a simple word
        synsets = wordnet.synsets('test')
        if synsets:
            print("✓ WordNet is working correctly!")
            return True
        else:
            print("✗ WordNet test failed - no synsets found")
            return False
    except Exception as e:
        print(f"✗ WordNet test failed: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Setting up Verbum Thesaurus App...")
    print("=" * 50)
    
    # Setup NLTK
    if not setup_nltk():
        print("Setup failed. Please check your internet connection and try again.")
        exit(1)
    
    # Test functionality
    if not test_wordnet():
        print("Setup completed but testing failed. The app may not work correctly.")
        exit(1)
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\nTo start the application, run:")
    print("    python app.py")
    print("\nThen open http://localhost:5000 in your browser.")
