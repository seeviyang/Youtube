# 🐛 YouTube Analysis System - Debugging Guide

## Quick Start

### Option 1: VS Code Debugger (Easiest)

1. **Open VS Code** and go to the Debug panel (⇧⌘D)
2. **Select a debug configuration** from the dropdown:
   - "Debug Backend API" - Debug the full server
   - "Debug Transcript Extraction" - Debug transcript extraction
   - "Debug API Analysis" - Debug the analysis pipeline
   - "Python: Current File" - Debug any Python file

3. **Set breakpoints** by clicking on line numbers (red dot appears)
4. **Press F5** or click "Start Debugging" button
5. **Use the debugger controls**:
   - ▶️ Continue (F5)
   - ⏸️ Pause (F6)
   - ↳ Step Over (F10)
   - ↙️ Step Into (F11)
   - ↰️ Step Out (⇧F11)

### Option 2: Command Line with pdb (More Control)

```bash
# Run debug script with interactive debugging
python debug_transcript_extractor.py

# When breakpoint hits, you'll see (Pdb) prompt
# Use pdb commands below...
```

### Option 3: Run with pdb directly

```bash
# Debug any Python file
python -m pdb backend/src/agents/transcript_extractor.py

# Or add breakpoint in code and run normally
python debug_api.py
```

---

## Debugging Commands (pdb)

When you hit a breakpoint, you get a `(Pdb)` prompt. Use these commands:

### Navigation
```
n        Next line (step over)
s        Step into function
c        Continue execution
l        List current code (10 lines)
ll       List entire function
w        Show stack (where you are)
u        Up one level in stack
d        Down one level in stack
```

### Inspection
```
p variable           Print variable value
pp variable          Pretty-print (nice format)
p locals()          Print all local variables
p dir(object)       Print all attributes of object
p type(variable)    Print type of variable
p len(variable)     Print length (for lists/dicts)
```

### Breakpoints
```
b 42                 Set breakpoint at line 42
b function_name      Set breakpoint at function
cl 1                 Clear breakpoint 1
cl                   Clear all breakpoints
```

### Execution
```
c                    Continue to next breakpoint
l                    List current location
h                    Help menu
q                    Quit debugger
```

### Example Session
```python
(Pdb) p result
{'video_id': 'dQw4w9WgXcQ', 'title': 'Rick Astley...', ...}

(Pdb) p len(result['transcript'])
61

(Pdb) p result['transcript'][0]
TranscriptSegment(timestamp='00:00:01', seconds=1.36, text='[🎵🎵🎵]')

(Pdb) pp result['summary']
{'short_summary': '...', 'bullet_points': [...], ...}

(Pdb) c
```

---

## Debugging Specific Components

### Debug Transcript Extraction

**File**: `backend/src/agents/transcript_extractor.py`

**Breakpoints to add**:
```python
# Line 89: After info extraction
transcript = self._extract_captions(info)
import pdb; pdb.set_trace()  # 🔴 What did _extract_captions return?

# Line 210: Inside _parse_captions
caption_url = captions[0]['url']
import pdb; pdb.set_trace()  # 🔴 Inspect URL structure

# Line 227: After downloading captions
caption_json = json.loads(caption_data)
import pdb; pdb.set_trace()  # 🔴 Check JSON structure
```

**Run with VS Code**:
1. Open `backend/src/agents/transcript_extractor.py`
2. Click on line number to add breakpoint
3. Go to Debug → Run "Debug Transcript Extraction"
4. Hit breakpoint, inspect variables

### Debug API Pipeline

**File**: `backend/src/orchestrator.py`

**Key breakpoints**:
```python
# Line 51: After transcript extraction
transcript_data = self.transcript_extractor.extract(youtube_url)
import pdb; pdb.set_trace()  # 🔴 Check transcript_data structure

# Line 59: After summary generation
summary = self.summarizer.summarize(transcript_text)
import pdb; pdb.set_trace()  # 🔴 Check summary object

# Line 93: After compilation
analysis_result = {...}
import pdb; pdb.set_trace()  # 🔴 Check final result
```

### Debug Serialization Issues

**File**: `backend/src/main.py`

```python
# Line 116: Check what fails to serialize
try:
    json.dumps(result, default=str)
except Exception as e:
    import pdb; pdb.set_trace()  # 🔴 Inspect result that can't serialize
    print(f"Failed to serialize: {e}")
```

---

## Common Debugging Scenarios

### Scenario 1: "No transcript available" Error

**Steps**:
1. Run `debug_transcript_extractor.py`
2. Choose option 2 (Caption Download)
3. Hit breakpoint at `import pdb; pdb.set_trace()`
4. Inspect caption structure:
   ```
   (Pdb) p caption  # See what's in caption dict
   (Pdb) p caption['url']  # Check if URL exists
   ```
5. If URL exists, test download:
   ```python
   import urllib.request, ssl, json
   ssl_context = ssl.create_default_context()
   ssl_context.check_hostname = False
   ssl_context.verify_mode = ssl.CERT_NONE
   
   response = urllib.request.urlopen(caption['url'], context=ssl_context, timeout=5)
   data = json.loads(response.read().decode('utf-8'))
   p len(data.get('events', []))  # Should be > 0
   ```

### Scenario 2: "JSON Serialization" Error

**Steps**:
1. Run `debug_api.py`
2. Choose option 1 (Full Analysis)
3. Let it fail on serialization
4. When breakpoint hits, inspect result:
   ```
   (Pdb) p type(result)  # Check type
   (Pdb) p result.keys()  # Check top-level keys
   (Pdb) p type(result['summary'])  # Check each field
   (Pdb) p hasattr(result['summary'], 'dict')  # Pydantic method?
   ```

### Scenario 3: Slow/Hanging Analysis

**Steps**:
1. Run `debug_api.py` with option 1
2. When it seems to hang, press Ctrl+C
3. You'll get a stack trace showing where it's stuck
4. Add breakpoint before that location
5. Inspect variables at that point

```bash
# Run with verbose output
python -u debug_api.py  # -u = unbuffered output
```

---

## Debugging Tips

### 1. **Print Debugging (Quick)**
```python
print(f"DEBUG: variable = {variable}")
print(f"DEBUG: type = {type(variable)}")
print(f"DEBUG: dir = {dir(variable)}")

# For lists/dicts:
import json
print(json.dumps(variable, indent=2, default=str))
```

### 2. **Conditional Breakpoints** (VS Code)
Right-click breakpoint → Edit Breakpoint → Add condition:
```
len(result['transcript']) == 0
```

### 3. **Logpoints** (VS Code)
Right-click line → Logpoint → Add message:
```
transcript_length={len(result['transcript'])}
```

### 4. **Watch Expressions** (VS Code)
In Debug panel, add to Watch section:
```
len(segments)
result['metadata']['title']
summary.bullet_points[0]
```

### 5. **Call Stack Navigation**
When at breakpoint, look at left panel "Call Stack" to see:
- Which function you're in
- What called it
- Click to jump up the stack

---

## Debugging the API Server

### Debug while server is running

**Terminal 1**: Start backend
```bash
cd /Users/viyangchaudhari/Projects/youtube
python3 -m backend.src.main
```

**Terminal 2**: Add breakpoint to code, then restart terminal 1:
```python
# In main.py or orchestrator.py, add:
import pdb; pdb.set_trace()
```

**Terminal 3**: Make API request
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

Execution will pause in Terminal 1 at breakpoint!

---

## Useful Debugging Patterns

### Pattern 1: Inspect Complex Objects
```python
(Pdb) from pprint import pprint
(Pdb) pprint(result)
```

### Pattern 2: Step Through Loop
```python
(Pdb) n  # Next iteration
(Pdb) n  # Keep pressing n to step through
```

### Pattern 3: Edit and Continue
```python
(Pdb) !variable = 42  # Use ! to execute Python code
(Pdb) !result['key'] = 'new_value'
```

### Pattern 4: Post-Mortem Debugging
```python
# After exception, drop into debugger:
try:
    something()
except Exception as e:
    import pdb; pdb.post_mortem()
```

### Pattern 5: Debug with Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Variable: {variable}")
```

---

## Quick Reference: What to Debug

| Component | File | Start Here |
|-----------|------|-----------|
| Transcript Extraction | `backend/src/agents/transcript_extractor.py` | Line 89 in `extract()` |
| Caption Download | `backend/src/agents/transcript_extractor.py` | Line 210 in `_parse_captions()` |
| Summarization | `backend/src/agents/summarizer.py` | Line 40 in `summarize()` |
| Insights | `backend/src/agents/insight_generator.py` | Line 50 in `generate_insights()` |
| Fact-checking | `backend/src/agents/fact_checker.py` | Line 60 in `check_facts()` |
| API Response | `backend/src/main.py` | Line 116 in `/analyze` endpoint |
| Orchestration | `backend/src/orchestrator.py` | Line 51 in `analyze()` |

---

## Troubleshooting

**Q: Breakpoint not working?**
A: Make sure `justMyCode` is disabled in launch.json, or set it to `false`

**Q: Debugger too slow?**
A: Use "Debug Console" instead of integrated terminal, or reduce variables watched

**Q: Can't see variable values?**
A: Try `print()` statements instead, or use `pp` command in pdb

**Q: Want to modify code while debugging?**
A: Edit the file, then use `!reload()` in pdb (Python 3 only)

---

## Next Steps

1. **Choose a component** from the table above
2. **Open the file** in VS Code
3. **Add a breakpoint** by clicking line number
4. **Run debug configuration** (F5)
5. **Inspect variables** when breakpoint hits
6. **Step through code** with F10/F11
7. **Check Call Stack** to understand flow

Happy debugging! 🔍
