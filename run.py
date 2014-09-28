from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import urllib2

import os
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ueditor/', methods=['GET', 'POST'])
def ueditor():
    action = request.args.get("action", "")
    if 'config' == action:
        return json.dumps(get_config())

    if 'uploadimage' == action:
        return json.dumps(upload_image())

    return ''

@app.route('/show/', methods=['GET', 'POST'])
def show():
    content = request.form['content']
    return render_template('display.html',content=content)



def get_config():
    return {"imageActionName": "uploadimage",
            "imageFieldName": "upfile",
            "imageMaxSize": 2048000,
            "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif"],
            "imageCompressEnable": True,
            "imageCompressBorder": 1600,
            "imageInsertAlign": "none",
            "imageUrlPrefix": "",
            "imagePathFormat": ""}


def upload_image():
    import hashlib
    file_storage = request.files['upfile']
    name, extension = os.path.splitext(file_storage.filename)
    m = hashlib.md5()
    m.update(name)
    name = m.hexdigest()
    filename = name + extension
    file_path = os.path.join("static/upload/", filename)
    file_storage.save(file_path)
    return {"state": "SUCCESS",
            "url": '/'+file_path,
            "title": file_storage.filename,
            "original": file_storage.filename,
            "type": extension,
            "size": ""}


    """
    url = 'http://192.168.24.30/upload/'
    length = os.path.getsize(file_path)
    image_data = open(file_path, "rb")
    req = urllib2.Request(url, data=image_data)
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Content-Length', '%d' % length)
    req.add_header('Content-Type', 'image/jpg')
    res = urllib2.urlopen(req).read().strip()
    result = json.loads(res)

    if result['key']:
        os.remove(file_path)


    return {"state": "SUCCESS",
            "url": 'http://192.168.24.30/display/?key='+result['key'],
            "title": file_storage.filename,
            "original": file_storage.filename,
            "type": extension,
            "size": ""}

    """

if __name__ == '__main__':
    app.run(debug=True)
