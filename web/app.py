from flask import Flask, request, render_template, url_for
import os
from werkzeug.utils import secure_filename
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.Dog_Detector import classify_image

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = os.path.join('web', 'static', 'uploads')

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    result = None
    filename = None
    breed_info = None
    
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file section!")
        
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No images selected!")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            try:
                result = classify_image(filepath)
            except Exception as e:
                return render_template("index.html", error=f"Lỗi khi xử lý ảnh: {str(e)}")

    return render_template("index.html", filename=filename, result=result)

if __name__ == "__main__":
    app.run(debug=True)