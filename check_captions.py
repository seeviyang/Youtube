#!/usr/bin/env python3
"""
Diagnostic script to check if a YouTube video has captions
"""
import sys

def check_video_captions(url: str) -> None:
    """Check if a video has captions available"""
    try:
        import yt_dlp
    except ImportError:
        print("❌ yt-dlp not installed. Install with: pip install yt-dlp")
        return
    
    print(f"\n🔍 Checking video: {url}\n")
    
    try:
        ydl_opts = {
            "quiet": False,
            "no_warnings": False,
            "extract_flat": False,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"✅ Video Title: {info.get('title', 'Unknown')}")
            print(f"   Duration: {info.get('duration', 0)} seconds")
            print(f"   Channel: {info.get('uploader', 'Unknown')}")
            print()
            
            # Check subtitles
            if info.get("subtitles"):
                print("✅ Official Subtitles (captions):")
                for lang, captions in info["subtitles"].items():
                    print(f"   - {lang}: {len(captions)} segments")
            else:
                print("❌ No Official Subtitles")
            
            print()
            
            # Check automatic captions
            if info.get("automatic_captions"):
                print("✅ Auto-Generated Captions:")
                for lang, captions in info["automatic_captions"].items():
                    print(f"   - {lang}: {len(captions)} segments")
            else:
                print("❌ No Auto-Generated Captions")
            
            print()
            
            # Summary
            has_captions = bool(info.get("subtitles") or info.get("automatic_captions"))
            if has_captions:
                print("✅ This video WILL WORK with your system!")
            else:
                print("❌ This video has NO captions - it will NOT work")
                print("   Try a different video or enable captions on this one")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure:")
        print("- The URL is a valid YouTube link")
        print("- The video is publicly accessible")
        print("- The video is not age-restricted")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_captions.py <youtube_url>")
        print("\nExample:")
        print("  python check_captions.py https://www.youtube.com/watch?v=eIho2S0ZahI")
        print("\nSupported URL formats:")
        print("  - https://www.youtube.com/watch?v=VIDEO_ID")
        print("  - https://youtu.be/VIDEO_ID")
        print("  - https://www.youtube.com/embed/VIDEO_ID")
        sys.exit(1)
    
    url = sys.argv[1]
    check_video_captions(url)
