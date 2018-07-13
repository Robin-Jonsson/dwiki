from django.shortcuts import render, redirect
from django.core.files import File

import os

BASE_DIR = os.path.join(os.path.abspath('.'), 'media', 'dwiki')

def page(request, url_path=None):
    stylesheets = [
        'dwiki/css/base.css',
        'dwiki/css/page.css',
    ]

    content = 'Welcome'
    if url_path:
        url_path = os.path.join(BASE_DIR, url_path)
        if os.path.isdir(url_path):
            readme = os.path.join(url_path, 'README.md')
            if os.path.isfile(readme):
                content = parse_file(readme)
            else:
                content = 'No README file.'
        elif os.path.isfile(url_path):
            content = parse_file(url_path)
        else:
            content = 'No file or directory with that name.'

    return render(request, 'page.html', {
        'stylesheets': stylesheets,
        'structure': Structure().structure,
        'content': content,
    })

def parse_file(file_path):
    content = ''
    with open(file_path) as f:
        for line in File(f):
            content += line

    return content

class Structure():
    structure = ''

    def __init__(self):
        if not os.path.isdir(BASE_DIR):
            self.structure = 'No '+BASE_DIR+' directory.'
            return

        self.structure += '<ul>'
        self.parse_dir(BASE_DIR)
        self.structure += '</ul>'

    def parse_dir(self, dir):
        for file in sorted(os.listdir(dir), key=lambda f: f.lower()):
            file_path = os.path.join(dir, file)
            if not os.path.isdir(file_path) and dir == BASE_DIR:
                continue

            if not file.startswith('.') and not file.lower().startswith('readme'):
                file_url = file_path[len(BASE_DIR):]

                self.structure += '<li>'

                if os.path.isfile(file_path) or os.path.isfile(os.path.join(file_path, 'README.md')):
                    self.structure += '<a href="'+file_url+'">'

                self.structure += os.path.splitext(os.path.basename(file))[0]

                if os.path.isfile(file_path) or os.path.isfile(os.path.join(file_path, 'README.md')):
                    self.structure += '</a>'

                current_file = os.path.join(dir, file)
                if os.path.isdir(current_file):
                    self.structure += '<ul>'
                    self.parse_dir(current_file)
                    self.structure += '</ul>'

                self.structure += '</li>'

