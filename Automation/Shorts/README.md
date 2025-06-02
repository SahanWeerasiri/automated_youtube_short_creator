# README

## Project Overview

`main.py` likely contains the main program logic or entry point of the application.


## Project Structure

The project structure is as follows:

```
- .env
- .gitignore
- main.py
```

## Project Details

This project contains the following files:

- main.py
### main.py
This Python code is designed to automate the creation of YouTube Shorts from longer YouTube videos. It leverages multiple libraries and APIs to achieve this:

**Core Functionality:**

1.  **Video Downloading:**
    *   `YouTubeDownloader`: Downloads YouTube videos. It first attempts to use the `pytube` library. If that fails (e.g., due to geo-restrictions or changes in YouTube's structure), it falls back to `yt-dlp`, a more robust downloader known for handling a wider range of YouTube content.
    *   Includes error handling with retries and fallback mechanisms to ensure successful video download.

2.  **Subtitle Extraction:**
    *   Uses `yt-dlp` in a subprocess to download English subtitles in SRT format (or converts VTT to SRT using ffmpeg if needed).

3.  **AI-Powered Analysis (Gemini API):**
    *   `GeminiProcessor`: Communicates with the Google Gemini API (using an API key) to analyze the downloaded subtitles.
    *   `find_peak_moments`: This method takes the subtitles as input, generates a prompt to the Gemini API, and asks it to identify the most engaging 40-60 second segment within the video. It extracts the start and end times from Gemini's response. Includes fallback API URLs in case the primary one fails.

4.  **Video Editing:**
    *   `VideoEditor`:
        *   `cut_video`: Cuts the video to create the short, based on the start and end times provided by the Gemini API.  Uses moviepy's `VideoFileClip` for this.
        *   `create_subtitle_clips`: Creates styled subtitle clips from the SRT file and overlays them on the video.

5.  **Workflow and Main Execution:**
    *   The `main` function orchestrates the entire process.
    *   It downloads the video, extracts subtitles, calls the Gemini API to find the key moment, cuts the video to the specified segment, and (implicitly) saves it as a YouTube Short-ready video.
    *   Uses `argparse` to take the YouTube URL, Gemini API key, and output file path as command-line arguments.
    *   Includes robust error handling throughout the process, logging informative messages and using color-coded logging for better readability.
    *   Includes cleanup of temporary files created.

**Key Libraries Used:**

*   `pytube`:  For downloading YouTube videos (primary method).
*   `yt-dlp`:  A more powerful and versatile YouTube downloader (fallback).
*   `moviepy`:  For video editing tasks (cutting, overlaying subtitles).
*   `ffmpeg`: Used to convert vtt subtitles to srt format.
*   `requests`:  For making HTTP requests to the Gemini API.
*   `speech\_recognition`: Used for speech recognition, although not present in the code.
*   `argparse`: For parsing command-line arguments.
*   `logging`: For logging events and errors.
*   `tempfile`: For creating temporary directories.
*   `subprocess`: For running yt-dlp and ffmpeg as sub-processes.

**Workflow Summary:**

1.  **Input:** YouTube video URL, Gemini API key, output file path
2.  **Download:** Download the video using either `pytube` or `yt-dlp`.
3.  **Extract Subtitles:** Downloads subtitles in SRT format.
4.  **Analyze Subtitles:** Use the Gemini API to identify the peak moments by analyzing the subtitles.
5.  **Cut & Edit:** Trim the video to the identified segment.
6.  **Output:** Save the short as a new video file.

This code provides a complete solution for automating the creation of YouTube Shorts, from the initial video download to the final edited segment, leveraging the power of AI for content analysis.


