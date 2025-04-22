from flask import Flask, request, send_file, jsonify, render_template
import os
import tempfile
import zipfile
import subprocess
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = None  # Remove file size limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_videos():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    zip_file = request.files['file']
    if not zip_file or not zip_file.filename.endswith('.zip'):
        return jsonify({'error': 'Invalid file type'}), 400

    temp_dir = tempfile.mkdtemp()
    logger.debug(f"Created temporary directory: {temp_dir}")
    zip_path = os.path.join(temp_dir, 'uploaded.zip')
    zip_file.save(zip_path)

    # Extract zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
        logger.debug(f"Extracted files to: {temp_dir}")
        logger.debug(f"Extracted files: {zip_ref.namelist()}")

    # Find and sort all .mp4 files chronologically
    mp4_files = []
    for root, dirs, files in os.walk(temp_dir):
        logger.debug(f"Walking directory: {root}")
        logger.debug(f"Found directories: {dirs}")
        logger.debug(f"Found files: {files}")
        for file in files:
            if file.endswith('.mp4'):
                full_path = os.path.join(root, file)
                logger.debug(f"Found MP4 file: {full_path}")
                # Extract date and time from path
                rel_path = os.path.relpath(full_path, temp_dir)
                logger.debug(f"Relative path: {rel_path}")
                parts = rel_path.split(os.sep)
                logger.debug(f"Path parts: {parts}")
                
                # The path structure is: 20250417-small/13/06.mp4
                # parts[0] = "20250417-small"
                # parts[1] = hour
                # parts[2] = minute.mp4
                if len(parts) >= 3:
                    try:
                        # Extract date from the first part (remove '-small' if present)
                        date_str = parts[0].split('-')[0]  # Get "20250417" from "20250417-small"
                        hour_str = parts[1]  # Hour
                        minute_str = parts[2].split('.')[0]  # Remove .mp4 from minute
                        timestamp = datetime.strptime(f"{date_str} {hour_str}:{minute_str}", "%Y%m%d %H:%M")
                        logger.debug(f"Parsed timestamp: {timestamp}")
                        mp4_files.append((timestamp, full_path))
                    except ValueError as e:
                        logger.error(f"Error parsing timestamp: {e}")
                        # If parsing fails, use the path as is
                        mp4_files.append((datetime.min, full_path))

    logger.debug(f"Total MP4 files found: {len(mp4_files)}")
    if not mp4_files:
        return jsonify({'error': 'No .mp4 files found'}), 400

    # Sort by timestamp
    mp4_files.sort(key=lambda x: x[0])
    sorted_paths = [path for _, path in mp4_files]
    logger.debug(f"Sorted paths: {sorted_paths}")

    # Create filelist.txt
    filelist_path = os.path.join(temp_dir, 'filelist.txt')
    with open(filelist_path, 'w', encoding='utf-8') as f:
        for path in sorted_paths:
            f.write(f"file '{path}'\n")
    logger.debug(f"Created filelist at: {filelist_path}")

    # Output file
    output_path = os.path.join(temp_dir, f'merged_{uuid.uuid4()}.mp4')

    # Run ffmpeg
    subprocess.run([
        'ffmpeg', '-f', 'concat', '-safe', '0',
        '-i', filelist_path, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', output_path
    ], check=True)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
