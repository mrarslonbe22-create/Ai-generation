import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from dotenv import load_dotenv

from modules.script_writer import write_script
from modules.tts_generator import text_to_speech, VOICE_MALE, VOICE_FEMALE
from modules.video_editor import build_video

load_dotenv()

app = Flask(__name__)
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    topic = request.form.get("topic", "").strip()
    voice_choice = request.form.get("voice", "male")
    orientation = request.form.get("orientation", "vertical")
    gameplay_file = request.files.get("gameplay")

    if not topic:
        return jsonify({"error": "Mavzu kiritilmagan"}), 400
    if not gameplay_file:
        return jsonify({"error": "Gameplay video yuklanmagan"}), 400

    job_id = uuid.uuid4().hex[:8]
    job_out_dir = os.path.join(OUTPUT_DIR, job_id)
    os.makedirs(job_out_dir, exist_ok=True)

    gameplay_path = os.path.join(UPLOAD_DIR, f"{job_id}_gameplay.mp4")
    gameplay_file.save(gameplay_path)

    # 1-BOSQICH: skript yozish
    script = write_script(topic, style="gaming")
    with open(os.path.join(job_out_dir, "script.txt"), "w", encoding="utf-8") as f:
        f.write(script)

    # 2-BOSQICH: ovoz + subtitr
    voice = VOICE_MALE if voice_choice == "male" else VOICE_FEMALE
    audio_path, subs_path = text_to_speech(script, job_out_dir, voice=voice)

    # 3-BOSQICH: montaj
    resolution = (1080, 1920) if orientation == "vertical" else (1920, 1080)
    final_path = os.path.join(job_out_dir, "final_video.mp4")
    build_video(gameplay_path, audio_path, subs_path, final_path, resolution=resolution)

    return jsonify(
        {
            "job_id": job_id,
            "script": script,
            "video_url": f"/download/{job_id}",
        }
    )


@app.route("/download/<job_id>")
def download(job_id):
    path = os.path.join(OUTPUT_DIR, job_id, "final_video.mp4")
    return send_file(path, as_attachment=True, download_name=f"video_{job_id}.mp4")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
