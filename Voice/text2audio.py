from gtts import gTTS  # Google Text-to-Speech
import pygame  # For playing audio

def text_to_speech(text, output_file="output.mp3"):
    """Convert text to speech and save as audio file"""
    try:
        print("Generating speech from text...")
        tts = gTTS(text=text, lang='en')
        tts.save(output_file)
        print(f"Audio saved as {output_file}")
        return output_file
    except Exception as e:
        raise Exception(f"Error in text-to-speech conversion: {e}")

def play_audio(audio_file):
    """Play the generated audio file"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        raise Exception(f"Error playing audio: {e}")
