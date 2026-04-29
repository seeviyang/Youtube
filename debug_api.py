#!/usr/bin/env python3
"""
Debug script for testing the full API analysis flow with breakpoints.

Usage:
    python debug_api.py

Then set breakpoints and interact with the debugger.
"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))

from orchestrator import VideoAnalysisOrchestrator
from config import config


def debug_full_analysis():
    """Debug the complete analysis pipeline"""
    
    print("\n" + "="*60)
    print("🐛 DEBUG: Full API Analysis Pipeline")
    print("="*60)
    
    # Check Ollama connection first
    print("\n📡 Checking Ollama connection...")
    if not config.validate_ollama_connection():
        print("❌ ERROR: Ollama not connected!")
        print("   Make sure to run: ollama serve")
        sys.exit(1)
    print("✓ Ollama connected")
    
    # Test URL
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"\n📺 Testing URL: {youtube_url}")
    
    # Initialize orchestrator
    print("\n📝 Step 1: Initialize orchestrator...")
    orchestrator = VideoAnalysisOrchestrator()
    print("✓ Orchestrator initialized")
    
    # 🔴 BREAKPOINT 1: Inspect orchestrator components
    print("\n🔍 Components:")
    print(f"   - Transcript Extractor: {orchestrator.transcript_extractor}")
    print(f"   - Summarizer: {orchestrator.summarizer}")
    print(f"   - Insight Generator: {orchestrator.insight_generator}")
    print(f"   - Fact Checker: {orchestrator.fact_checker}")
    print(f"   - Memory: {orchestrator.memory}")
    
    import pdb; pdb.set_trace()  # 🔴 BREAKPOINT HERE
    
    # Run analysis
    print("\n📝 Step 2: Running full analysis...")
    print("   ⏳ This will take 30-60 seconds...\n")
    
    try:
        result = orchestrator.analyze(youtube_url)
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE!")
        print("="*60)
        
        # 🔴 BREAKPOINT 2: Inspect result structure
        print("\n🔍 Result Structure:")
        print(f"   Top-level keys: {list(result.keys())}")
        print(f"   Metadata keys: {list(result['metadata'].keys())}")
        print(f"   Summary keys: {list(result['summary'].keys())}")
        print(f"   Insights keys: {list(result['insights'].keys())}")
        print(f"   Fact-check keys: {list(result['fact_check'].keys())}")
        
        import pdb; pdb.set_trace()  # 🔴 BREAKPOINT HERE
        
        # Print summary
        print("\n📋 SUMMARY:")
        print(f"   Title: {result['metadata']['title']}")
        print(f"   Duration: {result['metadata']['duration_seconds']}s")
        print(f"   Segments: {result['metadata']['transcript_segments_count']}")
        print(f"   Summary: {result['summary']['short_summary'][:200]}...")
        
        # Print bullet points
        print("\n🔹 BULLET POINTS:")
        for i, bullet in enumerate(result['summary']['bullet_points'][:3], 1):
            print(f"   {i}. {bullet}")
        
        # Print action items
        print("\n💡 ACTION ITEMS:")
        for i, item in enumerate(result['insights']['action_items'][:2], 1):
            print(f"   {i}. {item[:100]}...")
        
        # Print fact-check summary
        print("\n✓ FACT-CHECK SUMMARY:")
        fc_summary = result['fact_check']['summary']
        print(f"   Total checked: {fc_summary['total_facts_checked']}")
        print(f"   Supported: {fc_summary['supported_facts']}")
        print(f"   Unsupported: {fc_summary['unsupported_facts']}")
        print(f"   Support rate: {fc_summary['support_percentage']}%")
        print(f"   Average confidence: {fc_summary['average_confidence']}")
        
        # Print quality metrics
        print("\n📊 QUALITY METRICS:")
        metrics = result['quality_metrics']
        print(f"   Summary valid: {metrics['summary_validation']['is_valid']}")
        print(f"   Bullet points valid: {metrics['bullet_points_validation']['is_valid']}")
        print(f"   Overall confidence: {metrics['overall_confidence']}")
        
        # 🔴 BREAKPOINT 3: Before saving
        print("\n💾 Saving to memory...")
        import pdb; pdb.set_trace()  # 🔴 BREAKPOINT HERE
        
        return result
        
    except Exception as e:
        print(f"\n❌ ERROR during analysis: {e}")
        import traceback
        traceback.print_exc()
        
        # 🔴 BREAKPOINT 4: Debug the error
        import pdb; pdb.set_trace()
        
        return None


def debug_transcript_only():
    """Debug just the transcript extraction"""
    
    print("\n" + "="*60)
    print("🐛 DEBUG: Transcript Extraction Only")
    print("="*60)
    
    from agents.transcript_extractor import TranscriptExtractor
    
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    extractor = TranscriptExtractor()
    
    print(f"\n📺 Extracting: {youtube_url}")
    
    # 🔴 BREAKPOINT: Before extraction
    import pdb; pdb.set_trace()
    
    result = extractor.extract(youtube_url)
    
    print(f"\n✓ Extracted {len(result['transcript'])} segments")
    print(f"  Title: {result['title']}")
    
    # 🔴 BREAKPOINT: After extraction, inspect segments
    import pdb; pdb.set_trace()
    
    for i, seg in enumerate(result['transcript'][:5]):
        print(f"  [{i}] {seg.timestamp}: {seg.text[:50]}...")


def debug_summarizer_only():
    """Debug just the summarizer"""
    
    print("\n" + "="*60)
    print("🐛 DEBUG: Summarizer Only")
    print("="*60)
    
    from agents.transcript_extractor import TranscriptExtractor
    from agents.summarizer import ContentSummarizer
    
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Get transcript first
    print("\n📝 Getting transcript...")
    extractor = TranscriptExtractor()
    transcript_data = extractor.extract(youtube_url)
    full_text = extractor.get_full_transcript_text(transcript_data['transcript'])
    
    print(f"✓ Got {len(full_text)} chars of text")
    print(f"  First 200 chars: {full_text[:200]}...")
    
    # Now test summarizer
    print("\n📋 Testing Summarizer...")
    summarizer = ContentSummarizer()
    
    # 🔴 BREAKPOINT: Before summarization
    import pdb; pdb.set_trace()
    
    summary = summarizer.summarize(full_text)
    
    print("\n✓ Generated summary:")
    print(f"  {summary.short_summary}")
    
    # 🔴 BREAKPOINT: After summarization
    import pdb; pdb.set_trace()
    
    print(f"\n✓ Bullet points ({len(summary.bullet_points)}):")
    for bullet in summary.bullet_points[:3]:
        print(f"  - {bullet}")


def main():
    """Main debug entry point"""
    print("\n🔍 YouTube Analysis System - Debug Mode\n")
    
    choice = input("""
Choose what to debug:
1. Full Analysis Pipeline (all steps)
2. Transcript Extraction (transcript only)
3. Summarizer (transcript → summary)
4. Exit

Enter choice (1-4): """).strip()
    
    if choice == "1":
        debug_full_analysis()
    elif choice == "2":
        debug_transcript_only()
    elif choice == "3":
        debug_summarizer_only()
    else:
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
