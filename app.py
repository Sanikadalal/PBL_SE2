from flask import Flask, render_template, request, url_for, redirect
import os
from deeplearning import OCR
from werkzeug.utils import secure_filename
# webserver gateway interface
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(
    BASE_PATH, './static/upload')


@app.route("/")
def index():
    return render_template('index.html')
    
@app.route("/docker")
def docker():
    return render_template("docker.html")

@app.route('/nameplate_detection', methods=['POST', 'GET'])
def nameplate_detection():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)
        text = OCR(path_save, filename)

        return render_template('nameplate_detection.html', upload=True, upload_image=filename, text=text)
    return render_template('nameplate_detection.html', upload=False)
    



@app.route("/teams")
def team():
    return render_template("team.html")

@app.route("/vehicle_detection")
def vehicle_detection():
    return render_template("vehicle_detection.html")

@app.route("/vehicle_result")
def vehicle_result():
    return render_template("vehicle_result.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = '/root/Kubernetes-Python-CGI/Files/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'Please Select Image File Only'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No File Selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cmd = f"python3 -W ignore test.py {filename}"
            print(cmd)
            o = subprocess.getoutput(cmd)
            print(o)
            return(o)


if __name__ == "__main__":
    app.run(debug=True)