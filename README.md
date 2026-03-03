# YouTube Video Downloader

A simple local web application to download YouTube videos in various qualities.

## Features
- Download YouTube videos as MP4
- Select video quality (360p, 480p, 720p, 1080p - based on availability)
- Clean and modern UI
- Video preview with thumbnail
- Downloads directly to your PC's Downloads folder

## Requirements
- Python 3.7+
- FFmpeg (for merging high-quality video and audio)

## Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

**Windows:**
```bash
winget install ffmpeg
```

Or download from: https://ffmpeg.org/download.html

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 3. (Optional) For Higher Quality Downloads

To download videos above 360p, you need to export YouTube cookies:

1. Install "Get cookies.txt LOCALLY" extension in your browser
2. Go to YouTube.com
3. Click the extension and export cookies
4. Save the `cookies.txt` file in the project folder

Without cookies, you can still download 360p quality.

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and go to:
```
http://localhost:5000
```

3. Paste a YouTube video URL

4. Click "Get Video Info"

5. Select your preferred quality

6. Click "Download Video"

7. Video will be saved to your Downloads folder

## How It Works

- YouTube stores high-quality videos (720p+) as separate video and audio streams
- FFmpeg automatically merges them into a single MP4 file
- Without FFmpeg, only 360p is available (comes with audio pre-merged)
- Cookies help bypass YouTube's bot detection for higher quality access

## Troubleshooting

**"Failed to fetch video info"**
- YouTube may be blocking the request
- Try adding cookies.txt (see step 3 in Installation)
- Update yt-dlp: `pip install --upgrade yt-dlp`

**"Only 360p available"**
- This is normal without cookies.txt
- YouTube restricts higher qualities without authentication

**"FFmpeg not found"**
- Make sure FFmpeg is installed and in your system PATH
- Restart your terminal after installation

## Notes

- This is for personal use only
- Respect copyright and YouTube's Terms of Service
- Downloaded videos are saved in your system's Downloads folder
- The app runs locally on your computer (not accessible from internet)

## Project Structure

```
├── app.py              # Flask backend server
├── index.html          # Main web interface
├── script.js           # Frontend JavaScript
├── style.css           # UI styling
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License

For personal use only. Respect content creators and YouTube's Terms of Service.
