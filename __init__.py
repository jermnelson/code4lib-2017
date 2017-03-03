__author__ = "Jeremy Nelson"

import glob
import jinja2
import hashlib
import os
import re
import sys
from flask import Flask, jsonify, render_template, redirect, request 
from flask import session, url_for
app = Flask(__name__)
if not "SECRET_KEY" in app.config:
    app.config["SECRET_KEY"] = hashlib.sha256(os.urandom(45)).hexdigest()

PRESENTATION_ROOT = os.path.abspath(os.path.dirname(__file__))
CONTENT = dict()

def populate_content():
    global CONTENT
    for template in glob.iglob(os.path.join(PRESENTATION_ROOT, "templates/*.html")):
        if template.endswith("base.html") or template.endswith("navbar.html") or\
            template.endswith("footer.html") or template.endswith("favicon.html") or\
            template.endswith("ico.html"):
            continue
        content_key = os.path.split(template)[-1].split(".")[0] 
        CONTENT[content_key] = []
        raw_html = render_template("{}.html".format(content_key))
#    for line in open(template, 'r'):
        for line in raw_html.splitlines():
            CONTENT[content_key].append(line)
         
@app.route("/search", methods=['GET', 'POST'])
def search():
    q = request.values.get('query')
    hits = []
    regex = re.compile(q)
    for filename in CONTENT.keys():
        for i, line in enumerate(CONTENT[filename]):
            if regex.search(line):
                hits.append((filename, i, line))
    session['search-results'] = {"results": hits, "query": q}
    return redirect(url_for('results'))

@app.route("/hits")
def results():
    if 'search-results' in session:
        results = session['search-results']
    else:
        results = {}
    return render_template('search-results.html', results=results)
    
    

@app.route("/<page>")
def slide(page=None):
    if not page:
        redirect(default)
    return render_template("{}.html".format(page))

@app.route("/")
def default():
    if len(CONTENT) < 1:
        populate_content()
    return render_template("index.html")


