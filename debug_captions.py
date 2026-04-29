#!/usr/bin/env python3
"""Debug script to check YouTube captions"""

import yt_dlp
import json

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

ydl_opts = {
    "quiet": False,
    "no_warnings": False,
    "extract_flat": False,
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitlesformat": "json3",
    "subtitleslangs": ["en", "en-US", "en-GB", "a.en"],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
    print("=== SUBTITLES ===")
    if info.get("subtitles"):
        for lang, captions in list(info["subtitles"].items())[:2]:
            print(f"\n{lang}: {len(captions)} captions")
            print(f"First caption: {captions[0] if captions else 'None'}")
    else:
        print("No subtitles found")
    
    print("\n=== AUTOMATIC CAPTIONS ===")
    if info.get("automatic_captions"):
        for lang, captions in list(info["automatic_captions"].items())[:2]:
            print(f"\n{lang}: {len(captions)} captions")
            print(f"First caption: {captions[0] if captions else 'None'}")
    else:
        print("No automatic captions found")
