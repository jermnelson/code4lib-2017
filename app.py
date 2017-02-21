__author__ = "Jeremy Nelson"

import glob
import os
import re
import sys
from flask import Flask, jsonify, render_template, redirect, request 
from flask import session, url_for
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

PRESENTATION_ROOT = os.path.abspath(os.path.dirname(__file__))
CONTENT = dict()
for template in glob.iglob(os.path.join(PRESENTATION_ROOT, "templates/*.html")):
    if template.endswith("base.html") or template.endswith("navbar.html") or\
        template.endswith("footer.html"):
         continue
    content_key = os.path.split(template)[-1].split(".")[0] 
    CONTENT[content_key] = []
    for line in open(template, 'r'):
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
    return render_template("index.html")

if __name__ == "__main__":
    # Initialized content
    app.run(debug=True, host="0.0.0.0", port=5005)
