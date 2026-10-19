"""
Quick start script untuk menjalankan Swing Trader IDX
"""
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import pandas
        import yfinance
        import plotly
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\n📦 Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def check_watchlist():
    """Check if watchlist exists"""
    watchlist_path = Path("watchlist.txt")
    if not watchlist_path.exists():
        print("📋 Creating default watchlist...")
        with open(watchlist_path, "w") as f:
            f.write("BBCA\nBBRI\nBMRI\nTLKM\nASII\n")
        print("✅ Default watchlist created!")

def check_env():
    """Check if .env exists"""
    env_path = Path(".env")
    if not env_path.exists():
        print("⚙️ .env file not found. Using default configuration.")
        print("💡 Tip: Copy .env.example to .env and configure your settings.")

def main():
    """Main entry point"""
    print("=" * 60)
    print("🚀 Starting Swing Trader IDX")
    print("=" * 60)
    
    # Check requirements
    print("\n1️⃣ Checking dependencies...")
    if check_requirements():
        print("✅ All dependencies installed")
    
    # Check watchlist
    print("\n2️⃣ Checking watchlist...")
    check_watchlist()
    
    # Check environment
    print("\n3️⃣ Checking configuration...")
    check_env()
    
    # Run streamlit
    print("\n4️⃣ Launching application...")
    print("=" * 60)
    print("🌐 Opening browser at http://localhost:8501")
    print("📌 Press Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "Home.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped. Thank you for using Swing Trader IDX!")

if __name__ == "__main__":
    main()
