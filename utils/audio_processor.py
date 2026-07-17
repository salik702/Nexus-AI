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

YOUTUBE_CLIENT_PROFILES = [
    None,
    ["android"],
    ["ios"],
    ["web", "android"],
]


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


def _build_ydl_opts(player_clients: list[str] | None = None) -> dict:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
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

    if player_clients:
        ydl_opts["extractor_args"] = {"youtube": {"player_client": player_clients}}

    cookiefile = _resolve_cookiefile() or _ensure_cookiefile_from_content()
    if cookiefile:
        ydl_opts["cookiefile"] = cookiefile

    return ydl_opts


def download_youtube_audio(url: str) -> str:
    last_error = None

    if not (_resolve_cookiefile() or _resolve_cookie_content()):
        print(
            "No cookies found; if YouTube blocks the request, add cookies to Streamlit secrets as YTDLP_COOKIE_CONTENT or upload cookies.txt."
        )

    for player_clients in YOUTUBE_CLIENT_PROFILES:
        try:
            client_name = ",".join(player_clients) if player_clients else "default"
            print(f"Trying YouTube client profile: {client_name}")
            with yt_dlp.YoutubeDL(_build_ydl_opts(player_clients)) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = (
                    ydl.prepare_filename(info)
                    .replace(".webm", ".wav")
                    .replace(".m4a", ".wav")
                )
                return filename
        except Exception as error:
            last_error = error
            message = str(error)
            print(
                f"YouTube download failed for profile {player_clients or 'default'}: {message}"
            )
            if "403" not in message and "Forbidden" not in message:
                raise

    raise RuntimeError(
        "Unable to download video data from YouTube after trying multiple client profiles. "
        "If the video is age-restricted, region-restricted, or members-only, add valid cookies to Streamlit Secrets as YTDLP_COOKIE_CONTENT."
    ) from last_error


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
