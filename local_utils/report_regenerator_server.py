"""Local server for the report regenerator browser UI.

Run from the project root:

    python local_utils/report_regenerator_server.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from flask import Flask, jsonify, request, send_from_directory

from constants import APP_VERSION
import report_from_json as rfj

LOCAL_UTILS = Path(__file__).resolve().parent
app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(LOCAL_UTILS, "report_regenerator.html")


@app.route("/api/version")
def version():
    return jsonify({"app_version": APP_VERSION})


@app.route("/api/regenerate", methods=["POST"])
def regenerate():
    try:
        if request.files:
            uploaded = request.files["file"]
            content = uploaded.read().decode("utf-8")
            filename = uploaded.filename or "report.txt"
        else:
            payload = request.get_json(force=True)
            content = payload["content"]
            filename = payload.get("filename", "report.txt")

        result = rfj.regenerate_report(content)
        return jsonify(
            {
                "text_report": result["text_report"],
                "markdown_report": result["markdown_report"],
                "app_version": result["app_version"],
                "original_app_version": result["original_app_version"],
                "filename": filename,
            }
        )
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Failed to regenerate report: {exc}"}), 500


if __name__ == "__main__":
    print(f"Report Regenerator — tool v{APP_VERSION}")
    print("Open http://127.0.0.1:5001 in your browser")
    app.run(host="127.0.0.1", port=5001, debug=False)
