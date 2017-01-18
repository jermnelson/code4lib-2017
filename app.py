from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route("/<page>")
def slide(page=None):
    if not page:
        redirect(home)
    return render_template("{}.html".format(page))

@app.route("/")
def default():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
