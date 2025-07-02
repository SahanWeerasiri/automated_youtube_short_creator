import os
import logging
from typing import Optional, Tuple
from pytube import YouTube
from pytube.exceptions import PytubeError
from requests.exceptions import HTTPError
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip 
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import ffmpeg
from datetime import timedelta
import tempfile
import argparse
import requests
import json
import time
import yt_dlp
import speech_recognition as sr
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import request
import subprocess

# Configure logging with colors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ColorFormatter(logging.Formatter):
    """Custom formatter to add colors to logs"""
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[91m',  # Red
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        message = super().format(record)
        return f"{color}{message}{self.COLORS['RESET']}"

# Apply color formatter
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.handlers = [handler]


class YouTubeDownloader:
    """Comprehensive YouTube video downloader with multiple fallback options"""
    
    def __init__(self, url: str):
        self.url = url
        self.video_path: Optional[str] = None
        self.temp_dir = tempfile.mkdtemp(prefix='yt_dl_')
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
    def download_video(self) -> str:
        """Main download method with multiple fallback strategies"""
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
                # Configure pytube with custom headers
                self._configure_pytube_headers()
                
                yt = YouTube(
                    self.url,
                    use_oauth=True,
                    allow_oauth_cache=True
                )
                
                # Try different stream selection methods
                stream = self._select_best_pytube_stream(yt)
                if not stream:
                    raise PytubeError("No suitable stream found")
                
                self.video_path = os.path.join(self.temp_dir, 'video.mp4')
                stream.download(
                    output_path=self.temp_dir,
                    filename='video.mp4',
                    skip_existing=False
                )
                
                logger.info(f"Successfully downloaded with pytube: {self.video_path}")
                return self.video_path
                
            except HTTPError as e:
                if e.code == 400:
                    logger.warning(f"Attempt {attempt + 1}: HTTP 400 error. Retrying in {self.retry_delay}s...")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    raise PytubeError("Failed after multiple retries") from e
                raise
            except Exception as e:
                raise PytubeError(f"PyTube download failed: {str(e)}") from e
    
    def _configure_pytube_headers(self):
        """Configure pytube with custom headers to avoid 400 errors"""
        request.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'accept-language': 'en-US,en;q=0.9',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
    
    def _select_best_pytube_stream(self, yt: YouTube):
        """Try multiple stream selection strategies with pytube"""
        # Try different stream types in order of preference
        for stream_type in [
            {'progressive': True, 'file_extension': 'mp4'},  # Video+audio
            {'adaptive': True, 'file_extension': 'mp4'},      # Video only
            {}  # Any stream
        ]:
            stream = yt.streams.filter(**stream_type).order_by('resolution').desc().first()
            if stream:
                return stream
        return None
    
    def _download_with_ytdlp(self) -> str:
        """Fallback download method using yt-dlp"""
        logger.info("Attempting download with yt-dlp")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.temp_dir, 'video.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'retries': 3,
            'fragment_retries': 3,
            'extractor_retries': 3,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                self.video_path = ydl.prepare_filename(info)
                logger.info(f"Successfully downloaded with yt-dlp: {self.video_path}")
                return self.video_path
        except Exception as e:
            raise PytubeError(f"yt-dlp download failed: {str(e)}") from e
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                for filename in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        logger.error(f"Failed to delete {file_path}: {e}")
                os.rmdir(self.temp_dir)
                logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

    def extract_subtitles(self) -> str:
        """
        Download English subtitles using yt-dlp as a subprocess (auto-generated if needed).
        """
        subtitle_path = os.path.join(self.temp_dir, 'subtitles.srt')
        cmd = [
            'yt-dlp',
            '--write-auto-subs',
            '--sub-langs', 'en.*',
            '--skip-download',
            '-o', os.path.join(self.temp_dir, 'video.%(ext)s'),
            self.url
        ]
        try:
            logger.info(f"Running yt-dlp command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"yt-dlp failed: {result.stderr}")
                raise RuntimeError("yt-dlp subprocess failed.")
            # Find the actual subtitle file path
            srt_file = None
            for f in os.listdir(self.temp_dir):
                # Accept both .srt and .vtt files with English language code
                if (f.endswith('.srt') or f.endswith('.vtt')) and ('.en' in f or '.en-' in f):
                    srt_file = os.path.join(self.temp_dir, f)
                    break
            if not srt_file:
                raise RuntimeError("No English subtitles found with yt-dlp subprocess.")
            # If it's a .vtt file, convert to .srt using ffmpeg
            if srt_file.endswith('.vtt'):
                converted_path = subtitle_path
                cmd = [
                    'ffmpeg', '-y', '-i', srt_file, converted_path
                ]
                logger.info(f"Converting VTT to SRT: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    logger.error(f"ffmpeg failed to convert vtt to srt: {result.stderr}")
                    raise RuntimeError("Failed to convert vtt to srt.")
                logger.info(f"SRT file saved to: {converted_path}")
            else:
                os.rename(srt_file, subtitle_path)
                logger.info(f"SRT file saved to: {subtitle_path}")
        except Exception as e:
            logger.error(f"Failed to download subtitles with yt-dlp subprocess: {e}")
            raise RuntimeError("Subtitle extraction failed.") from e

        return subtitle_path

class GeminiProcessor:
    """Handles communication with Gemini API using HTTP requests"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        self.fallback_api_urls = [
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={self.api_key}",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        ]

    def find_peak_moments(self, srt_content: str) -> Tuple[float, float]:
        """Analyze subtitles to find the most interesting 20+ second segment"""
        logger.info("Analyzing subtitles with Gemini to find peak moments")
        prompt = (
            "Analyze the following video subtitles and identify the most engaging "
            "40-60 second segment."
            "Consider factors like emotional impact, humor, or key information.\n\n"
            "Return ONLY the start and end timestamps in this exact format: "
            "'START=seconds,END=seconds' where seconds are float numbers.\n\n"
            f"Subtitles:\n{srt_content[:10000]}"
        )
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        headers = {"Content-Type": "application/json"}
        last_error = None
        for api_url in self.fallback_api_urls:
            try:
                response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                if response.ok:
                    data = response.json()
                    try:
                        result = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    except (KeyError, IndexError):
                        raise ValueError("No valid response from Gemini API")
                    logger.info(f"Gemini response: {result}")
                    if "START=" not in result or "END=" not in result:
                        raise ValueError("Unexpected response format from Gemini")
                    start_str = result.split("START=")[1].split(",")[0]
                    end_str = result.split("END=")[1].split(",")[0]

                    def parse_time(t):
                        try:
                            return float(t)
                        except ValueError:
                            pass
                        parts = t.split(":")
                        if len(parts) == 3:
                            h, m, s = parts
                            return int(h) * 3600 + int(m) * 60 + float(s)
                        elif len(parts) == 2:
                            m, s = parts
                            return int(m) * 60 + float(s)
                        else:
                            raise ValueError(f"Unrecognized time format: {t}")

                    start = parse_time(start_str)
                    end = parse_time(end_str)
                    logger.info(f"Identified peak moment: {start}s to {end}s")
                    return start, end
                else:
                    logger.warning(f"Gemini model at {api_url} failed ({response.status_code}). Trying next fallback...")
                    last_error = RuntimeError(f"Error: {response.status_code} {response.text}")
            except Exception as e:
                logger.warning(f"Request to {api_url} failed: {e}")
                last_error = e
        logger.error("All Gemini API endpoints failed.")
        raise RuntimeError("Gemini analysis failed") from last_error
        
class VideoEditor:
    """Handles video editing tasks"""
    
    @staticmethod
    def cut_video(video_path: str, start: float, end: float, output_path: str) -> str:
        """Cut a segment from the video"""
        logger.info(f"Cutting video from {start}s to {end}s")
        try:
            with VideoFileClip(video_path) as video:
                clip = video.subclipped(start, end)
                clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
                logger.info(f"Video segment saved to {output_path}")
                return output_path
        except Exception as e:
            logger.error(f"Failed to cut video: {e}")
            raise
    
    @staticmethod
    def create_subtitle_clips(subtitle_path: str, video_size: Tuple[int, int]) -> SubtitlesClip:
        """Create styled subtitle clips from SRT file"""
        logger.info("Creating styled subtitle clips")
        try:
            # Custom generator that yields TextClip for each subtitle
            def generator(txt):
                return TextClip(
                    txt,
                    font='Arial-Bold',
                    fontsize=50,
                    color='yellow',
                    stroke_color='black',
                    stroke_width=2,
                    size=(int(video_size[0]*0.9), None),
                    method='caption',
                    align='center'
                ).set_position(('center', 'center'))
            
            subtitles = SubtitlesClip(subtitle_path, generator)
            return subtitles
        except Exception as e:
            logger.error(f"Failed to create subtitle clips: {e}")
            raise

def main(youtube_url: str, gemini_api_key: str, output_file: str):
    """Main workflow"""
    try:
        # Step 1: Download YouTube video
        yt_processor = YouTubeDownloader(youtube_url)
        video_path = yt_processor.download_video()
        
        # Step 2: Generate SRT file
        subtitle_path = yt_processor.extract_subtitles()
        
        # Step 3: Call Gemini API to find peak moments
        with open(subtitle_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        
        gemini = GeminiProcessor(gemini_api_key)
        start, end = gemini.find_peak_moments(srt_content)
        
        # Step 4: Cut the video at the given timestamps
        VideoEditor.cut_video(video_path, start, end, f'{output_file}.mp4')

        logger.info(f"Successfully created YouTube Short at {output_file}")
    except Exception as e:
        logger.error(f"Process failed: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate YouTube Shorts from longer videos')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('api_key', help='Gemini API key')
    parser.add_argument('output', help='Output file path')
    
    args = parser.parse_args()
    
    main(args.url, args.api_key, args.output)