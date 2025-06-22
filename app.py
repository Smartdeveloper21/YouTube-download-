from flask import Flask, render_template, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)

        try:
            subprocess.run([
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                "-o", output_path,
                url
            ], check=True)

            if os.path.exists(output_path):
                return send_file(output_path, as_attachment=True)
            else:
                return "Download failed: File not created."
        except Exception as e:
            return f"Download error: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
