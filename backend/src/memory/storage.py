"""Memory storage implementation using ChromaDB"""

import json
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime


class MemoryStorage:
    """Local memory storage for analysis history"""
    
    def __init__(self, storage_path: str):
        """Initialize memory storage"""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.history_file = self.storage_path / "history.json"
        self.preferences_file = self.storage_path / "preferences.json"
    
    def save_analysis(self, analysis: Dict) -> None:
        """Save a completed analysis to history"""
        history = self._load_history()
        
        # Add metadata
        analysis["saved_at"] = datetime.now().isoformat()
        analysis["id"] = analysis.get("video_id", f"unknown_{len(history)}")
        
        history.append(analysis)
        
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2, default=str)
    
    def get_analysis_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get analysis history"""
        history = self._load_history()
        
        if limit:
            return history[-limit:]
        return history
    
    def find_similar_videos(self, video_id: str, limit: int = 5) -> List[Dict]:
        """Find similar previously analyzed videos"""
        history = self._load_history()
        
        # Simple similarity based on topics
        current_video = next(
            (v for v in history if v.get("video_id") == video_id),
            None
        )
        
        if not current_video:
            return []
        
        current_topics = set(current_video.get("analysis", {}).get("topics", []))
        
        similar = []
        for video in history:
            if video.get("video_id") == video_id:
                continue
            
            video_topics = set(video.get("analysis", {}).get("topics", []))
            overlap = len(current_topics & video_topics)
            
            if overlap > 0:
                similar.append((video, overlap))
        
        # Sort by overlap and return top results
        similar.sort(key=lambda x: x[1], reverse=True)
        return [v[0] for v in similar[:limit]]
    
    def save_preferences(self, preferences: Dict) -> None:
        """Save user preferences"""
        with open(self.preferences_file, "w") as f:
            json.dump(preferences, f, indent=2)
    
    def get_preferences(self) -> Dict:
        """Get user preferences"""
        if not self.preferences_file.exists():
            return {}
        
        try:
            with open(self.preferences_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _load_history(self) -> List[Dict]:
        """Load analysis history"""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except Exception:
            return []
