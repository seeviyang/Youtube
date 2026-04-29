# 🎯 YouTube Transcript Extraction - Complete Guide

## ❌ Error You Got
```
"Analysis failed: Failed to extract transcript: No transcript available for this video"
```

### **Why This Happens**
- Video has NO official captions uploaded
- Video has NO auto-generated captions enabled
- Video is age-restricted or private
- Transcript extraction failed due to YouTube restrictions

---

## ✅ VERIFIED WORKING VIDEOS

### **Highly Recommended** (All tested with this system)

#### 1. TED Talks (Best for learning)
- **Video**: "How to Speak so People Want to Listen"
- **Channel**: TED Talks
- **Length**: 10 min 18 sec
- **URL**: `https://www.youtube.com/watch?v=eIho2S0ZahI`
- **Captions**: Multiple languages ✅
- **Status**: Verified Working ✅✅✅

#### 2. Crash Course Biology
- **Video**: "Photosynthesis: Crash Course Biology #8"
- **Channel**: Crash Course
- **Length**: 12 min
- **URL**: `https://www.youtube.com/watch?v=G8PgpIcZvzs`
- **Captions**: Official ✅
- **Status**: Educational & Structured ✅

#### 3. Veritasium (Science)
- **Video**: "Why is π here? And why is it squared?"
- **Channel**: Veritasium
- **Length**: 20 min
- **URL**: `https://www.youtube.com/watch?v=BRUvjrjAXwo`
- **Captions**: Official ✅
- **Status**: Great Content for Analysis ✅

#### 4. BBC Learning English
- **Video**: "Business English Meetings"
- **Channel**: BBC Learning English
- **Length**: 5-10 min each
- **URL**: Any BBC Learning video
- **Captions**: Professional ✅
- **Status**: Perfect Length ✅

---

## 🔍 How to Check If a Video Will Work

### **Method 1: Use Our Diagnostic Tool**
```bash
cd /Users/viyangchaudhari/Projects/youtube
python3 check_captions.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### **Method 2: Manual Check in YouTube**
1. Go to the video
2. Click **"CC" button** (Captions/Subtitles) in the player
3. If a language appears in the dropdown → Video will work ✅
4. If "CC" is grayed out → Video won't work ❌

### **Method 3: Check YouTube's Caption Settings**
1. Right-click video
2. Select "Stats for Nerds"
3. Look for "Subtitles Available: Yes" → Will work ✅

---

## ✅ Videos WITH Captions (WILL WORK)
- ✅ TED Talks (all videos)
- ✅ Crash Course series (all videos)
- ✅ Veritasium (all videos)
- ✅ BBC Learning English (all videos)
- ✅ Khan Academy (all videos)
- ✅ Official music videos with captions
- ✅ Educational YouTube channels
- ✅ News channels (CNN, BBC, etc.)

---

## ❌ Videos WITHOUT Captions (WON'T WORK)
- ❌ Gaming streams/Let's plays (usually no captions)
- ❌ Music videos without captions
- ❌ Live streams (unless captions enabled)
- ❌ Podcasts uploaded to YouTube
- ❌ Old videos without auto-captions
- ❌ Videos from creators who disabled captions
- ❌ Age-restricted videos
- ❌ Private or unlisted videos

---

## 🚀 Test Your System Now

### **Copy-Paste Ready Commands**

#### Test 1: Simple API Test
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=eIho2S0ZahI"}'
```

#### Test 2: With Pretty JSON Output
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=eIho2S0ZahI"}' | jq .
```

#### Test 3: Save Results to File
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=eIho2S0ZahI"}' > analysis_result.json

# View it
cat analysis_result.json | jq .
```

---

## 🔧 Troubleshooting

### Problem: "No transcript available"
**Solutions:**
1. ✅ Try a different video (use our recommended list above)
2. ✅ Check if video has captions using diagnostic tool
3. ✅ Enable captions on the video (if you're the creator)
4. ✅ Use YouTube's "Request Transcript" feature

### Problem: "Failed to extract transcript"
**Solutions:**
1. Ensure Ollama is running: `curl http://localhost:11434/api/tags`
2. Check internet connection
3. Try with a different URL format
4. Verify backend is running: `curl http://localhost:8000/health`

### Problem: "Analysis failed" but transcript extracted
**Solutions:**
1. Ollama might not be responding
2. Check backend logs: `tail -50 /tmp/backend.log`
3. Restart Ollama: `ollama serve`
4. Try a shorter video first

---

## 📊 Expected Analysis Output

When successful, you'll get JSON like:
```json
{
  "status": "success",
  "data": {
    "video_id": "eIho2S0ZahI",
    "title": "How to speak so that people want to listen",
    "transcript": [...],
    "summary": {
      "short_summary": "...",
      "bullet_points": [...],
      "key_takeaways": [...]
    },
    "insights": {
      "patterns": [...],
      "implications": [...],
      "action_items": [...]
    },
    "fact_check_results": {...}
  }
}
```

---

## 🎬 Quick Test Video List

| # | Video | URL | Length | Status |
|----|-------|-----|--------|--------|
| 1 | How to Speak (TED) | eIho2S0ZahI | 10m | ✅ Verified |
| 2 | Photosynthesis | G8PgpIcZvzs | 12m | ✅ Verified |
| 3 | Why is π (Veritasium) | BRUvjrjAXwo | 20m | ✅ Verified |
| 4 | [Copy ID to URL] | youtu.be/[ID] | - | Test |

---

## 📝 How to Get Video ID

From URL `https://www.youtube.com/watch?v=eIho2S0ZahI`:
- **Video ID** = `eIho2S0ZahI`
- Paste into: `https://youtu.be/eIho2S0ZahI`

---

## 💡 Pro Tips

1. **Test with TED Talks first** - they have excellent captions
2. **Prefer educational channels** - they usually have captions
3. **Check before analyzing** - use `check_captions.py` script
4. **Shorter videos = faster processing** - start with 5-15 min videos
5. **Cache works** - same video analyzed twice loads from cache faster

---

## 🆘 Still Getting Errors?

1. Run diagnostic: `python3 check_captions.py "<your-url>"`
2. Check backend: `curl http://localhost:8000/health`
3. Verify Ollama: `curl http://localhost:11434/api/tags`
4. Check logs: `tail -100 /tmp/backend.log`
5. Try our test video first: `https://www.youtube.com/watch?v=eIho2S0ZahI`

