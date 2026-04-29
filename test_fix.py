#!/usr/bin/env python3
"""Test the subtitle languages fix"""

def _list_available_subtitles_OLD(info: dict) -> str:
    """Old broken version"""
    available = []
    if info.get("subtitles"):
        available.extend(f"subtitles: {list(info['subtitles'].keys())}")  # BUG: extend() with a string
    if info.get("automatic_captions"):
        available.extend(f"auto: {list(info['automatic_captions'].keys())}")  # BUG: extend() with a string
    return ", ".join(available) if available else "None"


def _list_available_subtitles_NEW(info: dict) -> str:
    """New fixed version"""
    available = []
    if info.get("subtitles"):
        sub_langs = list(info['subtitles'].keys())
        available.append(f"subtitles: {', '.join(sub_langs)}")  # FIX: append() with proper string
    if info.get("automatic_captions"):
        auto_langs = list(info['automatic_captions'].keys())
        available.append(f"auto: {', '.join(auto_langs)}")  # FIX: append() with proper string
    return "; ".join(available) if available else "None"


if __name__ == "__main__":
    # Mock info dict
    info = {
        'subtitles': {'en': [], 'fr': [], 'de': []},
        'automatic_captions': {'en': [], 'es': []}
    }

    print("=" * 60)
    print("Testing subtitle languages string formatting")
    print("=" * 60)
    print()
    
    print("OLD (BROKEN) VERSION:")
    print("-" * 60)
    try:
        result_old = _list_available_subtitles_OLD(info)
        print(f"Result: {result_old}")
        print(f"Length: {len(result_old)}")
        print(f"First 100 chars: {result_old[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    print("NEW (FIXED) VERSION:")
    print("-" * 60)
    try:
        result_new = _list_available_subtitles_NEW(info)
        print(f"Result: {result_new}")
        print(f"Length: {len(result_new)}")
        print(f"Is proper JSON-serializable string: {isinstance(result_new, str)}")
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("✅ The fix changes:")
    print("   - From: available.extend(string) - treats string as iterable of chars")
    print("   - To: available.append(string) - treats string as single element")
    print()
    print("   - From: Produces character-separated output like: 's, u, b, t, i, t, l, e, s'")
    print("   - To: Produces proper formatted output like: 'subtitles: en, fr, de'")
