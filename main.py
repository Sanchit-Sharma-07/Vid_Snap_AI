# main.py
# Flask server to upload images and text, generate input.txt for reels

from flask import Flask, render_template, request
import uuid
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    # Home page
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    # Generate a unique ID for this upload session
    myid = str(uuid.uuid1())
    
    if request.method == "POST":
        rec_id = request.form.get("uuid") or myid  # Use UUID from form or generate new
        desc = request.form.get("text")
        input_files = []

        print(rec_id, desc)

        # Create folder for this upload
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(folder_path, exist_ok=True)

        # Save uploaded images
        for key, file in request.files.items():
            if file and file.filename:
                filename = secure_filename(file.filename)
                save_path = os.path.join(folder_path, filename)
                file.save(save_path)
                input_files.append(filename)

        # Save description text as desc.txt
        if desc:
            with open(os.path.join(folder_path, "desc.txt"), "w") as f:
                f.write(desc)

        # Create input.txt for ffmpeg (overwrite each time)
        input_txt_path = os.path.join(folder_path, "input.txt")
        with open(input_txt_path, "w") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\n")
                f.write("duration 1\n")  # Display each image for 1 second

    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    # Show all generated reels in gallery
    reels = os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels=reels)

if __name__ == "__main__":
    app.run(debug=True)
