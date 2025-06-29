import os
import re
import json
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.corpus import wordnet
import logging
import time
from threading import Lock
from better_profanity import profanity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize profanity filter based on environment setting
ENABLE_PROFANITY_FILTER = os.environ.get('ENABLE_PROFANITY_FILTER', 'true').lower() == 'true'
if ENABLE_PROFANITY_FILTER:
    profanity.load_censor_words()
    logger.info("Profanity filter enabled")
else:
    logger.info("Profanity filter disabled")

# File-based storage for word search history
SEARCH_HISTORY_DIR = os.environ.get('SEARCH_HISTORY_DIR', './data')
SEARCH_HISTORY_FILE = os.path.join(SEARCH_HISTORY_DIR, 'search_history.json')
search_history_lock = Lock()

# Ensure data directory exists
os.makedirs(SEARCH_HISTORY_DIR, exist_ok=True)

def load_search_history():
    """Load search history from JSON file."""
    try:
        if os.path.exists(SEARCH_HISTORY_FILE):
            with open(SEARCH_HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('words', {}), data.get('last_cleanup', time.time())
        return {}, time.time()
    except Exception as e:
        logger.error(f"Error loading search history: {e}")
        return {}, time.time()

def save_search_history(words, last_cleanup):
    """Save search history to JSON file."""
    try:
        with search_history_lock:
            data = {
                'words': words,
                'last_cleanup': last_cleanup,
                'updated': time.time()
            }
            with open(SEARCH_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving search history: {e}")

# Initialize search history
search_history, last_cleanup = load_search_history()

# Download WordNet data if not already present
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    logger.info("Downloading WordNet corpus...")
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

def sanitize_input(word):
    """
    Sanitize user input to prevent injection attacks, profanity, and ensure valid word format.
    Only allows alphabetic characters, hyphens, and apostrophes.
    Blocks inappropriate language and content.
    """
    if not word or not isinstance(word, str):
        return None
    
    # Remove any non-alphabetic characters except hyphens and apostrophes
    # This prevents SQL injection, XSS, and other attacks
    cleaned = re.sub(r"[^a-zA-Z\-']", "", word.strip())
    
    # Limit length to prevent resource exhaustion
    if len(cleaned) > 50:
        return None
    
    # Ensure it's not empty after cleaning
    if not cleaned:
        return None
    
    # Check for profanity and inappropriate content (if filter is enabled)
    if ENABLE_PROFANITY_FILTER and profanity.contains_profanity(cleaned):
        return None
        
    return cleaned.lower()

def get_synonyms(word):
    """
    Get synonyms and definition for a given word using WordNet.
    Returns a dictionary with synonyms list and definition.
    """
    synonyms = set()
    definition = ""
    
    try:
        # Get all synsets (synonym sets) for the word
        synsets = wordnet.synsets(word)
        
        if synsets:
            # Get the definition from the first synset (most common meaning)
            definition = synsets[0].definition()
        
        for syn in synsets:
            # Get all lemmas (word forms) for each synset
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                # Don't include the original word
                if synonym.lower() != word.lower():
                    synonyms.add(synonym)
    
    except Exception as e:
        logger.error(f"Error getting synonyms for '{word}': {e}")
        return {"synonyms": [], "definition": ""}
    
    # Convert to sorted list for consistent output
    return {
        "synonyms": sorted(list(synonyms)),
        "definition": definition
    }

@app.route('/')
def index():
    """Serve the main thesaurus interface."""
    return render_template('index.html')

@app.route('/api/synonyms', methods=['POST'])
def api_synonyms():
    """
    API endpoint to get synonyms for a word.
    Expects JSON with 'word' field.
    """
    global search_history, last_cleanup
    
    try:
        data = request.get_json()
        if not data or 'word' not in data:
            return jsonify({'error': 'No word provided'}), 400
        
        original_word = data['word']
        word = sanitize_input(original_word)
        
        if not word:
            # Check if it was rejected due to profanity (only if filter is enabled)
            if ENABLE_PROFANITY_FILTER and original_word and isinstance(original_word, str):
                cleaned_for_check = re.sub(r"[^a-zA-Z\-']", "", original_word.strip())
                if cleaned_for_check and profanity.contains_profanity(cleaned_for_check):
                    return jsonify({'error': 'Inappropriate content not allowed'}), 400
            return jsonify({'error': 'Invalid word format'}), 400
        
        result = get_synonyms(word)
        
        # Only track search history for words that have synonyms or definitions
        # This prevents spam and inappropriate content from being saved
        if result['synonyms'] or result['definition']:
            # Track search history
            search_history[word] = search_history.get(word, 0) + 1
            
            # Cleanup old entries periodically (keep only top 100)
            current_time = time.time()
            if current_time - last_cleanup > 300:  # Every 5 minutes
                if len(search_history) > 100:
                    # Keep only top 100 most searched words
                    sorted_words = sorted(search_history.items(), key=lambda x: x[1], reverse=True)
                    search_history = dict(sorted_words[:100])
                last_cleanup = current_time
                save_search_history(search_history, last_cleanup)
            else:
                # Save after each search for persistence
                save_search_history(search_history, last_cleanup)
        
        return jsonify({
            'word': word,
            'synonyms': result['synonyms'],
            'definition': result['definition'],
            'count': len(result['synonyms'])
        })
    
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/wordcloud', methods=['GET'])
def api_wordcloud():
    """
    API endpoint to get word cloud data.
    Returns list of words with their search frequencies.
    """
    try:
        # Return top 50 words for word cloud
        sorted_words = sorted(search_history.items(), key=lambda x: x[1], reverse=True)
        top_words = sorted_words[:50]
        
        return jsonify({
            'words': [{'text': word, 'weight': count} for word, count in top_words],
            'total_searches': sum(search_history.values()),
            'unique_words': len(search_history)
        })
    except Exception as e:
        logger.error(f"Word cloud API error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Use environment variables for configuration
    port = int(os.environ.get('PORT', 5020))
    host = os.environ.get('HOST', '127.0.0.1')
    
    # Import and run with Gunicorn for production security
    try:
        from gunicorn.app.wsgiapp import WSGIApplication
        
        class StandaloneApplication(WSGIApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
            
            def load_config(self):
                for key, value in self.options.items():
                    if key in self.cfg.settings and value is not None:
                        self.cfg.set(key.lower(), value)
            
            def load(self):
                return self.application
        
        options = {
            'bind': f'{host}:{port}',
            'workers': 4,
            'timeout': 30,
            'keepalive': 2,
            'max_requests': 1000,
            'max_requests_jitter': 100,
            'worker_class': 'sync'
        }
        
        logger.info(f"Starting Gunicorn server on {host}:{port}")
        StandaloneApplication(app, options).run()
        
    except ImportError:
        logger.warning("Gunicorn not available, falling back to Flask development server")
        app.run(host=host, port=port, debug=False)
