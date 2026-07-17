import os
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Uploader</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f4f4f4;
        }

        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            margin-top: 0;
        }

        form {
            margin-bottom: 30px;
        }

        input[type="file"] {
            margin-bottom: 15px;
        }

        button {
            padding: 10px 18px;
            border: none;
            border-radius: 5px;
            background-color: #2563eb;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background-color: #1d4ed8;
        }

        .message {
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            background-color: #fee2e2;
            color: #991b1b;
        }

        ul {
            padding-left: 20px;
        }

        li {
            margin-bottom: 8px;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Upload a File</h1>

        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}

        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <br>
            <button type="submit">Upload</button>
        </form>

        <h2>Uploaded Files</h2>

        {% if files %}
            <ul>
                {% for file in files %}
                    <li>{{ file }}</li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No files have been uploaded.</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if not uploaded_file or uploaded_file.filename == "":
            message = "Please select a file."
        else:
            filename = secure_filename(uploaded_file.filename)

            if not filename:
                message = "Invalid filename."
            else:
                file_path = UPLOAD_DIR / filename
                uploaded_file.save(file_path)

                return redirect(url_for("index"))

    uploaded_files = sorted(
        file.name
        for file in UPLOAD_DIR.iterdir()
        if file.is_file()
    )

    return render_template_string(
        HTML_PAGE,
        files=uploaded_files,
        message=message,
    )


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "upload_directory": str(UPLOAD_DIR),
    }, 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )