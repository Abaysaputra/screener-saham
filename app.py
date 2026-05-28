from flask import Flask, jsonify
from pathlib import Path
import os

app = Flask(__name__)

def ensure_watchlist():
    watchlist_path = Path("watchlist.txt")
    if not watchlist_path.exists():
        watchlist_path.write_text("BBCA\nBBRI\nBMRI\nTLKM\nASII\n", encoding="utf-8")
    return watchlist_path

@app.route("/")
def home():
    return jsonify({
        "message": "Swing Trader IDX backend is running on Vercel",
        "status": "ok"
    })

@app.route("/api/health")
def health():
    watchlist_path = ensure_watchlist()
    return jsonify({
        "status": "healthy",
        "watchlist_exists": watchlist_path.exists(),
        "env_loaded": Path(".env").exists(),
        "python_env": os.environ.get("VERCEL", "false")
    })