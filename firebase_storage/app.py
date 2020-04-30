import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField

# Google cloud storage api
from google.cloud import storage

# Build web form with flask-wtf
class UploadFile(FlaskForm):
    client_file = FileField("File")

# Set env Variables:
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keys/flask-storage-key.json"
os.environ["CLOUD_STORAGE_BUCKET"] = "twib-flask-storage"

# Config Variables
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
CLOUD_STORAGE_BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]

app = Flask(__name__, templates_folder='./templates')
app.config.from_mapping({
    'UPLOAD_FOLDER': UPLOAD_FOLDER,
    'SECRET_KEY': 'my_secret'
})

def allowed_file(filename):
    """Validate file extensions"""
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/to_cloud', methods=['GET', 'POST'])
def to_cloud():
    """Upload file from client to Google Cloud Storage

    Must have GOOGLE_APPLICATION_CREDENTIALS and CLOUD_STORAGE_BUCKET enviornment
    variable set up. Also must grant permission to service account on project to
    allow read/write permission.
    """
    form = UploadFile()

    if form.validate_on_submit():
        # Check if the post request has the file part
        if 'client_file' not in request.files:
            return 'No file uploaded.', 400
        uploaded_file = request.files.get('client_file')
        if uploaded_file.filename == '':
            return 'No file selected.', 400
        if uploaded_file and allowed_file(uploaded_file.filename):
            
            # Create cloud storage client
            gcs = storage.Client()

            # Get the bucket that the file will be uploaded to.
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            # Create a new blob and upload the file's content.
            blob = bucket.blob(secure_filename(uploaded_file.filename))
            blob.upload_from_string(uploaded_file.read(), content_type=uploaded_file.content_type)

            # The public URL can be used to directly access the uploaded file via HTTP.
            return redirect(blob.public_url)
    return render_template('upload.html', form=form)

@app.route('/from_cloud/<filename>')
def from_cloud(filename, url):
    """Server url for file saved on server"""
    return redirect(url)
