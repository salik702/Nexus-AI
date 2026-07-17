from faster_whisper import WhisperModel
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    global _model

    if _model is None:
        print("Loading Model...")
        _model = WhisperModel(
            WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )
        print("Whisper Model Loaded Successfully")

    return _model


def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:
    model = load_model()

    task = "translate" if translate else "transcribe"

    segments, info = model.transcribe(
        chunk_path,
        task=task
    )

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    return transcript.strip()


def transcribe_all(chunks: list, translate: bool = False) -> str:
    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}")
        text = transcribe_chunk(chunk, translate=translate)
        full_transcript += text + " "

    print("Transcription Completed")

    return full_transcript.strip()