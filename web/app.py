from flask import Flask, request, render_template, url_for, redirect
import os
from werkzeug.utils import secure_filename
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.Dog_Detector import classify_image
from scripts.dog_breeds_info import get_breed_info, get_all_breeds

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = os.path.join('web', 'static', 'uploads')
BREED_IMAGES_FOLDER = os.path.join('web', 'static', 'breed_images')

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BREED_IMAGES_FOLDER, exist_ok=True)

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

    breeds_list = get_all_breeds()
    return render_template("index.html", filename=filename, result=result, breeds_list=breeds_list)

@app.route("/search", methods=["GET", "POST"])
def search_breed():
    if request.method == "POST":
        breed_name = request.form.get("breed_name")
        if not breed_name:
            return redirect(url_for("upload_file"))
        
        # Get the breed information from your dog_breeds_info module
        breed_info = get_breed_info(breed_name)
        
        if not breed_info:
            return render_template("index.html", search_error=f"No information found for breed: {breed_name}", 
                                  breeds_list=get_all_breeds())
        
        # Check if we have an image for this breed
        breed_image = f"{breed_name.lower().replace(' ', '_')}.jpg"
        image_path = os.path.join(BREED_IMAGES_FOLDER, breed_image)
        
        # If we don't have an image for this breed, use a placeholder
        if not os.path.exists(image_path):
            breed_image = "placeholder_dog.jpg"
        
        search_result = {
            "breed": breed_name,
            "image": breed_image,
            "description": breed_info["description"],
            "origin": breed_info["origin"],
            "life_span": breed_info["life_span"],
            "temperament": breed_info["temperament"],
            "height": breed_info["height"],
            "weight": breed_info["weight"],
            "colors": breed_info["colors"]
        }
        
        return render_template("index.html", search_result=search_result, breeds_list=get_all_breeds())
    
    return redirect(url_for("upload_file"))

if __name__ == "__main__":
    app.run(debug=True)