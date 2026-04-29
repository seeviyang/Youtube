#!/usr/bin/env python3
"""
Debug script for testing transcript extraction with breakpoints.

Usage:
    python debug_transcript_extractor.py

Then set breakpoints in VS Code or use pdb commands when execution pauses.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))

from agents.transcript_extractor import TranscriptExtractor


def test_transcript_extraction():
    """Test transcript extraction with debugging"""
    
    print("\n" + "="*60)
    print("🐛 DEBUG: Transcript Extractor")
    print("="*60)
    
    # Test URL
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"\n📺 Testing URL: {youtube_url}")
    
    # Initialize extractor
    print("\n📝 Step 1: Initialize TranscriptExtractor...")
    extractor = TranscriptExtractor()
    print(f"   ✓ Cache directory: {extractor.cache_dir}")
    
    # Extract video ID
    print("\n📝 Step 2: Extract video ID...")
    video_id = extractor._extract_video_id(youtube_url)
    print(f"   ✓ Video ID: {video_id}")
    
    # Extract full transcript
    print("\n📝 Step 3: Extract transcript (this will download captions)...")
    print("   ⏳ This may take a moment...")
    
    # 🔴 BREAKPOINT 1: Set breakpoint here to inspect extractor state
    import pdb; pdb.set_trace()
    
    try:
        result = extractor.extract(youtube_url, use_cache=False)
        
        print("\n✅ SUCCESS! Transcript extracted:")
        print(f"   Video ID: {result['video_id']}")
        print(f"   Title: {result['title']}")
        print(f"   Duration: {result['duration']} seconds")
        print(f"   Segments: {len(result['transcript'])}")
        
        # 🔴 BREAKPOINT 2: Inspect transcript segments
        print("\n📝 First 3 segments:")
        for i, seg in enumerate(result['transcript'][:3]):
            print(f"   [{i}] {seg.timestamp} - {seg.text[:60]}...")
            # Uncomment to set breakpoint here:
            # import pdb; pdb.set_trace()
        
        # 🔴 BREAKPOINT 3: Get full text
        print("\n📝 Step 4: Generate full transcript text...")
        full_text = extractor.get_full_transcript_text(result['transcript'])
        print(f"   ✓ Full text length: {len(full_text)} characters")
        print(f"   ✓ First 200 chars: {full_text[:200]}...")
        
        return result
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # 🔴 BREAKPOINT 4: Debug the error
        import pdb; pdb.set_trace()
        
        return None


def test_caption_download():
    """Test caption URL download specifically"""
    
    print("\n" + "="*60)
    print("🐛 DEBUG: Caption URL Download")
    print("="*60)
    
    import yt_dlp
    
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\n📺 Extracting video info...")
    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        
        if info.get("subtitles"):
            print(f"\n✓ Found subtitles in {len(info['subtitles'])} languages")
            
            # 🔴 BREAKPOINT 5: Inspect subtitle structure
            for lang, captions in list(info["subtitles"].items())[:2]:
                print(f"\n   Language: {lang}")
                print(f"   Caption format: {type(captions)}")
                print(f"   Number of caption formats: {len(captions)}")
                
                # This is where we inspect the structure
                import pdb; pdb.set_trace()
                
                for i, caption in enumerate(captions[:1]):
                    print(f"   Caption[{i}] keys: {caption.keys()}")
                    if 'url' in caption:
                        print(f"   URL: {caption['url'][:100]}...")


def main():
    """Main debug entry point"""
    print("\n🔍 YouTube Analysis System - Debug Mode\n")
    
    choice = input("""
Choose what to debug:
1. Transcript Extraction (full flow)
2. Caption Download (URL inspection)
3. Exit

Enter choice (1-3): """).strip()
    
    if choice == "1":
        test_transcript_extraction()
    elif choice == "2":
        test_caption_download()
    else:
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
