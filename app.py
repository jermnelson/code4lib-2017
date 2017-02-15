from flask import Flask, render_template, redirect
app = Flask(__name__)

#@app.template_filter('is_active')
#def active_category(path):
#    if path.endswith('catalog-pull-platform'):
#        return 'active'
#    elif path.endswith('setup-env') or path.endswith('create-knowledge-graph') or\
#         path.endswith('ingesting-marc') or path.endswith('ingesting-metadata'):
#        return 'active'
#    elif path.endswith('cc-etd') or path.end

@app.route("/<page>")
def slide(page=None):
    if not page:
        redirect(default)
    return render_template("{}.html".format(page))

@app.route("/")
def default():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
