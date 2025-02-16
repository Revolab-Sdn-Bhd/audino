import ast
import json


def preprocess_transcription(transcription: str) -> list[dict]:
    try:
        return json.loads(transcription)  # Try to convert string to JSON
    except json.JSONDecodeError:
        # If it fails, preprocess the string
        transcripts = ast.literal_eval(transcription)

        def preprocess_segment(segment: str) -> dict:
            # E.g {'timestamp': (3.5, 6.5), 'text': ' هو الأكثر دارج حالياً'}
            return {"timestamp": segment["timestamp"], "text": segment["text"].strip()}

        return [preprocess_segment(segment) for segment in transcripts]
