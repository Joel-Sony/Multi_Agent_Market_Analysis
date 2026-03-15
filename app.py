"""
Flask Web Application — Dashboard & API endpoints.

Serves a premium dark-themed dashboard and exposes REST API
endpoints for dataset statistics, analysis execution, and
report management.
"""

import os
import sys
import json
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename

from config import OUTPUT_DIR, FLASK_HOST, FLASK_PORT, UPLOAD_DIR
from rag.pipeline import get_dataset_stats, set_active_dataset
from crew import run_analysis

# Support for PyInstaller built executable
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

# ── In-memory analysis state ──────────────────────────────────────
analysis_state = {
    "running": False,
    "progress": "",
    "result": None,
    "error": None,
}


# ── Routes ────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """Serve the main dashboard page."""
    return render_template("index.html")


@app.route("/api/dataset-stats")
def dataset_stats():
    """Return dataset statistics as JSON."""
    try:
        stats = get_dataset_stats()
        # Add filename default for the frontend
        from config import DATASET_PATH
        from rag.pipeline import ACTIVE_DATASET_PATH
        stats["filename"] = os.path.basename(ACTIVE_DATASET_PATH) if ACTIVE_DATASET_PATH else os.path.basename(DATASET_PATH)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/upload-dataset", methods=["POST"])
def upload_dataset():
    """Handle custom CSV file uploads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)
        
        try:
            # Update the rag pipeline to point to this new dataset
            set_active_dataset(filepath)
            
            # Get new stats to confirm and return to frontend
            stats = get_dataset_stats()
            stats["filename"] = filename
            return jsonify(stats)
            
        except Exception as e:
            return jsonify({"error": f"Failed to process CSV: {str(e)}"}), 500
            
    return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400


@app.route("/api/analyze", methods=["POST"])
def start_analysis():
    """Start background analysis. Body: { "query": "..." }"""
    if analysis_state["running"]:
        return jsonify({"error": "Analysis already in progress"}), 409

    data = request.get_json(silent=True) or {}
    query = data.get("query", "customer complaints, positive feedback, and product quality")

    def background_task():
        analysis_state["running"] = True
        analysis_state["progress"] = "Initializing RAG pipeline..."
        analysis_state["result"] = None
        analysis_state["error"] = None
        try:
            result = run_analysis(query)
            analysis_state["result"] = result
            analysis_state["progress"] = "Complete"
        except Exception as e:
            analysis_state["error"] = str(e)
            analysis_state["progress"] = "Failed"
        finally:
            analysis_state["running"] = False

    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()

    return jsonify({"status": "started", "query": query})


@app.route("/api/analysis-status")
def analysis_status():
    """Check the current analysis status."""
    return jsonify({
        "running": analysis_state["running"],
        "progress": analysis_state["progress"],
        "has_result": analysis_state["result"] is not None,
        "error": analysis_state["error"],
    })


@app.route("/api/analysis-result")
def analysis_result():
    """Get the latest analysis result."""
    if analysis_state["result"] is None:
        return jsonify({"error": "No analysis result available"}), 404
    return jsonify(analysis_state["result"])


@app.route("/api/reports")
def list_reports():
    """List all saved reports."""
    reports = []
    if os.path.exists(OUTPUT_DIR):
        for fname in sorted(os.listdir(OUTPUT_DIR), reverse=True):
            if fname.endswith(".md"):
                fpath = os.path.join(OUTPUT_DIR, fname)
                stat = os.stat(fpath)
                reports.append({
                    "name": fname,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
    return jsonify(reports)


@app.route("/api/reports/<name>")
def get_report(name):
    """Read a specific saved report."""
    fpath = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(fpath):
        return jsonify({"error": "Report not found"}), 404
    with open(fpath) as f:
        content = f.read()
    return jsonify({"name": name, "content": content})


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
