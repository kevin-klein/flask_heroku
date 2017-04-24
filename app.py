"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

###
# Routing for your application.
###

def get_content(sub_path=''):
    base_path = os.path.expanduser('~/101web/data/')
    if sub_path:
        path = os.path.join(base_path, sub_path)
    else:
        path = base_path

    if os.path.isfile(path):
        return [path, None]

    folder_content = os.listdir(path)
    folder_content = map(lambda f: os.path.join(path, f), folder_content)
    files = filter(lambda f: os.path.isfile(f), folder_content)
    dirs = filter(lambda f: not os.path.isfile(f), folder_content)

    files = map(lambda f: f.replace(base_path, ''), files)
    dirs = map(lambda f: f.replace(base_path, ''), dirs)

    return [files, dirs]

@app.route('/')
def home():
    """Send your static text file."""

    files, dirs = get_content()
    return render_template('home.html', files=files, dirs=dirs)

@app.route('/<path:name>')
def resource(name):
    files, dirs = get_content(name)
    if dirs is not None:
        return render_template('home.html', files=files, dirs=dirs)
    else:
        return send_file(files)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
