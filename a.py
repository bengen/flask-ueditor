from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import json
import pymongo
conn = pymongo.Connection('localhost:5430')
db = conn.test

app = Flask(__name__)

@app.route('/')
def index():
    contents = db.ueditor.find()
    return render_template('index.html', contents=contents)

@app.route('/add/', methods=['GET', 'POST'])
def add():
    form = request.form

    if request.method == 'POST':
        content= form['content']
        d = {'content': content}
        db.ueditor.insert(d)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['upfile']
        print file
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('/Users/zhufeng/codes/ueditors/static', filename))
            return json.dumps({'original': filename, 'url': filename, 'state':'SUCCESS'})
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=upfile>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
