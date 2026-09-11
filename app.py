from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
from werkzeug.utils import secure_filename
import shutil

from Detection import detect_image

app = Flask(__name__)

BASE = Path(__file__).parent
INPUT = BASE / "input"
OUTPUT = BASE / "output"

INPUT.mkdir(exist_ok=True)
OUTPUT.mkdir(exist_ok=True)

ALLOWED = {"png", "jpg", "jpeg", "webp"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():

    # ========================================================
    # CHECK IMAGE
    # ========================================================

    if "image" not in request.files:
        return jsonify(error="No image uploaded"), 400

    image = request.files["image"]

    if not image.filename:
        return jsonify(error="No image selected"), 400

    extension = image.filename.rsplit(".", 1)[-1].lower()

    if extension not in ALLOWED:
        return jsonify(error="Unsupported image"), 400


    # ========================================================
    # CLEAR OLD INPUT
    # ========================================================

    for item in INPUT.iterdir():

        if item.is_file():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)


    # ========================================================
    # CLEAR OLD OUTPUT
    # ========================================================

    for item in OUTPUT.iterdir():

        if item.is_file():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)


    # ========================================================
    # SAVE UPLOADED IMAGE
    # ========================================================

    filename = secure_filename(image.filename)

    input_path = INPUT / filename

    image.save(input_path)


    # ========================================================
    # RUN DETECTION
    # ========================================================

    result = detect_image(input_path)


    if not result["success"]:

        return jsonify(
            error=result["error"]
        ), 400


    # ========================================================
    # SEND RESULT TO JAVASCRIPT
    # ========================================================

    return jsonify({

        # Output image
        "image": "/output/detected_result.jpg",

        # Preset
        "image_key": result["image_key"],

        # Detection
        "idli_count": result["idli_count"],
        "sambar_detected": result["sambar_detected"],

        # Sambar absorption
        "absorption": result["absorption"],

        # Demo confidence
        "confidence": result["confidence"]

    })


# ============================================================
# OUTPUT IMAGE
# ============================================================

@app.route("/output/<filename>")
def output_file(filename):

    return send_from_directory(
        OUTPUT,
        filename
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)