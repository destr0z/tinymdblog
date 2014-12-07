import os
from os.path import basename

def get_slugs():
    html_folder = os.environ.get("HTML_FOLDER")
    all_files = os.listdir(html_folder)
    all_slugs = []

    for filename in all_files:
        all_slugs.append(filename.split('.')[0])
    return all_slugs
