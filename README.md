# Video Merge Tool

A simple web application that allows you to merge multiple MP4 videos from a ZIP file into a single video file. The tool automatically sorts the videos chronologically based on their directory structure and merges them using FFmpeg.

## Features

- Web-based interface with drag-and-drop support
- Automatic chronological sorting of videos
- Supports ZIP files containing MP4 videos
- Maintains video quality while converting audio to AAC
- No file size limits
- Simple and intuitive user interface
- Docker support for easy deployment

## Prerequisites

- Python 3.x
- FFmpeg installed on your system
- Required Python packages (see Requirements section)

## Installation

### Option 1: Local Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/video-merge-tool.git
cd video-merge-tool
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Ensure FFmpeg is installed on your system:
```bash
# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On macOS
brew install ffmpeg

# On Windows
# Download from https://ffmpeg.org/download.html
```

### Option 2: Docker Installation

The application is available as a Docker image from Docker Hub:

```bash
docker pull kbaillie/wyze-cam-video-merge-tool:latest
```

#### Running with Docker

1. Basic usage (using default temp directory):
```bash
docker run -p 5000:5000 kbaillie/wyze-cam-video-merge-tool:latest
```

2. Using a custom temp directory (mounted from host):
```bash
docker run -p 5000:5000 \
  -v /path/on/host:/custom/temp \
  -e TEMP_DIR=/custom/temp \
  kbaillie/wyze-cam-video-merge-tool:latest
```

3. Using a Docker volume:
```bash
docker run -p 5000:5000 \
  -v wyze-temp:/custom/temp \
  -e TEMP_DIR=/custom/temp \
  kbaillie/wyze-cam-video-merge-tool:latest
```

#### Docker Compose

You can also use Docker Compose for easier deployment. Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  wyze-cam-video-merge:
    image: kbaillie/wyze-cam-video-merge-tool:latest
    ports:
      - "5000:5000"
    volumes:
      - wyze-temp:/custom/temp
    environment:
      - TEMP_DIR=/custom/temp
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

volumes:
  wyze-temp:
```

Then run:
```bash
docker-compose up -d
```

#### Environment Variables

- `TEMP_DIR`: Specify a custom directory for temporary files (default: `/tmp/wyze-cam-video-merge`)
- `PYTHONUNBUFFERED`: Set to 1 to ensure logs are not buffered (default: 1)

## Usage

1. Start the application:
```bash
# For local installation
python app.py

# For Docker installation
docker run -p 5000:5000 kbaillie/wyze-cam-video-merge-tool:latest
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Prepare your videos:
   - Organize your MP4 files in a directory structure like: `YYYYMMDD/HH/MM.mp4`
   - Example: `20250417/13/06.mp4` represents April 17, 2025, 13:06
   - Create a ZIP file containing these directories

4. Upload your ZIP file:
   - Click the upload area or drag and drop your ZIP file
   - The tool will automatically sort and merge the videos

5. Download the merged video:
   - After processing, the merged video will automatically download
   - The output file will be named with a unique identifier

## Directory Structure

The tool expects your ZIP file to have the following structure:
```
YYYYMMDD/
├── HH/
│   ├── MM.mp4
│   ├── MM.mp4
│   └── ...
└── ...
```

Example:
```
20250417/
├── 13/
│   ├── 06.mp4
│   ├── 07.mp4
│   └── ...
└── 14/
    ├── 00.mp4
    ├── 01.mp4
    └── ...
```

## Requirements

- Flask==3.0.2
- Werkzeug==3.0.1

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
