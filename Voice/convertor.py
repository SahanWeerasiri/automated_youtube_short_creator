from pydub import AudioSegment

def convert_audio_format(input_path, output_path="converted.wav"):
    """Convert audio file to WAV format with correct parameters"""
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_channels(1)  # mono
    sound = sound.set_frame_rate(16000)  # 16kHz
    sound.export(output_path, format="wav")
    return output_path