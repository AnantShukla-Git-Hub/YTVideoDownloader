from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp
import os
import json
import tempfile

app = Flask(__name__, static_folder='.')
CORS(app)

# Use temporary folder for server-side downloads
TEMP_FOLDER = tempfile.gettempdir()

# Set FFmpeg path - check if running locally or on cloud
if os.path.exists(r'C:\Users\anant\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe'):
    FFMPEG_PATH = r'C:\Users\anant\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe'
else:
    FFMPEG_PATH = 'ffmpeg'  # Use system ffmpeg on cloud

# Common yt-dlp options to bypass restrictions
def get_ydl_opts(extra_opts=None):
    base_opts = {
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'ios'],
                'player_skip': ['webpage'],
            }
        },
    }
    
    # Only set ffmpeg if it exists
    if FFMPEG_PATH and os.path.exists(FFMPEG_PATH):
        base_opts['ffmpeg_location'] = FFMPEG_PATH
    
    # Check if cookies.txt exists and use it
    cookies_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    if os.path.exists(cookies_file):
        base_opts['cookiefile'] = cookies_file
    
    if extra_opts:
        base_opts.update(extra_opts)
    return base_opts

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

@app.route('/api/formats', methods=['POST'])
def get_formats():
    """Get available video formats for a YouTube URL"""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        ydl_opts = get_ydl_opts()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            seen_qualities = {}
            
            for f in info.get('formats', []):
                height = f.get('height')
                vcodec = f.get('vcodec', 'none')
                format_id = f.get('format_id')
                
                if height and vcodec != 'none' and height >= 144:
                    quality_label = f"{height}p"
                    
                    if quality_label not in seen_qualities:
                        seen_qualities[quality_label] = {
                            'format_id': format_id,
                            'quality': quality_label,
                            'ext': f.get('ext', 'mp4'),
                            'filesize': f.get('filesize', 0),
                            'fps': f.get('fps', 30),
                            'height': height
                        }
            
            formats = list(seen_qualities.values())
            formats.sort(key=lambda x: x['height'], reverse=True)
            
            for f in formats:
                del f['height']
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': formats
            })
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch video info: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video and send directly to browser"""
    if request.is_json:
        data = request.json
    else:
        data = request.form
    
    url = data.get('url')
    format_id = data.get('format_id', 'best')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        if format_id == 'best':
            format_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else:
            format_string = f'{format_id}+bestaudio/best'
        
        import time
        temp_filename = f"video_{int(time.time())}.mp4"
        temp_path = os.path.join(TEMP_FOLDER, temp_filename)
            
        extra_opts = {
            'format': format_string,
            'outtmpl': temp_path,
            'merge_output_format': 'mp4',
        }
        ydl_opts = get_ydl_opts(extra_opts)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            download_name = f"{safe_title}.mp4"
            
            if os.path.exists(temp_path):
                response = send_file(
                    temp_path,
                    as_attachment=True,
                    download_name=download_name,
                    mimetype='video/mp4'
                )
                
                import threading
                def cleanup():
                    import time
                    time.sleep(10)
                    try:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                    except:
                        pass
                
                threading.Thread(target=cleanup).start()
                return response
            else:
                return jsonify({'error': 'Download failed - file not found'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/api/file/<filename>', methods=['GET'])
def download_file(filename):
    """Send file to browser for download"""
    try:
        file_path = os.path.join(TEMP_FOLDER, filename)
        if os.path.exists(file_path):
            response = send_file(file_path, as_attachment=True, download_name=filename)
            
            import threading
            def cleanup():
                import time
                time.sleep(5)
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except:
                    pass
            
            threading.Thread(target=cleanup).start()
            return response
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\nYouTube Video Downloader")
    print(f"Running on port {port}\n")
    app.run(host='0.0.0.0', port=port, debug=False)
