import yt_dlp
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

DEFAULT_CHUNK_MINUTES = int(os.getenv("AUDIO_CHUNK_MINUTES", "1"))


def _resolve_cookiefile() -> str | None:
    candidates = [
        os.getenv("YTDLP_COOKIE_FILE"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "cookies.txt"),
        os.path.join(DOWNLOAD_DIR, "cookies.txt"),
    ]

    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate

    return None


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "ignoreconfig": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    cookiefile = _resolve_cookiefile()
    if cookiefile:
        ydl_opts["cookiefile"] = cookiefile
    else:
        print(
            "No cookies.txt found; if this video requires sign-in, export cookies to cookies.txt or set YTDLP_COOKIE_FILE."
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
