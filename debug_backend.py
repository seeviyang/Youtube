#!/usr/bin/env python3
"""
🐍 Backend Debugger - Breakpoint-friendly version
This script runs the backend in a way that plays nicely with VS Code debugger.
"""

import sys
import os

# Set up Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import and run
if __name__ == "__main__":
    from backend.src.main import app, config
    import uvicorn
    
    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║  🐍 YouTube Backend Debugger                          ║
    ║  ✅ Breakpoints ENABLED                               ║
    ║  🔴 Set breakpoints by clicking line numbers          ║
    ╚════════════════════════════════════════════════════════╝
    
    Starting API Server...
    Host: {config.API_HOST}
    Port: {config.API_PORT}
    
    📚 Documentation: http://localhost:{config.API_PORT}/docs
    
    Waiting for breakpoints or requests...
    """)
    
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="info",
        reload=False,
        access_log=True
    )
