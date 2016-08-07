#!/usr/bin/env python
from flask import Flask, request
from subprocess import Popen, PIPE
import os
import sys

app = Flask(__name__)

def premod(s):
    #return "<pre>%s</pre>" % str(s)
    return str(s)

def sanitize_html(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    return s

def formatted_pwd():
    return premod(sanitize_html(os.getcwd()))

@app.route("/ls", methods=["GET"])
def ls():
    return premod(sanitize_html("\n".join(sorted(os.listdir(".")))))

@app.route("/pwd", methods=["GET"])
def pwd():
    return formatted_pwd()

@app.route("/cd", methods=["POST"])
def cd():
    d = str(request.form.get("dir"))
    if os.access(d, os.F_OK):
        sys.stdout.write("chdir: %r\n" % d)
        os.chdir(d)
        return formatted_pwd()
    else:
        return "EACCES"

def zerointeractioncmd(args):
    proc = Popen(args, stdout=PIPE)
    (stdout, _) = proc.communicate()
    return premod(sanitize_html(stdout))

@app.route("/git/diff", methods=["GET"])
def gitdiff():
    return zerointeractioncmd(["git", "diff"])

@app.route("/git/log", methods=["GET"])
def gitlog():
    #return zerointeractioncmd(["git", "log", "--pretty=oneline"])
    return zerointeractioncmd(["git", "log", "--pretty=format:On %ad, %an committed %B"])[:10000]

@app.route("/git/status", methods=["GET"])
def gitstatus():
    return zerointeractioncmd(["git", "status"])

@app.route("/git/add", methods=["POST"])
def gitadd():
    f = str(request.form.get("filename"))
    if os.access(f, os.F_OK):
        return zerointeractioncmd(["git", "add", f])
    else:
        return "EACCES"

@app.route("/git/commit", methods=["POST"])
def gitcommit():
    m = str(request.form.get("message"))
    return zerointeractioncmd(["git", "commit", "-m", m])

@app.route("/git/pull", methods=["POST"])
def gitpull():
    return zerointeractioncmd(["git", "pull"])

@app.route("/git/push", methods=["POST"])
def gitpush():
    return zerointeractioncmd(["git", "push"])

app.run(debug=True)
