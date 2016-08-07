#!/usr/bin/env python
from flask import Flask, request
import os
import sys

app = Flask(__name__)

def sanitize_html(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    return s

def formatted_pwd():
    return "<pre>%s</pre>" % sanitize_html(os.getcwd())

@app.route("/ls", methods=["GET"])
def ls():
    return "<pre>%s</pre>" % sanitize_html("\n".join(sorted(os.listdir('.'))))

@app.route("/pwd", methods=["GET"])
def pwd():
    return formatted_pwd()

@app.route("/cd", methods=["POST"])
def cd():
    d = str(request.form.get('dir'))
    if os.access(d, os.F_OK):
        sys.stdout.write("chdir: %r\n" % d)
        os.chdir(d)
    return formatted_pwd()

app.run(debug=True)
