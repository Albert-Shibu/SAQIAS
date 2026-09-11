from flask import Flask, render_template, request, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
BASE = Path(__file__).parent
INPUT = BASE / "input"
INPUT.mkdir(exist_ok=True)
ALLOWED = {"png", "jpg", "jpeg", "webp"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify(error="No image uploaded"), 400
    image = request.files["image"]
    if not image.filename or image.filename.rsplit(".", 1)[-1].lower() not in ALLOWED:
        return jsonify(error="Unsupported image"), 400

    path = INPUT / secure_filename(image.filename)
    image.save(path)

    # Replace this demo result with your friend's AI:
    # from vision.measurements import analyze_image
    # return jsonify(analyze_image(str(path)))

    return jsonify(
        absorption=68.4,
        dry=31.6,
        confidence=91.2,
        insight="This idly has absorbed a solid amount of sambar. It's not fully soaked yet, but it's on the way to becoming a sambar legend."
    )

if __name__ == "__main__":
    app.run(debug=True)
