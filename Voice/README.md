# README

## Project Overview

*   **audio2text.py:** Likely handles the conversion of audio files into text.
*   **convertor.py:** Could contain general-purpose conversion functions used across other modules.
*   **gemini.py:** Probably integrates with Google's Gemini AI model, potentially for tasks like text generation or analysis.
*   **main.py:** The main entry point of the program, orchestrating the workflow and calling functions from other modules.
*   **text2audio.py:** Likely handles the conversion of text into audio files.


## Project Structure

The project structure is as follows:

```
- .env
- .gitignore
- audio2text.py
- convertor.py
- english_hello.wav
- gemini.py
- main.py
- text2audio.py
- Wolfga.mp3
- __pycache__
```

## Project Details

This project contains the following files:

- audio2text.py
### audio2text.py
The Python code defines a function `recognize_speech` that takes an audio file path as input and attempts to transcribe the audio into text using Google's Speech Recognition API.

Here's a breakdown:

1. **Initialization:** It initializes a `Recognizer` object from the `speech_recognition` library.

2. **Audio File Handling:** It first attempts to directly read the audio file using `sr.AudioFile`. If this fails (e.g., due to an unsupported audio format), it proceeds to convert the audio file to a compatible format using a function `convert_audio_format` (presumably defined in a separate module called `convertor`).  After successful conversion, it attempts to read the converted file.

3. **Error Handling During Audio Reading:**  It catches `FileNotFoundError` if the input audio file doesn't exist.

4. **Transcription:**  Once the audio is successfully read into an `AudioData` object, it uses `recognizer.recognize_google(audio)` to transcribe the audio using Google's Speech Recognition service.

5. **Transcription Error Handling:** It handles two specific errors that can occur during transcription:
   - `sr.UnknownValueError`: Raised if Google Speech Recognition can't understand the audio.
   - `sr.RequestError`:  Raised if there's an issue with the request to the Google Speech Recognition service (e.g., network error).

6. **Cleanup:** If the audio file was converted, the converted file is deleted using `os.remove(converted_file)` to avoid cluttering the file system.

7. **Return Value:** If the transcription is successful, the function returns the transcribed text as a string. If any error occurs during the process, it raises an exception with a descriptive error message.


- convertor.py
### convertor.py
The Python code defines a function `convert_audio_format` that takes an input audio file path and an optional output path (defaulting to "converted.wav"). The function uses the `pydub` library to:

1.  Load the audio file from the given input path.
2.  Convert the audio to mono (single channel).
3.  Set the audio's frame rate to 16kHz.
4.  Export the modified audio to a WAV file at the specified output path.

The function returns the output path of the converted WAV file. In essence, it normalizes audio files to a standardized format (mono, 16kHz WAV) for compatibility with other processes or systems.


- gemini.py
### gemini.py
This code defines a function `summarize_text` that uses the Gemini 2.0 Flash API to summarize a given text.  It takes the text as input, constructs a prompt asking for a summary of the text and important events, sends a request to the Gemini API, and returns the summary extracted from the API response. If the API request fails or the response doesn't contain a summary, it returns an error message.  The code also includes an example usage demonstrating how to use the `summarize_text` function with a sample text. It loads the Gemini API key from a `.env` file for authentication.


- main.py
### main.py
This Python code provides a speech-to-text and text-to-speech pipeline using external modules. Here's a breakdown:

1. **Imports:** It imports three modules:
   - `audio2text.recognize_speech`:  Likely a function that transcribes audio to text.
   - `gemini.summarize_text`: Likely a function that summarizes a given text (presumably using Google's Gemini model).
   - `text2audio.text_to_speech`:  Likely a function that converts text to speech (generates an audio file).
   - `text2audio.play_audio`: likely a function that plays an audio file using an external library.

2. **`speech_to_text()` Function:**
   - Prompts the user to enter the path to an audio file.
   - Calls `recognize_speech()` (from `audio2text`) to convert the audio file to text.
   - Then, calls `summarize_text()` (from `gemini`) to summarize the recognized text.
   - Prints the summarized text to the console.
   - Handles potential errors during the process (e.g., file not found, API issues) by printing an error message.
   - Returns the recognized and summarized text, or `None` if an error occurred.

3. **Main Execution Block (`if __name__ == "__main__":`)**
   - Calls the `speech_to_text()` function to get the recognized text.
   - If `speech_to_text()` returns text successfully (not `None`):
     - Calls `text_to_speech()` (from `text2audio`) to convert the recognized text back into an audio file.  The audio file is named using the first 6 characters of the text along with ".mp3" extension.
     - Calls `play_audio()` (from `text2audio`) to play the newly generated audio file.

In essence, the code takes an audio file path as input, converts it to text, summarizes the text, then converts the summarized text back to audio and plays it.  It relies on external modules for the core speech-to-text, text summarization, and text-to-speech functionalities.


- text2audio.py
### text2audio.py
This Python code provides a simple text-to-speech (TTS) functionality using the `gTTS` library and plays the generated audio using `pygame`.

Here's a breakdown:

1. **`text_to_speech(text, output_file="output.mp3")`**: This function takes text as input and converts it to speech using Google's Text-to-Speech service. It saves the audio as an MP3 file (defaulting to "output.mp3"). It includes error handling to catch potential issues during the conversion process.

2. **`play_audio(audio_file)`**: This function takes the audio file (created by `text_to_speech`) as input and plays it using the `pygame` library.  It initializes `pygame.mixer`, loads the audio file, starts playing, and waits until the audio finishes playing.  It also includes error handling in case there are problems playing the audio file.

In essence, the code allows you to convert text into spoken audio and then play that audio directly.


