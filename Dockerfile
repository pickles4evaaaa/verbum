FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (including bundled WordNet data)
COPY . .

# No need to run setup.py anymore - WordNet data is bundled

# Create data directory for persistent storage
RUN mkdir -p /app/data

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 5020

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5020/ || exit 1

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5020", "--timeout", "30", "app:app"]
