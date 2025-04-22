# Video Merge Tool

A simple web application that allows you to merge multiple MP4 videos from a ZIP file into a single video file. The tool automatically sorts the videos chronologically based on their directory structure and merges them using FFmpeg.

## Features

- Web-based interface with drag-and-drop support
- Automatic chronological sorting of videos
- Supports ZIP files containing MP4 videos
- Maintains video quality while converting audio to AAC
- No file size limits
- Simple and intuitive user interface

## Prerequisites

- Python 3.x
- FFmpeg installed on your system
- Required Python packages (see Requirements section)

## Installation

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

## Usage

1. Start the application:
```bash
python app.py
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
