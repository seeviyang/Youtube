#!/usr/bin/env python3
"""
Simple interactive debugger for YouTube Analysis.

This script lets you debug step-by-step with full control.

Usage:
    python simple_debug.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))


def main():
    print("\n" + "="*70)
    print("🐛  SIMPLE DEBUG MODE - YouTube Analysis System")
    print("="*70)
    
    print("""
What would you like to debug?

1. 📜 Transcript Extraction
   - Extract captions from a YouTube video
   - Inspect transcript segments
   - Check caption download

2. 📝 Summarization
   - Take transcript and generate summary
   - Inspect bullet points and key takeaways
   - Check LLM output

3. 💡 Insights
   - Generate patterns and insights
   - Check action items
   - Inspect related topics

4. ✓ Fact Checking
   - Verify claims in transcript
   - Check confidence scores
   - Inspect evidence mapping

5. 🔄 Full Pipeline
   - Run all steps end-to-end
   - Inspect data at each stage
   - Check final response

6. 🔐 Debugging Tools
   - Open Python REPL for manual testing
   - Import and test components directly
""")
    
    choice = input("Enter choice (1-6): ").strip()
    
    if choice == "1":
        debug_transcript()
    elif choice == "2":
        debug_summarizer()
    elif choice == "3":
        debug_insights()
    elif choice == "4":
        debug_fact_checker()
    elif choice == "5":
        debug_pipeline()
    elif choice == "6":
        debug_repl()
    else:
        print("Invalid choice")
        sys.exit(1)


def debug_transcript():
    """Step-by-step transcript extraction"""
    print("\n" + "="*70)
    print("📜 DEBUGGING: Transcript Extraction")
    print("="*70)
    
    from agents.transcript_extractor import TranscriptExtractor
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\n📺 URL: {url}")
    
    print("\n" + "─"*70)
    print("STEP 1: Initialize Extractor")
    print("─"*70)
    
    extractor = TranscriptExtractor()
    print(f"✓ Created extractor")
    print(f"  - Cache dir: {extractor.cache_dir}")
    
    input("\n▶️  Press Enter to continue...")
    
    print("\n" + "─"*70)
    print("STEP 2: Extract Video ID")
    print("─"*70)
    
    video_id = extractor._extract_video_id(url)
    print(f"✓ Video ID: {video_id}")
    
    input("\n▶️  Press Enter to continue...")
    
    print("\n" + "─"*70)
    print("STEP 3: Extract Transcript (downloading captions...)")
    print("─"*70)
    print("⏳ This may take 10-20 seconds...\n")
    
    result = extractor.extract(url, use_cache=False)
    
    print(f"\n✓ Extraction complete!")
    print(f"  - Video ID: {result['video_id']}")
    print(f"  - Title: {result['title']}")
    print(f"  - Duration: {result['duration']}s")
    print(f"  - Segments: {len(result['transcript'])}")
    
    input("\n▶️  Press Enter to inspect segments...")
    
    print("\n" + "─"*70)
    print("STEP 4: Inspect First 5 Segments")
    print("─"*70)
    
    for i, seg in enumerate(result['transcript'][:5], 1):
        print(f"\n  Segment {i}:")
        print(f"    ⏱️  Timestamp: {seg.timestamp}")
        print(f"    ⏰ Seconds: {seg.seconds}")
        print(f"    📝 Text: {seg.text[:80]}")
        if len(seg.text) > 80:
            print(f"       {seg.text[80:]}...")
    
    input("\n▶️  Press Enter to generate full text...")
    
    print("\n" + "─"*70)
    print("STEP 5: Generate Full Transcript Text")
    print("─"*70)
    
    full_text = extractor.get_full_transcript_text(result['transcript'])
    print(f"✓ Generated full text:")
    print(f"  - Length: {len(full_text)} characters")
    print(f"  - Words: ~{len(full_text.split())} words")
    print(f"\n  First 300 characters:")
    print(f"  {full_text[:300]}")
    print(f"  ...")
    
    print("\n✅ Transcript extraction complete!")


def debug_summarizer():
    """Step-by-step summarization"""
    print("\n" + "="*70)
    print("📝 DEBUGGING: Summarization")
    print("="*70)
    
    from agents.transcript_extractor import TranscriptExtractor
    from agents.summarizer import ContentSummarizer
    from config import config
    
    # Check Ollama first
    print("\n📡 Checking Ollama connection...")
    if not config.validate_ollama_connection():
        print("❌ ERROR: Ollama not connected!")
        print("   Run: ollama serve")
        return
    print("✓ Ollama connected")
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("\n" + "─"*70)
    print("STEP 1: Extract Transcript")
    print("─"*70)
    print("⏳ Downloading captions...\n")
    
    extractor = TranscriptExtractor()
    result = extractor.extract(url)
    full_text = extractor.get_full_transcript_text(result['transcript'])
    
    print(f"✓ Got transcript: {len(full_text)} characters")
    
    input("\n▶️  Press Enter to summarize...")
    
    print("\n" + "─"*70)
    print("STEP 2: Generate Summary")
    print("─"*70)
    print("⏳ Calling LLM (this will take 15-30 seconds)...\n")
    
    summarizer = ContentSummarizer()
    summary = summarizer.summarize(full_text)
    
    print(f"\n✓ Summary generated!")
    
    input("\n▶️  Press Enter to view results...")
    
    print("\n" + "─"*70)
    print("STEP 3: Inspect Summary")
    print("─"*70)
    
    print(f"\n📋 SHORT SUMMARY:")
    print(f"   {summary.short_summary}\n")
    
    print(f"🔹 BULLET POINTS ({len(summary.bullet_points)}):")
    for i, bullet in enumerate(summary.bullet_points, 1):
        print(f"   {i}. {bullet}")
    
    print(f"\n💡 KEY TAKEAWAYS ({len(summary.key_takeaways)}):")
    for i, takeaway in enumerate(summary.key_takeaways, 1):
        print(f"   {i}. {takeaway}")
    
    print(f"\n🏷️  TOPICS ({len(summary.topics)}):")
    for i, topic in enumerate(summary.topics, 1):
        print(f"   {i}. {topic}")
    
    print("\n✅ Summarization complete!")


def debug_insights():
    """Step-by-step insights generation"""
    print("\n" + "="*70)
    print("💡 DEBUGGING: Insights Generation")
    print("="*70)
    
    from agents.transcript_extractor import TranscriptExtractor
    from agents.summarizer import ContentSummarizer
    from agents.insight_generator import InsightGenerator
    from config import config
    
    if not config.validate_ollama_connection():
        print("❌ Ollama not connected!")
        return
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("\n⏳ Extracting transcript...\n")
    extractor = TranscriptExtractor()
    result = extractor.extract(url)
    full_text = extractor.get_full_transcript_text(result['transcript'])
    
    print("⏳ Generating summary...\n")
    summarizer = ContentSummarizer()
    summary = summarizer.summarize(full_text)
    
    input("\n▶️  Press Enter to generate insights...")
    
    print("\n" + "─"*70)
    print("GENERATING INSIGHTS")
    print("─"*70)
    print("⏳ Calling LLM (10-20 seconds)...\n")
    
    generator = InsightGenerator()
    insights = generator.generate_insights(full_text, summary.short_summary)
    
    print(f"\n✓ Insights generated!")
    
    input("\n▶️  Press Enter to view results...")
    
    print("\n" + "─"*70)
    print("STEP: Inspect Insights")
    print("─"*70)
    
    print(f"\n🔍 PATTERNS ({len(insights.patterns)}):")
    for i, pattern in enumerate(insights.patterns[:3], 1):
        print(f"   {i}. {pattern[:100]}...")
    
    print(f"\n⚡ IMPLICATIONS ({len(insights.implications)}):")
    for i, impl in enumerate(insights.implications[:3], 1):
        print(f"   {i}. {impl[:100]}...")
    
    print(f"\n💼 ACTION ITEMS ({len(insights.action_items)}):")
    for i, action in enumerate(insights.action_items[:3], 1):
        print(f"   {i}. {action[:100]}...")
    
    print("\n✅ Insights generation complete!")


def debug_fact_checker():
    """Step-by-step fact checking"""
    print("\n" + "="*70)
    print("✓ DEBUGGING: Fact Checking")
    print("="*70)
    
    from agents.transcript_extractor import TranscriptExtractor
    from agents.summarizer import ContentSummarizer
    from agents.fact_checker import FactChecker
    from config import config
    
    if not config.validate_ollama_connection():
        print("❌ Ollama not connected!")
        return
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("\n⏳ Extracting transcript...\n")
    extractor = TranscriptExtractor()
    result = extractor.extract(url)
    full_text = extractor.get_full_transcript_text(result['transcript'])
    
    print("⏳ Generating summary...\n")
    summarizer = ContentSummarizer()
    summary = summarizer.summarize(full_text)
    
    input("\n▶️  Press Enter to fact-check...")
    
    print("\n" + "─"*70)
    print("FACT-CHECKING CLAIMS")
    print("─"*70)
    print("⏳ Checking claims (15-30 seconds)...\n")
    
    checker = FactChecker()
    claims = summary.bullet_points + summary.key_takeaways
    results = checker.check_facts(claims, full_text, result['transcript'])
    
    print(f"\n✓ Fact-checking complete!")
    print(f"  - Total claims: {len(results)}")
    
    input("\n▶️  Press Enter to view results...")
    
    print("\n" + "─"*70)
    print("FACT-CHECK RESULTS")
    print("─"*70)
    
    supported = sum(1 for r in results if r.supported)
    unsupported = len(results) - supported
    
    print(f"\n📊 SUMMARY:")
    print(f"   Supported: {supported}/{len(results)}")
    print(f"   Unsupported: {unsupported}/{len(results)}")
    print(f"   Support rate: {100*supported//len(results)}%")
    
    print(f"\n✓ SUPPORTED CLAIMS (first 3):")
    for i, result in enumerate([r for r in results if r.supported][:3], 1):
        print(f"   {i}. Claim: {result.claim[:60]}...")
        print(f"      Confidence: {result.confidence*100:.0f}%")
    
    print(f"\n❌ UNSUPPORTED CLAIMS (first 3):")
    unsupported_claims = [r for r in results if not r.supported]
    if unsupported_claims:
        for i, result in enumerate(unsupported_claims[:3], 1):
            print(f"   {i}. Claim: {result.claim[:60]}...")
            print(f"      Confidence: {result.confidence*100:.0f}%")
    else:
        print("   (All claims supported!)")
    
    print("\n✅ Fact-checking complete!")


def debug_pipeline():
    """Full end-to-end pipeline"""
    print("\n" + "="*70)
    print("🔄 DEBUGGING: Full Pipeline")
    print("="*70)
    
    from orchestrator import VideoAnalysisOrchestrator
    from config import config
    
    if not config.validate_ollama_connection():
        print("❌ Ollama not connected!")
        return
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\n🎯 Running full analysis on: {url}\n")
    
    orchestrator = VideoAnalysisOrchestrator()
    result = orchestrator.analyze(url)
    
    input("\n▶️  Press Enter to view full results...")
    
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)
    
    print(f"\n📺 METADATA:")
    print(f"   Title: {result['metadata']['title']}")
    print(f"   Duration: {result['metadata']['duration_seconds']}s")
    print(f"   Segments: {result['metadata']['transcript_segments_count']}")
    
    print(f"\n📋 SUMMARY:")
    print(f"   {result['summary']['short_summary'][:200]}...")
    
    print(f"\n✓ FACT-CHECK:")
    fc = result['fact_check']['summary']
    print(f"   Total: {fc['total_facts_checked']}")
    print(f"   Supported: {fc['supported_facts']}")
    print(f"   Support rate: {fc['support_percentage']:.0f}%")
    
    print(f"\n📊 QUALITY:")
    qm = result['quality_metrics']
    print(f"   Summary valid: {qm['summary_validation']['is_valid']}")
    print(f"   Bullets valid: {qm['bullet_points_validation']['is_valid']}")
    print(f"   Overall confidence: {qm['overall_confidence']}")
    
    print("\n✅ Full pipeline complete!")


def debug_repl():
    """Python REPL for manual testing"""
    print("\n" + "="*70)
    print("🔐 PYTHON REPL - Manual Testing")
    print("="*70)
    
    print("""
Interactive Python shell. You can now:
- Import modules
- Create objects
- Test functions
- Inspect data structures

Examples:
>>> from agents.transcript_extractor import TranscriptExtractor
>>> extractor = TranscriptExtractor()
>>> result = extractor.extract("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
>>> len(result['transcript'])
>>> result['transcript'][0]

Type 'exit()' to quit.
""")
    
    import code
    code.interact(local=globals())


if __name__ == "__main__":
    main()
