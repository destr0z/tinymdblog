from flask import Flask, render_template, request, make_response
from markdown import markdown
from utils import slugify, requires_auth
import os

app = Flask(__name__)

@app.route("/")
def start():
    html_text = ""
    return render_template("index.html", content=html_text)

@app.route("/admin/", methods=['POST', 'GET'])
@requires_auth
def admin():
    if request.method == "POST":
        directory = "pages"
        if not os.path.exists(directory):
            os.makedirs(directory)

        title = request.form.get("title")
        if not title:
            render_template("admin.html")

        filename = slugify(title)+".md"
        content = request.form.get("content")
        with open(directory+"/"+filename, "w") as text_file:
            text_file.write(content)

    return render_template("admin.html")

@app.route("/preview/", methods=['POST', 'GET'])
def preview():
    html_text = "test"
    if request.method == "POST" and request.form.get("content"):
        text = request.form.get("content")
        html_text = markdown(text, extensions=['markdown.extensions.nl2br'])
    
    return html_text

@app.route("/<slug>", methods=['GET'])
def page(slug):
    html_text = ""
    try:
        html_text = ""
        filename = "pages/"+slug+".md"
        print filename
        with open(filename, "r") as text_file:
            if request.args.get("format") == "md":
                html_text = text_file.read()
            else:
                html_text = markdown(text_file.read(), extensions=['markdown.extensions.nl2br'])        
    except:
        pass

    if not html_text:
        resp = make_response(render_template('error.html'), 404)
    else:
        resp = make_response(render_template('index.html', content=html_text), 200)
    return resp

if __name__ == "__main__":
    app.run(debug=True)