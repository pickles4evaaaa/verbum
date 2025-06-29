# Verbum -- ## ✨ Features

- **🎨 Clean Interface**: Minimalist design focused on functionality
- **📚 WordNet Integration**: Uses the comprehensive WordNet lexical database
- **📖 Word Definitions**: Shows clear definitions along with synonyms
- **☁️ Word Cloud Background**: Animated background showing previously searched words
- **🛡️ Content Filtering**: Blocks inappropriate language and spam
- **🔒 Security First**: Input validation and sanitization to prevent vulnerabilities
- **📱 Responsive Design**: Works beautifully on desktop and mobile
- **🏠 Self-Hosted**: Run it on your own server with complete control
- **⚡ Fast & Lightweight**: Quick synonym lookups with minimal resource usagen Interface**: Minimalist design focused on functionality
- **📚 WordNet Integration**: Uses the comprehensive WordNet lexical database
- **📖 Word Definitions**: Shows clear definitions along with synonyms
- **☁️ Word Cloud Background**: Animated background showing previously searched words
- **🔒 Security First**: Input validation and sanitization to prevent vulnerabilitiesf-Hosted Thesaurus App

A sleek, minimalist thesaurus application powered by WordNet that provides synonyms for any word you search. Built with security and simplicity in mind.

![Verbum Interface](https://img.shields.io/badge/Interface-Sleek%20%26%20Modern-blue)
![Security](https://img.shields.io/badge/Security-Hardened-green)
![WordNet](https://img.shields.io/badge/Powered%20by-WordNet-orange)

## ✨ Features

- **🎨 Clean Interface**: Minimalist design focused on functionality
- **📚 WordNet Integration**: Uses the comprehensive WordNet lexical database
- **� Word Definitions**: Shows clear definitions along with synonyms
- **�🔒 Security First**: Input validation and sanitization to prevent vulnerabilities
- **📱 Responsive Design**: Works beautifully on desktop and mobile
- **🏠 Self-Hosted**: Run it on your own server with complete control
- **⚡ Fast & Lightweight**: Quick synonym lookups with minimal resource usage

## 🔐 Security Features

- **Input Sanitization**: Prevents XSS and injection attacks
- **Configurable Profanity Filter**: Optional content filtering (can be disabled)
- **Character Filtering**: Only allows letters, hyphens, and apostrophes
- **Length Limitations**: Prevents resource exhaustion attacks
- **HTML Escaping**: Frontend protection against script injection
- **Rate Limiting**: Through proper input validation
- **No Database**: Uses read-only WordNet corpus (no SQL injection risk)
- **Smart Word Cloud**: Only saves words with successful dictionary lookups

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/pickles4evaaaa/verbum.git
   cd verbum
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup WordNet Data**
   ```bash
   python setup.py
   ```

4. **Run Tests**
   ```bash
   python test.py
   ```

5. **Start the Application**
   ```bash
   python app.py
   ```

6. **Access the App**
   Open your browser to `http://localhost:5020`

## 🐳 Docker Deployment

For containerized deployment:

```bash
# Clone the repository first
git clone https://github.com/pickles4evaaaa/verbum.git
cd verbum

# Build and run with Docker Compose
docker-compose up --build

# Or with Docker directly
docker build -t verbum .
docker run -p 5020:5020 verbum
```

## 🌐 Production Deployment

For production use, use the included deployment script:

```bash
./deploy.sh
```

Or manually with Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5020 app:app
```

## ⚙️ Configuration

Environment variables you can set:

- `PORT`: Port to run the application (default: `5020`)
- `HOST`: Host to bind to (default: `127.0.0.1`)
- `ENABLE_PROFANITY_FILTER`: Enable/disable content filtering (default: `true`)

### Content Filtering

The profanity filter can be controlled via environment variable:

```bash
# Enable profanity filter (default)
ENABLE_PROFANITY_FILTER=true python app.py

# Disable profanity filter
ENABLE_PROFANITY_FILTER=false python app.py
```

When **enabled**: Blocks inappropriate language from being processed
When **disabled**: All words pass through sanitization (but only dictionary words with synonyms get saved to word cloud)

## 📡 API Usage

The app provides a simple REST API:

**POST** `/api/synonyms`
```json
{
  "word": "example"
}
```

**Response:**
```json
{
  "word": "example",
  "definition": "an item of information that is typical of a class or group",
  "synonyms": ["instance", "case", "illustration", "sample"],
  "count": 4
}
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test.py
```

Tests cover:
- Input sanitization
- Synonym lookup functionality  
- Security validation
- Malicious input protection

## 🛠️ Technology Stack

- **Backend**: Python Flask (lightweight and secure)
- **NLP**: NLTK with WordNet corpus (comprehensive synonym database)
- **Frontend**: Vanilla JavaScript with modern CSS (no dependencies)
- **Security**: Multi-layer input validation and sanitization
- **Deployment**: Docker, Gunicorn, or standalone Flask

## 📁 Project Structure

```
verbum/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Frontend interface with word cloud
├── requirements.txt    # Python dependencies
├── setup.py           # Setup script for WordNet data
├── test.py            # Comprehensive test suite
├── deploy.sh          # Production deployment script
├── search_history.json # Word search history (auto-generated)
├── Dockerfile         # Container configuration
├── docker-compose.yml # Container orchestration
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🔍 Usage Examples

Try searching for these words to see Verbum in action:

- **happy** → glad, joyful, cheerful, content
- **big** → large, huge, enormous, massive  
- **smart** → intelligent, clever, bright, wise
- **beautiful** → lovely, gorgeous, stunning, attractive

## 🤝 Contributing

1. Fork the repository from https://github.com/pickles4evaaaa/verbum
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/verbum.git`
3. Create a feature branch: `git checkout -b feature-name`
4. Make your changes
5. Run tests: `python test.py`
6. Commit and push: `git commit -m "Add feature" && git push origin feature-name`
7. Submit a pull request

## 📄 License

MIT License - feel free to use this for any purpose.

## 🙏 Acknowledgments

- **WordNet**: Princeton University's lexical database
- **NLTK**: Natural Language Toolkit for Python
- **Flask**: Lightweight Python web framework

---

*Built with ❤️ for word enthusiasts and developers who value clean, secure code.*
