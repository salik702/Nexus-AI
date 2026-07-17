import os
import time
from pathlib import Path

import httpx
from groq import Groq
from pydub import AudioSegment

_client = None

# Maximum retries for transient network errors
MAX_RETRIES = 3
MAX_SPLIT_DEPTH = 4


def get_groq_client() -> Groq:
    """Initialize and return the Groq client lazily with a generous timeout."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set. "
                "Please add it to your .env file."
            )
        # 5-minute timeout — large WAV uploads need time on slow connections
        _client = Groq(
            api_key=api_key,
            timeout=httpx.Timeout(300.0, connect=60.0),
        )
    return _client


def load_model():
    """Dummy loader for compatibility with any legacy imports."""
    return get_groq_client()


def _is_request_too_large(error: Exception) -> bool:
    status_code = getattr(error, "status_code", None)
    if status_code == 413:
        return True

    message = str(error).lower()
    return "request_too_large" in message or "413" in message


def _split_audio_file(chunk_path: Path) -> list[Path]:
    audio = AudioSegment.from_file(chunk_path)
    if len(audio) < 2000:
        raise ValueError(f"{chunk_path} is too small to split any further.")

    midpoint = len(audio) // 2
    split_paths = [
        chunk_path.with_name(f"{chunk_path.stem}_part1{chunk_path.suffix}"),
        chunk_path.with_name(f"{chunk_path.stem}_part2{chunk_path.suffix}"),
    ]

    audio[:midpoint].export(split_paths[0], format="wav")
    audio[midpoint:].export(split_paths[1], format="wav")

    print(
        f"Split {chunk_path} into {split_paths[0].name} and {split_paths[1].name} to satisfy Groq size limits."
    )
    return split_paths


def _transcribe_single_chunk(chunk_path: Path, translate: bool | str = False) -> str:
    client = get_groq_client()

    # Determine if we should translate.
    # We use Groq's translation endpoint (which translates to English) if:
    # 1. translate is a boolean and is True.
    # 2. translate is a string and matches "hinglish".
    is_translation = False
    if isinstance(translate, bool):
        is_translation = translate
    elif isinstance(translate, str):
        is_translation = translate.lower() == "hinglish"

    model_name = os.getenv("GROQ_WHISPER_MODEL", "whisper-large-v3-turbo")

    # Log file size for debugging
    file_size_mb = os.path.getsize(chunk_path) / (1024 * 1024)
    print(f"File size: {file_size_mb:.1f} MB")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if is_translation:
                print(
                    f"[Attempt {attempt}] Sending {chunk_path} to Groq Translation API..."
                )
                response = client.audio.translations.create(
                    file=chunk_path,
                    model=model_name,
                )
            else:
                print(
                    f"[Attempt {attempt}] Sending {chunk_path} to Groq Transcription API..."
                )
                # If we know the language is English, specify it for better accuracy.
                language_code = None
                if isinstance(translate, str) and translate.lower() == "english":
                    language_code = "en"

                response = client.audio.transcriptions.create(
                    file=chunk_path,
                    model=model_name,
                    language=language_code,
                )

            print(f"[Attempt {attempt}] Groq transcription completed for {chunk_path}.")
            return response.text.strip()

        except Exception as error:
            print(f"[Attempt {attempt}] Error: {error}")
            if _is_request_too_large(error):
                raise
            if attempt < MAX_RETRIES:
                wait = 2**attempt  # exponential backoff: 2s, 4s
                print(f"Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise


def transcribe_chunk(chunk_path: str, translate: bool | str = False) -> str:
    """Transcribe or translate an audio chunk using the Groq API with retries."""
    path = Path(chunk_path)

    try:
        return _transcribe_single_chunk(path, translate=translate)
    except Exception as error:
        if _is_request_too_large(error):
            if path.name.count("_part") >= MAX_SPLIT_DEPTH:
                raise RuntimeError(
                    f"Groq still rejected {chunk_path} after recursive splitting. Reduce AUDIO_CHUNK_MINUTES or re-encode the source audio."
                ) from error

            print(
                f"Groq rejected {chunk_path} with 413; splitting the chunk and retrying."
            )
            split_paths = _split_audio_file(path)
            parts = [
                transcribe_chunk(str(split_path), translate=translate)
                for split_path in split_paths
            ]
            return " ".join(part.strip() for part in parts if part.strip())

        raise RuntimeError(f"Failed to transcribe {chunk_path}: {error}") from error


def transcribe_all(chunks: list, translate: bool | str = False) -> str:
    """Transcribe all chunks sequentially and concatenate the results."""
    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}")
        text = transcribe_chunk(chunk, translate=translate)
        full_transcript += text + " "

    print("Transcription Completed")

    return full_transcript.strip()
