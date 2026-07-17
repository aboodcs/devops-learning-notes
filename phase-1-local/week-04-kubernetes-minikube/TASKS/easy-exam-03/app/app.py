import os
from pathlib import Path
from flask import Flask, request, redirect, url_for, render_template_string, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Easy Exam 03 - File Upload</title>
</head>
<body>
    <h1>File Upload App</h1>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>

    <h2>Uploaded Files</h2>
    <ul>
        {% for file in files %}
            <li>{{ file }}</li>
        {% else %}
            <li>No files uploaded yet.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    files = sorted([file.name for file in UPLOAD_DIR.iterdir() if file.is_file()])
    return render_template_string(PAGE, files=files)

@app.route("/", methods=["POST"])
def upload_file():
    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return redirect(url_for("index"))

    filename = secure_filename(uploaded_file.filename)
    file_path = UPLOAD_DIR / filename
    uploaded_file.save(file_path)

    return redirect(url_for("index"))

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="healthy"), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)