import os
import sys
import json
import logging
import traceback
import numpy as np
from subprocess import run, CalledProcessError
import torch
import imageio_ffmpeg
from flask import Flask, render_template, request, jsonify, send_file, Response
import whisper
import whisper.audio as _whisper_audio

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Patch whisper to use bundled ffmpeg (絕對路徑，不依賴 PATH) ────────────────
_ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
log.info(f"ffmpeg binary : {_ffmpeg_exe}")
log.info(f"ffmpeg exists : {os.path.isfile(_ffmpeg_exe)}")
log.info(f"CUDA available: {torch.cuda.is_available()}")

def _load_audio(file: str, sr: int = _whisper_audio.SAMPLE_RATE):
    cmd = [
        _ffmpeg_exe, "-nostdin", "-threads", "0",
        "-i", file,
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(sr),
        "-",
    ]
    try:
        out = run(cmd, capture_output=True, check=True).stdout
    except CalledProcessError as e:
        raise RuntimeError(f"ffmpeg error: {e.stderr.decode()}") from e
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

_whisper_audio.load_audio = _load_audio
log.info("whisper.audio.load_audio patched with bundled ffmpeg")

# 支援 PyInstaller 打包後的路徑
if getattr(sys, "frozen", False):
    _BASE = os.path.dirname(sys.executable)
    app = Flask(__name__, template_folder=os.path.join(_BASE, "templates"))
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(_BASE, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
log.info(f"Upload folder : {UPLOAD_FOLDER}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    log.info(f"Uploaded: {filepath} (exists={os.path.isfile(filepath)}, size={os.path.getsize(filepath)} bytes)")

    return jsonify({"success": True, "filename": filename})


@app.route("/transcribe/<filename>", methods=["POST"])
def transcribe_video(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    log.info(f"Transcribe request: {filepath}")
    log.info(f"  File exists : {os.path.isfile(filepath)}")

    if not os.path.isfile(filepath):
        log.error(f"  File not found: {filepath}")
        return jsonify({"error": "File not found"}), 404

    data = request.get_json() or {}
    model_size = data.get("model", "base")
    language = data.get("language") or None
    log.info(f"  Model={model_size}  Language={language}  FP16={torch.cuda.is_available()}")

    try:
        log.info("  Loading Whisper model...")
        model = whisper.load_model(model_size)
        log.info("  Model loaded. Starting transcription...")

        options = {"fp16": torch.cuda.is_available()}
        if language:
            options["language"] = language

        result = model.transcribe(filepath, **options)
        log.info(f"  Transcription done. Detected language: {result['language']}, segments: {len(result['segments'])}")

        segments = [
            {
                "id": seg["id"],
                "start": round(seg["start"], 3),
                "end": round(seg["end"], 3),
                "text": seg["text"].strip(),
            }
            for seg in result["segments"]
        ]

        return jsonify({"success": True, "language": result["language"], "segments": segments})

    except Exception as e:
        log.error(f"  Transcription failed: {e}")
        log.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/export_srt/<filename>", methods=["POST"])
def export_srt(filename):
    data = request.get_json() or {}
    segments = data.get("segments", [])

    def seconds_to_srt_time(s):
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = s % 60
        return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")

    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{seconds_to_srt_time(seg['start'])} --> {seconds_to_srt_time(seg['end'])}")
        lines.append(seg["text"])
        lines.append("")

    srt_content = "\n".join(lines)
    base = os.path.splitext(filename)[0]

    return Response(
        srt_content,
        mimetype="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{base}.srt"'},
    )


@app.route("/video/<filename>")
def serve_video(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(filepath, conditional=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
