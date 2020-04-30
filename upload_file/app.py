import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField

# Build web form with flask-wtf
class CoverImage(FlaskForm):
    cover_img = FileField("Cover Image")

# Config Variables
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_mapping({
    'UPLOAD_FOLDER': UPLOAD_FOLDER,
    'SECRET_KEY': 'my_secret'
})

def allowed_file(filename):
    """Validate file extensions"""
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/to_server', methods=['GET', 'POST'])
def to_server():
    """upload file from client to server"""
    form = CoverImage()

    if form.validate_on_submit():
        # Check if the post request has the file part
        if 'cover_img' not in request.files:
            return 'No file uploaded.', 400
        uploaded_file = request.files.get('cover_img')
        if uploaded_file.filename == '':
            return 'No file selected.', 400
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('from_server', filename=filename))
    
    return render_template('index.html', form=form)

@app.route('/from_server/<filename>')
def from_server(filename):
    """Server url for file saved on server"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


