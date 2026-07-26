import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok = True)


# ✅ Sirf yeh 2 lines add ki hain
# FFMPEG_PATH = "D:/sms/ffmpeg-8.1.2-essentials_build/bin/ffmpeg.exe"

#upar wali line FFMPEG_PATCH chhe aa hatavi jayre loaclly run karvu hoy aa github push kariye atala hatavi
# nahi tar code run nai thay local machine per




def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    # ydl_opts = {
    #     "format": "bestaudio/best",
    #     "outtmpl": output_path,
    #     "postprocessors": [
    #         {
    #             "key": "FFmpegExtractAudio",
    #             "preferredcodec": "wav",
    #             "preferredquality": "192",
    #         }
    #     ],
    #     "quiet": True,
    #     "ffmpeg_location": FFMPEG_PATH,
    # }

#upar wali line FFMPEG_PATCH chhe aa hatavi jayre loaclly run karvu hoy aa github push kariye atala hatavi
# nahi tar code run nai thay local machine per



    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_path,
    "quiet": True,
    "noplaylist": True,

    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }
    ],

    "http_headers": {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0 Safari/537.36"
        )
    }
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename

# data=download_youtube_audio("https://youtu.be/mtiOK2QG9Q0?si=ruaWGEXfMGYQLlek")




def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path

# data_final=convert_to_wav(data)


def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

# print(chunk_audio(data_final))


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks


