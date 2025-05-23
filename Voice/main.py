from audio2text import recognize_speech
from gemini import summarize_text
from text2audio import text_to_speech, play_audio

def speech_to_text():
    """Main function to get user input and display results"""
    audio_file = input("Enter the path to the audio file: ")
    
    try:
        text = recognize_speech(audio_file)

        text = summarize_text(text)
        
        print("You said:", text)
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    recognized_text = speech_to_text()

    if recognized_text:
        audio_file = text_to_speech(recognized_text, recognized_text[:6]+".mp3")
        play_audio(audio_file)