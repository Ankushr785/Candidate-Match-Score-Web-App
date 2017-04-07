import os
from flask import Flask, request, redirect, url_for, make_response, flash, current_app
from werkzeug.utils import secure_filename
import candidate_match_score

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        pastExp = request.form['past_exp']
        corpus = request.form['job_posting_keywords']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser may
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            csv_output = candidate_match_score.processData(filepath, pastExp, corpus)
            response = make_response(csv_output)
            response.headers["Content-Disposition"] = "attachment; filename=output.csv"
            return response 
    return current_app.send_static_file('index.html')

@app.route('/static/<path:filename>')
def send_static(filename):
    return current_app.send_static_file(filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
