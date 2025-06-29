import os
import re
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.corpus import wordnet
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Download WordNet data if not already present
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    logger.info("Downloading WordNet corpus...")
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

def sanitize_input(word):
    """
    Sanitize user input to prevent injection attacks and ensure valid word format.
    Only allows alphabetic characters, hyphens, and apostrophes.
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
        
    return cleaned.lower()

def get_synonyms(word):
    """
    Get synonyms for a given word using WordNet.
    Returns a list of unique synonyms.
    """
    synonyms = set()
    
    try:
        # Get all synsets (synonym sets) for the word
        synsets = wordnet.synsets(word)
        
        for syn in synsets:
            # Get all lemmas (word forms) for each synset
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                # Don't include the original word
                if synonym.lower() != word.lower():
                    synonyms.add(synonym)
    
    except Exception as e:
        logger.error(f"Error getting synonyms for '{word}': {e}")
        return []
    
    # Convert to sorted list for consistent output
    return sorted(list(synonyms))

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
    try:
        data = request.get_json()
        if not data or 'word' not in data:
            return jsonify({'error': 'No word provided'}), 400
        
        word = sanitize_input(data['word'])
        if not word:
            return jsonify({'error': 'Invalid word format'}), 400
        
        synonyms = get_synonyms(word)
        
        return jsonify({
            'word': word,
            'synonyms': synonyms,
            'count': len(synonyms)
        })
    
    except Exception as e:
        logger.error(f"API error: {e}")
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
