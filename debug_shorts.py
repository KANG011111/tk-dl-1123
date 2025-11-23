from yt_dlp import YoutubeDL
import json

url = "https://www.youtube.com/@LIGHTSAREOFF/shorts"

opts = {
    "extract_flat": True,
    "quiet": True,
    "noprogress": True,
}

with YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download=False)
    print(json.dumps(info, indent=2))
