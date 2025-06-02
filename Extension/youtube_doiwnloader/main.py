import os
import logging
from typing import Optional
from pytube import YouTube
from pytube.exceptions import PytubeError
import yt_dlp
import sys
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeDownloader:
    """Simplified YouTube video downloader that saves to Downloads folder"""
    
    def __init__(self, url: str):
        self.url = url
        self.video_path: Optional[str] = None
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
    def download_video(self) -> str:
        """Main download method with fallback to yt-dlp"""
        try:
            return self._download_with_pytube()
        except Exception as pytube_error:
            logger.warning(f"PyTube failed: {pytube_error}. Trying yt-dlp...")
            try:
                return self._download_with_ytdlp()
            except Exception as ytdlp_error:
                logger.error(f"All download methods failed: {ytdlp_error}")
                raise PytubeError("All download attempts failed") from ytdlp_error
    
    def _download_with_pytube(self) -> str:
        """Try downloading with pytube with multiple retries"""
        for attempt in range(self.max_retries):
            try:
                yt = YouTube(
                    self.url,
                    use_oauth=True,
                    allow_oauth_cache=True
                )
                
                # Get the highest resolution stream
                stream = yt.streams.get_highest_resolution()
                if not stream:
                    raise PytubeError("No suitable stream found")
                
                # Save to Downloads folder
                downloads_path = os.path.expanduser("~/Downloads")
                self.video_path = os.path.join(downloads_path, f"{yt.title}.mp4")
                
                # Ensure filename is unique
                counter = 1
                while os.path.exists(self.video_path):
                    self.video_path = os.path.join(downloads_path, f"{yt.title}_{counter}.mp4")
                    counter += 1
                
                stream.download(
                    output_path=downloads_path,
                    filename=os.path.basename(self.video_path),
                    skip_existing=False
                )
                
                logger.info(f"Successfully downloaded with pytube: {self.video_path}")
                return self.video_path
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed. Retrying in {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                    continue
                raise PytubeError(f"PyTube download failed: {str(e)}") from e
    
    def _download_with_ytdlp(self) -> str:
        """Fallback download method using yt-dlp"""
        logger.info("Attempting download with yt-dlp")
        
        downloads_path = os.path.expanduser("~/Downloads")
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'retries': 3,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                self.video_path = ydl.prepare_filename(info)
                
                # Handle duplicate filenames
                if os.path.exists(self.video_path):
                    base, ext = os.path.splitext(self.video_path)
                    counter = 1
                    while os.path.exists(f"{base}_{counter}{ext}"):
                        counter += 1
                    self.video_path = f"{base}_{counter}{ext}"
                    os.rename(ydl.prepare_filename(info), self.video_path)
                
                logger.info(f"Successfully downloaded with yt-dlp: {self.video_path}")
                return self.video_path
        except Exception as e:
            raise PytubeError(f"yt-dlp download failed: {str(e)}") from e

# Example usage:
if __name__ == "__main__":
    sys.argv = sys.argv[1:]  # Allow passing URL as command line argument
    url = sys.argv[0] if sys.argv else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    downloader = YouTubeDownloader(url)
    try:
        video_path = downloader.download_video()
        print(f"Video downloaded to: {video_path}")
    except Exception as e:
        print(f"Failed to download video: {e}")