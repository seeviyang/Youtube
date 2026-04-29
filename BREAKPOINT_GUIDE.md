# 🎯 Breakpoint Debugging - Complete Setup Guide

## ✅ What Changed

Your breakpoints weren't working because:
1. **Module launching issue** - Using `"module": "backend.src.main"` doesn't support breakpoints well with FastAPI/Uvicorn
2. **Uvicorn foreground mode** - Needs to run synchronously for debugger to attach
3. **Import path issues** - Relative imports weren't working from debugger

## 🟢 NOW FIXED!

### What Was Updated:

1. **launch.json** - Now uses `debug_backend.py` instead of module launching
2. **debug_backend.py** - New debug-friendly entry point (created)
3. **backend/src/main.py** - Updated imports to work with debugger

---

## 🚀 How to Use Breakpoints Now

### Step 1: Open Python File in Backend
Open any file in the backend folder:
- `backend/src/main.py`
- `backend/src/agents/transcript_extractor.py`
- `backend/src/orchestrator.py`
- `backend/src/agents/summarizer.py`
- etc.

### Step 2: Add Breakpoint
Click on the **line number** where you want to pause execution.
- A **red dot** 🔴 will appear
- This is your breakpoint

**Example locations:**
```python
# In backend/src/main.py (line 55)
async def analyze_video(request: AnalysisRequest):
    # Add breakpoint here to see request object
    logger.info(f"Analyzing video: {request.url}")
    
# In backend/src/agents/transcript_extractor.py (line 90)
result = self._extract_captions(info, lang_priority)
# Add breakpoint here to inspect captions
```

### Step 3: Start Debugging
Press **F5** (or ⇧⌘D → Select "🐍 Debug Backend API")

You should see:
```
🎬 YouTube Backend Debugger
✅ Breakpoints ENABLED
Starting API Server...
Waiting for breakpoints or requests...
```

### Step 4: Trigger Breakpoint
Make an API request to hit the breakpoint:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

The debugger will **pause** at your breakpoint! ⏸️

### Step 5: Step Through Code
Use these keyboard shortcuts:

| Shortcut | Action | Purpose |
|----------|--------|---------|
| **F10** | Step Over | Execute current line, move to next |
| **F11** | Step Into | Enter function/method |
| **⇧F11** | Step Out | Exit current function |
| **F5** | Continue | Resume execution to next breakpoint |
| **⌘K⌘I** | Toggle | Add/remove breakpoint |

### Step 6: Inspect Variables
When paused, look at the **Variables** panel on the left:
- **Locals** - Variables in current function
- **Globals** - Global variables
- **Statics** - Class variables

Hover over any variable in code to see its value!

---

## 🎬 Real Debugging Example

### Goal: Debug what happens when transcripts are extracted

**File**: `backend/src/agents/transcript_extractor.py`

1. **Open the file** in VS Code

2. **Find this code** (around line 90):
```python
def extract_transcript(self, video_id: str, video_info: dict) -> dict:
    """Extract transcript from video"""
    result = self._extract_captions(info, lang_priority)  # ← Add breakpoint HERE
    return result
```

3. **Click line 90** to add red breakpoint dot 🔴

4. **Press F5** to start debugging
   - Terminal shows: `✅ Breakpoints ENABLED`
   - Terminal shows: `Waiting for breakpoints or requests...`

5. **In another terminal**, run:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

6. **VS Code pauses** at your breakpoint ⏸️
   - Yellow highlight shows current line
   - Variables panel shows local variables
   - You can hover over variables to see values

7. **Step through code**:
   - Press **F10** to go line by line
   - Press **F11** to enter the `_extract_captions()` function
   - Watch the Variables panel update

8. **Inspect data**:
   - Hover over `info` to see video metadata
   - Hover over `result` to see extracted captions
   - Expand objects in Variables panel

9. **Continue**:
   - Press **F5** to resume
   - API completes and returns JSON response

---

## 🔍 Useful Breakpoint Locations

### API Entry Points
- `backend/src/main.py:55` - `analyze_video()` function
  - See the incoming request
- `backend/src/main.py:85` - `analyze_video()` after orchestrator
  - See the final result

### Transcript Extraction
- `backend/src/agents/transcript_extractor.py:90` - After `_extract_captions()`
  - See extracted captions
- `backend/src/agents/transcript_extractor.py:210` - Inside `_parse_captions()`
  - See JSON parsing
- `backend/src/agents/transcript_extractor.py:230` - After caption parsing
  - See final transcript segments

### Summarization
- `backend/src/agents/summarizer.py:40` - Inside `summarize()`
  - See LLM input prompt
- `backend/src/agents/summarizer.py:55` - After LLM call
  - See LLM output

### Orchestrator
- `backend/src/orchestrator.py:51` - After transcript extraction
- `backend/src/orchestrator.py:59` - After summarization
- `backend/src/orchestrator.py:93` - Before final result

---

## 🆘 Troubleshooting

### ❌ "Breakpoint not bound"
**Solution**: Make sure you:
1. Have a **Python file** open (not frontend/app.js)
2. Set breakpoint in a file in the `backend/` folder
3. Are using the **🐍 Debug Backend API** config
4. Press F5 AFTER adding the breakpoint

### ❌ "Debugger doesn't pause"
**Try**:
1. Stop debugger (press ⇧F5)
2. Kill the process: `pkill -f debug_backend.py`
3. Delete breakpoint and re-add it
4. Press F5 again
5. Make a fresh API request

### ❌ "ImportError: cannot import name"
**Solution**:
1. Make sure `PYTHONPATH` is set: `export PYTHONPATH=/Users/viyangchaudhari/Projects/youtube`
2. Stop and restart debugger
3. Or use: `python3 -m backend.src.main`

### ❌ "Port 8000 already in use"
**Kill existing process**:
```bash
lsof -i :8000
# Find the PID, then:
kill -9 <PID>
```

---

## 📚 Debug Keyboard Shortcuts (Complete List)

### Execution Control
- **F5** - Continue / Play
- **F6** - Pause
- **F10** - Step Over (next line)
- **F11** - Step Into (enter function)
- **⇧F11** - Step Out (exit function)
- **⌘F5** - Restart
- **⇧F5** - Stop debugging

### Breakpoints
- **⌘K⌘I** - Toggle breakpoint on current line
- **⌘K⇧⌘I** - Toggle conditional breakpoint (with condition)
- **⌘⇧B** - Open Breakpoints panel

### Debugging Panels
- **⇧⌘D** - Open Debug panel
- **⌘⇧Y** - Open Debug console

### Variable Inspection
- Hover over variable to see value (inline preview)
- Click Variables panel to expand objects
- Click Debug Console to evaluate expressions

---

## 💡 Pro Tips

### Conditional Breakpoints
Right-click on breakpoint dot → "Edit Breakpoint" → Add condition:
```
len(segments) > 0
result is not None
video_id == "dQw4w9WgXcQ"
```

### Logpoints (Don't pause, just log)
Right-click on line → "Add Logpoint" → Enter message:
```
Extracting captions for {video_id}: {info}
```

### Debug Console Expressions
While paused, click the Debug Console tab and type:
```python
len(segments)
result['transcript']
info.get('title')
```

### Watch Expressions
Click Variables panel → "+" button → Enter expression:
```
len(segments)
type(result)
result.keys()
```

---

## 🎉 Next Steps

1. **Try it now**:
   - Open `backend/src/main.py`
   - Click line 60 (inside `analyze_video`)
   - Press F5
   - In another terminal: `curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'`
   - Watch it pause! 🎊

2. **Debug the whole pipeline**:
   - Add breakpoints at: transcript extraction, summarization, insights, fact-checking
   - Step through each stage
   - Watch the data transform at each step

3. **Create conditional breakpoints**:
   - Only break when specific conditions are met
   - Perfect for debugging specific videos or edge cases

4. **Use Debug Console**:
   - Evaluate expressions
   - Call functions
   - Inspect complex objects

---

## 📞 Questions?

If breakpoints still don't work:
1. Verify Python environment: `which python3`
2. Check VS Code Python extension is installed
3. Try running: `python3 debug_backend.py` manually first
4. Then attach debugger with F5

Happy debugging! 🚀
