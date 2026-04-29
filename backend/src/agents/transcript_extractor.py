"""Transcript Extraction Agent - Extracts transcripts from YouTube videos"""

import json
import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass
import hashlib


@dataclass
class TranscriptSegment:
    """Represents a segment of transcript with timestamp"""
    timestamp: str  # HH:MM:SS format
    seconds: float
    text: str


class TranscriptExtractor:
    """Extracts transcripts from YouTube videos using yt-dlp"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the transcript extractor"""
        self.cache_dir = Path(cache_dir) if cache_dir else Path.cwd() / "data" / "transcripts"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def extract(self, youtube_url: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Extract transcript from YouTube video
        
        Args:
            youtube_url: YouTube video URL
            use_cache: Whether to use cached transcript if available
            
        Returns:
            Dictionary containing:
            - video_id: YouTube video ID
            - title: Video title
            - transcript: List of TranscriptSegment objects
            - duration: Video duration in seconds
            - language: Language of transcript
        """
        try:
            import yt_dlp
        except ImportError:
            raise ImportError("yt-dlp not installed. Install with: pip install yt-dlp")
        
        # Extract video ID
        video_id = self._extract_video_id(youtube_url)
        if not video_id:
            raise ValueError(f"Invalid YouTube URL: {youtube_url}")
        
        # Check cache
        cached_data = self._load_from_cache(video_id) if use_cache else None
        if cached_data:
            return cached_data
        
        # Extract transcript using yt-dlp
        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                # Don't try to write anything to disk
                "extract_flat": False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                
                # Get transcript (captions) - priority order
                transcript = self._extract_captions(info)
                
                if not transcript:
                    # Fallback: Try to get auto-generated captions
                    transcript = self._extract_auto_captions(info)
                
                if not transcript:
                    # Last resort: Try to get any available subtitle language
                    transcript = self._extract_any_language_captions(info)
                
                if not transcript:
                    # If still no transcript, provide helpful error
                    available_subs = self._list_available_subtitles(info)
                    raise ValueError(
                        f"No transcript available for this video. "
                        f"Available subtitles: {available_subs}"
                    )
                
                result = {
                    "video_id": video_id,
                    "title": info.get("title", "Unknown"),
                    "transcript": transcript,
                    "duration": info.get("duration", 0),
                    "language": "en",
                    "url": youtube_url,
                }
                
                # Cache the result
                self._save_to_cache(video_id, result)
                
                return result
        
        except Exception as e:
            raise RuntimeError(f"Failed to extract transcript: {str(e)}")
    
    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)",
            r"(?:youtube\.com\/watch\?v=)([^&]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_captions(self, info: Dict) -> Optional[List[TranscriptSegment]]:
        """Extract captions from video info"""
        try:
            if not info.get("subtitles"):
                return None
            
            # Try to get English subtitles
            for lang in ["en", "en-US", "en-GB"]:
                if lang in info["subtitles"]:
                    captions_data = info["subtitles"][lang]
                    parsed = self._parse_captions(captions_data)
                    if parsed:
                        return parsed
            
            # Fallback to first available language
            first_lang = next(iter(info["subtitles"]))
            captions_data = info["subtitles"][first_lang]
            return self._parse_captions(captions_data)
        
        except Exception as e:
            return None
    
    def _extract_auto_captions(self, info: Dict) -> Optional[List[TranscriptSegment]]:
        """Extract auto-generated captions from video info"""
        try:
            if not info.get("automatic_captions"):
                return None
            
            # Try to get English auto-captions
            for lang in ["en", "en-US", "en-GB", "a.en"]:
                if lang in info["automatic_captions"]:
                    return self._parse_captions(info["automatic_captions"][lang])
            
            # Fallback to first available language
            first_lang = next(iter(info["automatic_captions"]))
            return self._parse_captions(info["automatic_captions"][first_lang])
        
        except Exception:
            return None
    
    def _extract_any_language_captions(self, info: Dict) -> Optional[List[TranscriptSegment]]:
        """Extract captions in any available language (last resort)"""
        try:
            # Try subtitles first (official)
            if info.get("subtitles"):
                for lang, captions in info["subtitles"].items():
                    try:
                        result = self._parse_captions(captions)
                        if result:
                            print(f"Using subtitles in language: {lang}")
                            return result
                    except Exception:
                        continue
            
            # Then try automatic captions
            if info.get("automatic_captions"):
                for lang, captions in info["automatic_captions"].items():
                    try:
                        result = self._parse_captions(captions)
                        if result:
                            print(f"Using automatic captions in language: {lang}")
                            return result
                    except Exception:
                        continue
            
            return None
        except Exception:
            return None
    
    def _list_available_subtitles(self, info: Dict) -> str:
        """List all available subtitles for debugging"""
        available = []
        if info.get("subtitles"):
            sub_langs = list(info['subtitles'].keys())
            available.append(f"subtitles: {', '.join(sub_langs)}")
        if info.get("automatic_captions"):
            auto_langs = list(info['automatic_captions'].keys())
            available.append(f"auto: {', '.join(auto_langs)}")
        return "; ".join(available) if available else "None"
    
    def _parse_captions(self, captions: List[Dict]) -> List[TranscriptSegment]:
        """Parse captions into TranscriptSegment objects"""
        import json
        import urllib.request
        import socket
        import ssl
        
        segments = []
        
        # If captions is a list of URL metadata dicts, download the actual captions
        if captions and isinstance(captions[0], dict) and 'url' in captions[0]:
            try:
                caption_url = captions[0]['url']
                req = urllib.request.Request(caption_url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
                
                try:
                    # Create SSL context that doesn't verify certificates (for YouTube URLs)
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    
                    with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
                        caption_data = response.read().decode('utf-8')
                        
                        # Try to parse as JSON (json3 format)
                        try:
                            caption_json = json.loads(caption_data)
                            events = caption_json.get('events', [])
                            
                            for event in events:
                                if 'tStartMs' in event and 'segs' in event:
                                    start_time = int(event['tStartMs']) / 1000.0
                                    text_parts = [seg.get('utf8', '') for seg in event.get('segs', [])]
                                    text = ''.join(text_parts).strip()
                                    
                                    if text:
                                        timestamp = self._seconds_to_timestamp(start_time)
                                        segments.append(TranscriptSegment(
                                            timestamp=timestamp,
                                            seconds=start_time,
                                            text=text
                                        ))
                            
                            return segments if segments else None
                        except json.JSONDecodeError:
                            # If JSON parsing fails, return None to fall back to auto-captions
                            return None
                            
                except (urllib.error.URLError, socket.timeout) as e:
                    # Network error - return None to try next caption language
                    return None
            except Exception as e:
                return None
        
        # Otherwise, assume it's already parsed caption data
        for caption in captions:
            start_time = caption.get("start", 0)
            text = caption.get("text", "").strip()
            
            if not text:
                continue
            
            timestamp = self._seconds_to_timestamp(start_time)
            
            segments.append(TranscriptSegment(
                timestamp=timestamp,
                seconds=start_time,
                text=text
            ))
        
        return segments if segments else None
    
    @staticmethod
    def _seconds_to_timestamp(seconds: float) -> str:
        """Convert seconds to HH:MM:SS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def _get_cache_path(self, video_id: str) -> Path:
        """Get cache file path for video"""
        # Use hash to create safe filename
        safe_id = hashlib.md5(video_id.encode()).hexdigest()
        return self.cache_dir / f"{safe_id}.json"
    
    def _load_from_cache(self, video_id: str) -> Optional[Dict]:
        """Load transcript from cache"""
        cache_path = self._get_cache_path(video_id)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, "r") as f:
                data = json.load(f)
                # Reconstruct TranscriptSegment objects
                data["transcript"] = [
                    TranscriptSegment(**seg) for seg in data["transcript"]
                ]
                return data
        except Exception:
            return None
    
    def _save_to_cache(self, video_id: str, data: Dict) -> None:
        """Save transcript to cache"""
        cache_path = self._get_cache_path(video_id)
        
        try:
            # Convert TranscriptSegment objects to dicts
            cached_data = data.copy()
            cached_data["transcript"] = [
                {
                    "timestamp": seg.timestamp,
                    "seconds": seg.seconds,
                    "text": seg.text,
                }
                for seg in data["transcript"]
            ]
            
            with open(cache_path, "w") as f:
                json.dump(cached_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to cache transcript: {e}")
    
    def get_full_transcript_text(self, segments: List[TranscriptSegment]) -> str:
        """Get full transcript as single text"""
        return " ".join(seg.text for seg in segments)
