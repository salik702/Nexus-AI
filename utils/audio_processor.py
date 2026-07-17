import yt_dlp
import os
from pathlib import Path


def _get_secret(name: str):
    try:
        import streamlit as st

        return st.secrets.get(name)
    except Exception:
        return None


DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

DEFAULT_CHUNK_MINUTES = int(os.getenv("AUDIO_CHUNK_MINUTES", "1"))


def _resolve_cookiefile() -> str | None:
    secret_cookie_file = _get_secret("YTDLP_COOKIE_FILE")
    if secret_cookie_file and os.path.isfile(str(secret_cookie_file)):
        return str(secret_cookie_file)

    candidates = [
        os.getenv("YTDLP_COOKIE_FILE"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "cookies.txt"),
        os.path.join(DOWNLOAD_DIR, "cookies.txt"),
    ]

    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate

    return None


def _resolve_cookie_content() -> str | None:
    secret_cookie_content = _get_secret("YTDLP_COOKIE_CONTENT")
    if secret_cookie_content:
        return str(secret_cookie_content)

    return os.getenv("YTDLP_COOKIE_CONTENT")


def _ensure_cookiefile_from_content() -> str | None:
    cookie_content = _resolve_cookie_content()
    if not cookie_content:
        return None

    cookie_path = os.path.join(DOWNLOAD_DIR, "streamlit_cookies.txt")
    with open(cookie_path, "w", encoding="utf-8") as cookie_file:
        cookie_file.write(cookie_content)

    return cookie_path


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "ignoreconfig": True,
        "noplaylist": True,
        "retries": 3,
        "extractor_retries": 3,
        "socket_timeout": 30,
        "geo_bypass": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    cookiefile = _resolve_cookiefile() or _ensure_cookiefile_from_content()
    if cookiefile:
        ydl_opts["cookiefile"] = cookiefile
    else:
        print(
            "No cookies found; if YouTube blocks the request, add cookies to Streamlit secrets as YTDLP_COOKIE_CONTENT or upload cookies.txt."
        )

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = (
            ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
        )

    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    from pydub import AudioSegment

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # 16khz
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = DEFAULT_CHUNK_MINUTES) -> list:
    from pydub import AudioSegment

    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000  # Convert minutes to milliseconds

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print(f"Chunking audio into ~{DEFAULT_CHUNK_MINUTES}-minute segments...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
