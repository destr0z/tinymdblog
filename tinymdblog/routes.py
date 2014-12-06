from flask import Flask, render_template, request, make_response
from markdown import markdown
from utils import requires_auth
from slugify import slugify
from tinymdblog import app
import os


@app.route('/')
def start():
    html_text = ''
    return render_template('index.html', content=html_text)

@app.route('/admin/', methods=['POST', 'GET'])
@requires_auth
def admin():
    if request.method == 'POST':
        md_folder = os.environ.get('MD_FOLDER')
        html_folder = os.environ.get('HTML_FOLDER')
        if not os.path.exists(md_folder):
            os.makedirs(md_folder)

        if not os.path.exists(html_folder):
            os.makedirs(html_folder)

        title = request.form.get('title')
        if not title:
            render_template('admin.html')

        filename = slugify(title)
        content = request.form.get('content')
        with open(md_folder+'/'+filename+'.md', 'w') as text_file:
            text_file.write(content.encode('utf8'))
            text_file.close()

        html_text = markdown(content, extensions=['markdown.extensions.nl2br'])
        html_page = render_template('index.html', content=html_text)
        with open(html_folder+'/'+filename+'.html', 'w') as html_file:
            html_file.write(html_page.encode('utf8'))
            html_file.close()

    return render_template('admin.html')

@app.route('/preview/', methods=['POST', 'GET'])
def preview():
    html_text = 'test'
    if request.method == 'POST' and request.form.get('content'):
        text = request.form.get('content')
        html_text = markdown(text, extensions=['markdown.extensions.nl2br'])

    return html_text

@app.route('/<slug>', methods=['GET'])
def page(slug):
    html_text = ''
    try:
        html_text = ''
        md_folder = os.environ.get('MD_FOLDER')
        filename = md_folder+'/'+slug+'.md'
        print filename
        with open(filename, 'r') as text_file:
            html_text = markdown(text_file.read(), extensions=['markdown.extensions.nl2br'])
    except:
        pass

    if not html_text:
        resp = make_response(render_template('error.html'), 404)
    else:
        resp = make_response(render_template('index.html', content=html_text), 200)
    return resp
