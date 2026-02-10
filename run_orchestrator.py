"""
Quick start script for the orchestrator
"""
import uvicorn
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("="*60)
    print("🚀 Starting AI Memory System Orchestrator")
    print("="*60)
    print("\n📍 Server will be available at:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Health: http://localhost:8000/health")
    print("   - Metrics: http://localhost:8000/metrics")
    print("\n⚡ Press CTRL+C to stop the server\n")
    print("="*60 + "\n")
    
    uvicorn.run(
        "orchestrator.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
