# YouTube Video Downloader

A simple web platform to download YouTube videos in various qualities.

## Features
- Download YouTube videos as MP4
- Select video quality (720p, 1080p, etc.)
- Clean and modern UI
- Video preview with thumbnail

## Setup

1. Install FFmpeg (required for merging video and audio):
   - Windows: Download from https://ffmpeg.org/download.html or use `choco install ffmpeg`
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask backend:
```bash
python app.py
```

3. Open `index.html` in your browser or serve it with a local server:
```bash
python -m http.server 8000
```

Then visit: http://localhost:8000

## Usage

1. Paste a YouTube video URL
2. Click "Get Video Info"
3. Select your preferred quality
4. Click "Download Video"
5. Video will be saved in the `downloads` folder

## Note
Downloaded videos are saved in the `downloads` folder in your project directory.
