"""Orchestrator - Coordinates all agents for video analysis"""

from typing import Dict, Optional
from dataclasses import asdict
from .config import config
from .agents import (
    TranscriptExtractor,
    ContentSummarizer,
    InsightGenerator,
    FactChecker,
)
from .memory import MemoryStorage
from .guardrails import OutputGuardrails, GuardrailResult


class VideoAnalysisOrchestrator:
    """Orchestrates the multi-agent system"""
    
    def __init__(self):
        """Initialize orchestrator with all agents"""
        self.transcript_extractor = TranscriptExtractor(config.TRANSCRIPT_CACHE)
        self.summarizer = ContentSummarizer()
        self.insight_generator = InsightGenerator()
        self.fact_checker = FactChecker()
        self.memory = MemoryStorage(config.MEMORY_PATH)
    
    def analyze(self, youtube_url: str) -> Dict:
        """
        Analyze a YouTube video end-to-end
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Dictionary containing complete analysis with:
            - metadata (video_id, title, duration, url)
            - transcript (full text and segments)
            - summary (short_summary, bullet_points, key_takeaways, topics)
            - insights (patterns, implications, action_items, etc.)
            - fact_check_results (verified claims and confidence)
            - metadata (guardrail_status, confidence_scores)
        """
        
        print(f"Starting analysis for: {youtube_url}")
        
        # Step 1: Extract transcript
        print("📝 Step 1: Extracting transcript...")
        transcript_data = self.transcript_extractor.extract(youtube_url)
        print(f"✓ Extracted {len(transcript_data['transcript'])} transcript segments")
        
        # Get full transcript text
        transcript_segments = transcript_data["transcript"]
        transcript_text = self.transcript_extractor.get_full_transcript_text(
            transcript_segments
        )
        
        # Step 2: Generate summary
        print("📋 Step 2: Generating summary...")
        summary = self.summarizer.summarize(transcript_text)
        print(f"✓ Generated summary with {len(summary.bullet_points)} bullet points")
        
        # Validate summary
        summary_validation = OutputGuardrails.validate_summary(summary.short_summary)
        bullet_validation = OutputGuardrails.validate_bullet_points(summary.bullet_points)
        
        # Step 3: Generate insights
        print("💡 Step 3: Generating insights...")
        insights = self.insight_generator.generate_insights(
            transcript_text,
            summary.short_summary
        )
        print(f"✓ Generated {len(insights.action_items)} actionable items")
        
        # Step 4: Fact checking
        print("✓ Step 4: Fact checking...")
        all_claims = (
            summary.bullet_points +
            summary.key_takeaways +
            insights.action_items
        )
        fact_check_results = self.fact_checker.check_facts(
            all_claims,
            transcript_text,
            transcript_segments
        )
        confidence_summary = self.fact_checker.generate_confidence_summary(
            fact_check_results
        )
        print(f"✓ Fact-checked {len(fact_check_results)} claims")
        
        # Step 5: Compile results
        print("📊 Step 5: Compiling results...")
        analysis_result = {
            "metadata": {
                "video_id": transcript_data["video_id"],
                "title": transcript_data["title"],
                "url": transcript_data["url"],
                "duration_seconds": transcript_data["duration"],
                "transcript_segments_count": len(transcript_segments),
            },
            "transcript": {
                "full_text": transcript_text,
                "segments": [asdict(seg) for seg in transcript_segments],
            },
            "summary": asdict(summary),
            "insights": asdict(insights),
            "fact_check": {
                "summary": confidence_summary,
                "detailed_results": [
                    {
                        "claim": fc.claim,
                        "supported": fc.supported,
                        "confidence": fc.confidence,
                        "evidence": fc.evidence,
                        "timestamp": fc.timestamp,
                    }
                    for fc in fact_check_results
                ]
            },
            "quality_metrics": {
                "summary_validation": summary_validation.dict(),
                "bullet_points_validation": bullet_validation.dict(),
                "overall_confidence": round(
                    (summary_validation.confidence + 
                     bullet_validation.confidence +
                     confidence_summary["average_confidence"]) / 3,
                    2
                ),
            }
        }
        
        # Step 6: Store in memory
        print("💾 Step 6: Storing in memory...")
        self.memory.save_analysis(analysis_result)
        print("✓ Analysis saved to memory")
        
        print("✅ Analysis complete!")
        return analysis_result
    
    def get_previous_analyses(self, limit: int = 10) -> list:
        """Get previous analyses from memory"""
        return self.memory.get_analysis_history(limit)
    
    def find_similar_videos(self, video_id: str) -> list:
        """Find similar previously analyzed videos"""
        return self.memory.find_similar_videos(video_id)


if __name__ == "__main__":
    # Test orchestrator
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <youtube_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    orchestrator = VideoAnalysisOrchestrator()
    result = orchestrator.analyze(url)
    
    print("\n" + "="*60)
    print("ANALYSIS RESULT SUMMARY")
    print("="*60)
    print(f"Title: {result['metadata']['title']}")
    print(f"Summary: {result['summary']['short_summary']}")
    print(f"Confidence: {result['quality_metrics']['overall_confidence']}")
