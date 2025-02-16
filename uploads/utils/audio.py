from pydub import AudioSegment


def get_audio_length_ms(file_path) -> int:
    """
    Load an audio file and return its length in milliseconds.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        duration_ms = len(audio) + 100  # pydub's len() gives duration in milliseconds
        print(f"File: {file_path} | Duration: {duration_ms}ms")
        return duration_ms
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return 0
