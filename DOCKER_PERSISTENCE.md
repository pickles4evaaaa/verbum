# Docker Data Persistence Guide

This guide explains how Verbum handles persistent data storage in Docker deployments.

## Overview

Verbum saves search history and word cloud data to maintain state across sessions. In Docker environments, this data needs to be persisted outside the container to survive restarts and updates.

## How It Works

### File Location
- **Container Path**: `/app/data/search_history.json`
- **Volume Name**: `verbum_data`
- **Local Development**: `./data/search_history.json`

### Docker Volume Management

#### Automatic (Recommended)
When using Docker Compose, volumes are managed automatically:

```bash
# Start with persistent storage
docker-compose up -d

# Stop without losing data
docker-compose down

# Update and restart (data persists)
docker-compose pull && docker-compose up -d
```

#### Manual Volume Management

```bash
# Create volume manually
docker volume create verbum_data

# Run with volume attached
docker run -d \
  --name verbum \
  -p 5020:5020 \
  -v verbum_data:/app/data \
  verbum:latest

# Inspect volume contents
docker volume inspect verbum_data

# Backup volume data
docker run --rm \
  -v verbum_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/verbum_backup.tar.gz -C /data .

# Restore volume data
docker run --rm \
  -v verbum_data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/verbum_backup.tar.gz"
```

## Data Structure

The persistent data includes:

```json
{
  "words": {
    "happy": 5,
    "joyful": 3,
    "amazing": 2
  },
  "last_cleanup": 1751228421.903594,
  "updated": 1751228422.8882828
}
```

- **words**: Search frequency for each word
- **last_cleanup**: Timestamp of last data pruning
- **updated**: Last modification timestamp

## Environment Configuration

Control where data is stored:

```bash
# Default Docker location
SEARCH_HISTORY_DIR=/app/data

# Custom location (if needed)
SEARCH_HISTORY_DIR=/custom/path
```

## Volume Location on Host

Docker stores volumes in different locations depending on your system:

- **Linux**: `/var/lib/docker/volumes/verbum_verbum_data/_data/`
- **macOS**: `~/Library/Containers/com.docker.docker/Data/vms/0/data/docker/volumes/verbum_verbum_data/_data/`
- **Windows**: `C:\Users\[username]\AppData\Local\Docker\wsl\data\ext4.vhdx`

## Troubleshooting

### Volume Not Found
```bash
# List all volumes
docker volume ls

# Create missing volume
docker volume create verbum_data
```

### Permission Issues
```bash
# Fix permissions (Linux/macOS)
docker run --rm -v verbum_data:/data alpine chown -R 1000:1000 /data
```

### Data Recovery
```bash
# Access volume data directly
docker run --rm -it -v verbum_data:/data alpine sh
cd /data && ls -la
```

### Clean Slate
```bash
# Remove all data (destructive!)
docker-compose down -v
docker volume rm verbum_verbum_data
```

## Best Practices

1. **Regular Backups**: Use the backup commands above
2. **Monitor Size**: Verbum auto-prunes to top 100 words
3. **Environment Separation**: Use different volumes for dev/prod
4. **Volume Naming**: Use descriptive names for multiple instances

```bash
# Production volume
docker-compose -p verbum-prod up -d

# Development volume  
docker-compose -p verbum-dev up -d
```

This ensures your word cloud and search history persist beautifully across all Docker operations!
