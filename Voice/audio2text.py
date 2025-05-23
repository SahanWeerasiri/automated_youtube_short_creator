import speech_recognition as sr
import os
from convertor import convert_audio_format

def recognize_speech(audio_file):
    """Recognize speech from audio file"""
    recognizer = sr.Recognizer()
    
    try:
        # First try directly
        try:
            with sr.AudioFile(audio_file) as source:
                print("Reading audio file...")
                audio = recognizer.record(source)
        except:
            # If direct read fails, try converting
            print("Converting audio format...")
            converted_file = convert_audio_format(audio_file)
            with sr.AudioFile(converted_file) as source:
                print("Reading converted audio file...")
                audio = recognizer.record(source)
            os.remove(converted_file)  # Clean up
        
        print("Processing...")
        text = recognizer.recognize_google(audio)
        return text

    except FileNotFoundError:
        raise Exception("Audio file not found.")
    except sr.UnknownValueError:
        raise Exception("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        raise Exception(f"Could not request results from Google Speech Recognition service; {e}")